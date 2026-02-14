#!/usr/bin/env python3
"""
Better Markdown to Gutenberg Converter
Handles tables, lists, and proper HTML conversion
"""

import re
import sys
from html import escape

def markdown_to_gutenberg(md_text):
    """Convert markdown to Gutenberg blocks"""
    lines = md_text.split('\n')
    result = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Skip empty lines
        if not line:
            i += 1
            continue

        # Headings
        if line.startswith('#'):
            level = len(re.match(r'^#+', line).group())
            text = line.lstrip('#').strip()
            result.append(f'<!-- wp:heading {{"level":{level}}} -->')
            result.append(f'<h{level}>{text}</h{level}>')
            result.append(f'<!-- /wp:heading -->')
            result.append('')

        # Tables
        elif line.startswith('|') and '|' in line[1:]:
            table_rows = []
            # Collect all table rows
            while i < len(lines) and lines[i].strip().startswith('|'):
                row = lines[i].strip()
                # Skip separator rows
                if '---' not in row:
                    cells = [escape(c.strip()) for c in row.split('|')[1:-1]]
                    table_rows.append(cells)
                i += 1

            # Generate HTML table
            if table_rows:
                result.append('<!-- wp:table -->')
                result.append('<figure class="wp-block-table">')
                result.append('<table>')

                for row_idx, row in enumerate(table_rows):
                    tag = 'th' if row_idx == 0 else 'td'
                    result.append('<tr>' if row_idx == 0 else '')
                    if row_idx > 0:
                        result.append('<tbody>' if row_idx == 1 else '')
                    for cell in row:
                        # Process inline markdown in cells
                        cell = process_inline(cell)
                        result.append(f'<{tag}>{cell}</{tag}>')
                    result.append('</tr>')

                result.append('</tbody></table></figure>')
                result.append('<!-- /wp:table -->')
                result.append('')
            continue

        # Lists
        elif line.startswith('- ') or line.startswith('* '):
            items = []
            while i < len(lines) and (lines[i].strip().startswith('- ') or lines[i].strip().startswith('* ')):
                text = lines[i].strip()[2:]
                text = process_inline(text)
                items.append(f'<li>{text}</li>')
                i += 1

            result.append('<!-- wp:list -->')
            result.append('<ul>')
            result.extend(items)
            result.append('</ul>')
            result.append('<!-- /wp:list -->')
            result.append('')
            continue

        # Blockquotes
        elif line.startswith('> '):
            text = line[2:]
            text = process_inline(text)
            result.append('<!-- wp:quote -->')
            result.append(f'<blockquote class="wp-block-quote"><p>{text}</p></blockquote>')
            result.append('<!-- /wp:quote -->')
            result.append('')

        # Paragraphs
        else:
            text = process_inline(line)
            result.append('<!-- wp:paragraph -->')
            result.append(f'<p>{text}</p>')
            result.append('<!-- /wp:paragraph -->')
            result.append('')

        i += 1

    return '\n'.join(result)

def process_inline(text):
    """Process inline markdown: bold, italic, links, code"""
    # Escape HTML first
    text = escape(text)

    # Links: [text](url)
    text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', text)

    # Bold: **text**
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)

    # Italic: *text*
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)

    # Code: `text`
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)

    return text

if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            md_content = f.read()
    else:
        md_content = sys.stdin.read()

    gutenberg_html = markdown_to_gutenberg(md_content)
    print(gutenberg_html)
