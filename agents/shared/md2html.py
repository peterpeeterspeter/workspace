#!/usr/bin/env python3
"""
Markdown to HTML Converter for WordPress Publishing
Converts markdown articles to properly formatted HTML for WordPress REST API
"""

import sys
import re
import json
from html import escape

def markdown_to_html(md_content):
    """Convert markdown to HTML with proper formatting"""

    html_lines = []
    lines = md_content.split('\n')

    in_code_block = False
    in_list = False
    list_items = []

    for line in lines:
        # Code blocks
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            if in_code_block:
                html_lines.append('<pre><code>')
            else:
                html_lines.append('</code></pre>')
            continue

        if in_code_block:
            html_lines.append(escape(line) + '\n')
            continue

        # Headers
        if line.startswith('# '):
            if in_list:
                html_lines.append('</ul>\n')
                in_list = False
            text = line[2:].strip()
            html_lines.append(f'<h1>{text}</h1>\n')
        elif line.startswith('## '):
            if in_list:
                html_lines.append('</ul>\n')
                in_list = False
            text = line[3:].strip()
            html_lines.append(f'<h2>{text}</h2>\n')
        elif line.startswith('### '):
            if in_list:
                html_lines.append('</ul>\n')
                in_list = False
            text = line[4:].strip()
            html_lines.append(f'<h3>{text}</h3>\n')
        elif line.startswith('#### '):
            if in_list:
                html_lines.append('</ul>\n')
                in_list = False
            text = line[5:].strip()
            html_lines.append(f'<h4>{text}</h4>\n')

        # Horizontal rule
        elif line.strip() == '---':
            if in_list:
                html_lines.append('</ul>\n')
                in_list = False
            html_lines.append('<hr>\n')

        # Bold text
        elif '**' in line:
            if in_list:
                html_lines.append('</ul>\n')
                in_list = False
            # Convert **bold** to <strong>
            line = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', line)
            # Convert *italic* to <em>
            line = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', line)
            html_lines.append(f'<p>{line}</p>\n')

        # Links [text](url)
        elif '[' in line and '](' in line:
            if in_list:
                html_lines.append('</ul>\n')
                in_list = False
            line = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', line)
            html_lines.append(f'<p>{line}</p>\n')

        # Unordered list items
        elif line.strip().startswith('- ') or line.strip().startswith('* '):
            if not in_list:
                html_lines.append('<ul>\n')
                in_list = True
            text = line.strip()[2:].strip()
            html_lines.append(f'<li>{text}</li>\n')

        # Ordered list items
        elif re.match(r'^\d+\.\s', line.strip()):
            if in_list:
                html_lines.append('</ul>\n')
                in_list = False
            # Handle ordered lists (simplified)
            text = re.sub(r'^\d+\.\s', '', line.strip())
            html_lines.append(f'<p>{text}</p>\n')

        # Tables (basic support)
        elif '|' in line and line.strip():
            if in_list:
                html_lines.append('</ul>\n')
                in_list = False
            cells = [cell.strip() for cell in line.split('|')]
            cells = [c for c in cells if c]  # Remove empty cells

            if cells:
                if not html_lines or not html_lines[-1].startswith('<table'):
                    html_lines.append('<table>\n')
                html_lines.append('<tr>')
                for cell in cells:
                    tag = 'th' if '---' not in line else 'td'
                    html_lines.append(f'<{tag}>{cell}</{tag}>')
                html_lines.append('</tr>\n')

        # Regular paragraphs
        elif line.strip():
            if in_list:
                html_lines.append('</ul>\n')
                in_list = False
            html_lines.append(f'<p>{line}</p>\n')

    # Close any open tags
    if in_list:
        html_lines.append('</ul>\n')

    return ''.join(html_lines)

def extract_metadata(md_content):
    """Extract metadata from markdown frontmatter or headers"""

    metadata = {
        'title': '',
        'description': '',
        'keywords': [],
        'site': ''
    }

    lines = md_content.split('\n')

    in_frontmatter = False
    for line in lines:
        # YAML frontmatter
        if line.strip() == '---' and not in_frontmatter and not metadata['title']:
            in_frontmatter = True
            continue
        elif line.strip() == '---' and in_frontmatter:
            in_frontmatter = False
            continue

        # Parse frontmatter
        if in_frontmatter:
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower()
                value = value.strip()
                if key == 'title':
                    metadata['title'] = value.strip("'").strip('"')
                elif key == 'description':
                    metadata['description'] = value.strip("'").strip('"')
                elif key == 'keywords':
                    metadata['keywords'] = [k.strip() for k in value.split(',')]
            continue

        # Title from H1
        if line.startswith('# ') and not metadata['title']:
            metadata['title'] = line[2:].strip()

        # Metadata fields
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
    main()
