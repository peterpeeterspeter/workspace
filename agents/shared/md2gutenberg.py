#!/usr/bin/env python3
"""
Convert markdown to WordPress Gutenberg blocks
Extracted from pinch-to-post wp-rest.sh
"""

import sys
import re

def markdown_to_gutenberg(md_content):
    """Convert markdown to Gutenberg blocks"""
    html_lines = []
    lines = md_content.split('\n')
    in_list = False
    list_items = []

    for line in lines:
        # Close list if needed
        if in_list and not re.match(r'^[*-]\s+', line.strip()):
            if list_items:
                html_lines.append('<!-- wp:list -->')
                html_lines.append(f'<ul>{"".join(f"<li>{i}</li>" for i in list_items)}</ul>')
                html_lines.append('<!-- /wp:list -->')
                html_lines.append('')
            in_list = False
            list_items = []

        # Headings
        if line.startswith('### '):
            html_lines.append('<!-- wp:heading {"level":3} -->')
            html_lines.append(f'<h3>{line[4:].strip()}</h3>')
            html_lines.append('<!-- /wp:heading -->')
            html_lines.append('')
        elif line.startswith('## '):
            html_lines.append('<!-- wp:heading -->')
            html_lines.append(f'<h2>{line[3:].strip()}</h2>')
            html_lines.append('<!-- /wp:heading -->')
            html_lines.append('')
        elif line.startswith('# '):
            html_lines.append('<!-- wp:heading {"level":1} -->')
            html_lines.append(f'<h1>{line[2:].strip()}</h1>')
            html_lines.append('<!-- /wp:heading -->')
            html_lines.append('')
        elif line.strip() == '---':
            html_lines.append('<!-- wp:separator -->')
            html_lines.append('<hr class="wp-block-separator"/>')
            html_lines.append('<!-- /wp:separator -->')
            html_lines.append('')
        elif re.match(r'^[*-]\s+', line.strip()):
            in_list = True
            list_items.append(line.strip()[2:])
        elif line.strip():
            # Process inline markdown
            processed = line.strip()

            # Bold
            processed = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', processed)
            # Italic
            processed = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', processed)
            # Code
            processed = re.sub(r'`([^`]+)`', r'<code>\1</code>', processed)
            # Links
            processed = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', processed)

            html_lines.append('<!-- wp:paragraph -->')
            html_lines.append(f'<p>{processed}</p>')
            html_lines.append('<!-- /wp:paragraph -->')
            html_lines.append('')

    # Close any open list
    if in_list and list_items:
        html_lines.append('<!-- wp:list -->')
        html_lines.append(f'<ul>{"".join(f"<li>{i}</li>" for i in list_items)}</ul>')
        html_lines.append('<!-- /wp:list -->')
        html_lines.append('')

    return '\n'.join(html_lines)

if __name__ == '__main__':
    md_content = sys.stdin.read()
    print(markdown_to_gutenberg(md_content))
