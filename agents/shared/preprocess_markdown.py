#!/usr/bin/env python3
"""
Preprocessor for pinch-to-post WordPress publishing
- Strips YAML frontmatter
- Converts markdown tables to Gutenberg table blocks
"""

import sys
import re

def strip_yaml_frontmatter(content):
    """Remove YAML frontmatter from markdown"""
    lines = content.split('\n')

    # Find first ---
    start = -1
    for i, line in enumerate(lines):
        if line.strip() == '---':
            start = i
            break

    if start == -1:
        return content  # No frontmatter

    # Find second ---
    end = -1
    for i in range(start + 1, len(lines)):
        if lines[i].strip() == '---':
            end = i
            break

    if end == -1:
        return content  # Unclosed frontmatter, return as-is

    # Return content after frontmatter
    return '\n'.join(lines[end + 1:])

def convert_markdown_tables(content):
    """Convert markdown tables to HTML tables (Gutenberg-compatible)"""

    lines = content.split('\n')
    result = []
    in_table = False
    table_rows = []

    for line in lines:
        # Check if line looks like a table row
        if '|' in line and line.strip() and not line.strip().startswith('#'):
            # Skip separator rows
            if re.match(r'^\s*\|?(\s*:?-+:?\s*\|)+\s*$', line):
                continue

            cells = [cell.strip() for cell in line.split('|')]
            cells = [c for c in cells if c]  # Remove empty cells from edges

            if len(cells) >= 2:  # At least 2 columns = table
                # Process inline markdown in cells
                row_cells = []
                for cell in cells:
                    # Bold
                    cell = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', cell)
                    # Italic
                    cell = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', cell)
                    # Links
                    cell = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', cell)
                    # Code
                    cell = re.sub(r'`([^`]+)`', r'<code>\1</code>', cell)
                    row_cells.append(cell)

                table_rows.append(f'<tr>{"".join(f"<td>{c}</td>" for c in row_cells)}</tr>')
                in_table = True
                continue

        # Close table if we hit a non-table line
        if in_table and table_rows:
            result.append('<!-- wp:table -->')
            result.append('<figure class="wp-block-table">')
            result.append('<table>')
            result.extend(table_rows)
            result.append('</table>')
            result.append('</figure>')
            result.append('<!-- /wp:table -->')
            result.append('')
            table_rows = []
            in_table = False

        result.append(line)

    # Close any open table at end
    if in_table and table_rows:
        result.append('<!-- wp:table -->')
        result.append('<figure class="wp-block-table">')
        result.append('<table>')
        result.extend(table_rows)
        result.append('</table>')
        result.append('</figure>')
        result.append('<!-- /wp:table -->')

    return '\n'.join(result)

def main():
    if len(sys.argv) < 2:
        print("Usage: preprocess_markdown.py <input.md> [output.md]", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Step 1: Strip YAML frontmatter
    content = strip_yaml_frontmatter(content)

    # Step 2: Convert tables to HTML
    content = convert_markdown_tables(content)

    # Output
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Preprocessed: {input_file} → {output_file}", file=sys.stderr)
    else:
        print(content)

if __name__ == '__main__':
    main()
