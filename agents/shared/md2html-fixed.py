#!/usr/bin/env python3
"""
PROPER Markdown to HTML Converter - Fixes all WordPress HTML issues
Handles YAML frontmatter, tables, proper tag closing
"""

import sys
import re
from html import escape

def markdown_to_html(md_content):
    """Convert markdown to properly formatted HTML"""

    html_lines = []
    lines = md_content.split('\n')

    in_code_block = False
    in_table = False
    in_frontmatter = False
    table_rows = []
    frontmatter_count = 0

    for line in lines:
        # YAML frontmatter detection
        if line.strip() == '---':
            frontmatter_count += 1
            if frontmatter_count <= 2:  # Skip first two --- markers
                in_frontmatter = not in_frontmatter
                continue

        if in_frontmatter:
            continue

        # Code blocks
        if line.strip().startswith('```'):
            if in_code_block:
                # Close code block
                if table_rows:
                    # Finish table first
                    html_lines.append('<table>\n')
                    html_rows = []
                    for row in table_rows:
                        html_rows.append('<tr>' + row + '</tr>\n')
                    html_lines.extend(html_rows)
                    html_lines.append('</table>\n')
                    table_rows = []
                html_lines.append('</code></pre>\n')
            else:
                html_lines.append('<pre><code>\n')
            in_code_block = not in_code_block
            continue

        if in_code_block:
            html_lines.append(escape(line) + '\n')
            continue

        # Horizontal rule
        if line.strip() == '---':
            html_lines.append('<hr/>\n')
            continue

        # Tables
        if '|' in line and line.strip() and not line.strip().startswith('|'):
            # Skip separator rows
            if '|----' in line or '| ---' in line or '|===' in line:
                continue

            # Check if this looks like a table row
            cells = [cell.strip() for cell in line.split('|')]
            cells = [c for c in cells if c and c.strip()]  # Remove empty

            if len(cells) >= 2:  # At least 2 columns = table
                # Convert markdown cells to HTML
                row_html = ''
                for cell in cells:
                    # Process cell content (bold, links, italic)
                    cell = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', cell)
                    cell = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', cell)
                    # Fix links in table cells to ensure they have protocol
                    cell = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', 
                        lambda m: f'<a href="{("https://" + m.group(2) if not (m.group(2).startswith("http://") or m.group(2).startswith("https://") or m.group(2).startswith("/")) and "." in m.group(2) else m.group(2))}">{m.group(1)}</a>', cell)
                    row_html += f'<td>{cell}</td>'

                table_rows.append(row_html)
                in_table = True
                continue

        # Close table if we hit a non-table line
        if in_table and (not line.strip() or line.startswith('#') or '|' not in line):
            if table_rows:
                html_lines.append('<table>\n')
                for row in table_rows:
                    html_lines.append(f'<tr>{row}</tr>\n')
                html_lines.append('</table>\n')
                table_rows = []
            in_table = False

        # Headers
        if line.startswith('# '):
            text = line[2:].strip()
            text = process_inline(text)
            html_lines.append(f'<h1>{text}</h1>\n')
        elif line.startswith('## '):
            text = line[3:].strip()
            text = process_inline(text)
            html_lines.append(f'<h2>{text}</h2>\n')
        elif line.startswith('### '):
            text = line[4:].strip()
            text = process_inline(text)
            html_lines.append(f'<h3>{text}</h3>\n')
        elif line.startswith('#### '):
            text = line[5:].strip()
            text = process_inline(text)
            html_lines.append(f'<h4>{text}</h4>\n')

        # Lists
        elif line.strip().startswith('- ') or line.strip().startswith('* '):
            text = line.strip()[2:].strip()
            text = process_inline(text)
            html_lines.append(f'<li>{text}</li>\n')
        elif re.match(r'^\d+\.\s', line.strip()):
            text = re.sub(r'^\d+\.\s', '', line.strip())
            text = process_inline(text)
            html_lines.append(f'<li>{text}</li>\n')

        # Regular paragraphs
        elif line.strip():
            text = process_inline(line.strip())
            html_lines.append(f'<p>{text}</p>\n')

    # Close any open table
    if in_table and table_rows:
        html_lines.append('<table>\n')
        for row in table_rows:
            html_lines.append(f'<tr>{row}</tr>\n')
        html_lines.append('</table>\n')

    return ''.join(html_lines)

def process_inline(text):
    """Process inline markdown (bold, italic, links)"""

    # Links [text](url) - ensure URL has protocol
    def fix_link(match):
        link_text = match.group(1)
        url = match.group(2)
        # Add https:// if URL doesn't have a protocol
        if not url.startswith('http://') and not url.startswith('https://') and not url.startswith('/'):
            # Check if it looks like a domain (contains a dot and no spaces)
            if '.' in url and ' ' not in url:
                url = 'https://' + url
        return f'<a href="{url}">{link_text}</a>'
    
    text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', fix_link, text)

    # Bold **text**
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)

    # Italic *text*
    text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', text)

    # Code `text`
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)

    return text

def extract_metadata(md_content):
    """Extract metadata from markdown"""

    metadata = {
        'title': '',
        'description': '',
        'keywords': [],
        'site': ''
    }

    lines = md_content.split('\n')

    in_frontmatter = False
    frontmatter_lines = []

    for line in lines:
        # YAML frontmatter
        if line.strip() == '---':
            if not in_frontmatter and not frontmatter_lines:
                in_frontmatter = True
                continue
            elif in_frontmatter:
                in_frontmatter = False
                # Parse frontmatter
                for fm_line in frontmatter_lines:
                    if ':' in fm_line:
                        key, value = fm_line.split(':', 1)
                        key = key.strip().lower()
                        value = value.strip()
                        if key == 'title':
                            metadata['title'] = value.strip("'").strip('"')
                        elif key == 'description':
                            metadata['description'] = value.strip("'").strip('"')
                        elif key == 'keywords':
                            metadata['keywords'] = [k.strip() for k in value.split(',')]
                continue

        if in_frontmatter:
            frontmatter_lines.append(line)
            continue

        # Extract from body
        if line.startswith('# ') and not metadata['title']:
            metadata['title'] = line[2:].strip()

        if '**Title:' in line or '**Title Tag:' in line:
            metadata['title'] = line.split(':', 1)[1].strip().strip('*').strip()

        if '**Meta Description:' in line or '**description:' in line:
            metadata['description'] = line.split(':', 1)[1].strip().strip('*').strip()

        if '**Target Keywords:' in line or '**keywords:' in line:
            keywords_str = line.split(':', 1)[1].strip().strip('*').strip()
            metadata['keywords'] = [k.strip() for k in keywords_str.split(',')]

        if '**Site:**' in line or '**Site:' in line:
            site = line.split(':', 1)[1].strip().strip('*').strip()
            metadata['site'] = site

    return metadata

def main():
    if len(sys.argv) < 2:
        print(json.dumps({'error': 'No markdown file provided'}))
        sys.exit(1)

    md_file = sys.argv[1]

    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # Extract metadata
        metadata = extract_metadata(md_content)

        # Convert to HTML
        html_content = markdown_to_html(md_content)

        # Output result
        result = {
            'metadata': metadata,
            'html': html_content
        }

        print(json.dumps(result, indent=2))

    except Exception as e:
        print(json.dumps({'error': str(e)}))
        sys.exit(1)

if __name__ == '__main__':
    import json
    main()
