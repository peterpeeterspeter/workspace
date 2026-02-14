#!/usr/bin/env python3
"""
Simple Post Cleanup - Remove broken links, fix tables, wrap lists
"""

import json
import re
import requests
from requests.auth import HTTPBasicAuth

WP_SITE_URL = "https://crashcasino.io/wp-json"
WP_USERNAME = "peter"
WP_APP_PASSWORD = "3vRhtTs2khfdLtTiDFqkdeXI"

def fetch_posts():
    url = f"{WP_SITE_URL}/wp/v2/posts?per_page=20&status=publish"
    response = requests.get(url, auth=HTTPBasicAuth(WP_USERNAME, WP_APP_PASSWORD))
    return response.json()

def fix_broken_headings(content):
    """Fix headings with broken internal links"""
    # Fix <h{level}> broken pattern
    content = re.sub(r'<h\{level\}>[^<]*</h\{level\}>', '', content)

    # Fix headings with links inside them
    for level in range(1, 7):
        # Pattern: <hX>text <a href="internal">word</a> more text</hX>
        pattern = rf'(<h{level}[^>]*>)([^<]*?)<a href="https://www\.crashcasino\.io/[^"]*"[^>]*>([^<]+)</a>([^<]*?</h{level}>)'
        replacement = r'\1\2\3\4'
        content = re.sub(pattern, replacement, content)

    return content

def fix_markdown_tables(content):
    """Convert markdown tables to HTML - simplified"""
    lines = content.split('\n')
    result = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Start of markdown table
        if line.startswith('|') and '|' in line and '<' not in line:
            table_rows = []

            # Collect table rows
            while i < len(lines) and lines[i].strip().startswith('|'):
                # Skip separator rows (contain ---)
                if '---' not in lines[i]:
                    cells = [c.strip() for c in lines[i].split('|')[1:-1]]
                    table_rows.append(cells)
                i += 1

            # Convert to HTML table
            if table_rows:
                table_html = '<table>'
                for row_idx, row in enumerate(table_rows):
                    tag = 'th' if row_idx == 0 else 'td'
                    table_html += '<tr>'
                    for cell in row:
                        table_html += f'<{tag}>{cell}</{tag}>'
                    table_html += '</tr>'
                table_html += '</table>'
                result.append(table_html)
            continue

        result.append(lines[i])
        i += 1

    return '\n'.join(result)

def wrap_loose_lis(content):
    """Wrap <li> tags that aren't in <ul> or <ol>"""
    # Simple approach: find consecutive <li> tags and wrap them
    result = []
    lines = content.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i]

        # Check if this line contains a loose <li>
        if '<li>' in line and '</li>' in line:
            # Check if it's NOT already inside a list
            if not any(tag in '\n'.join(lines[max(0,i-5):i]) for tag in ['<ul>', '<ol>']):
                # Start of a list
                result.append('<ul>')
                result.append(line)

                # Add subsequent <li> tags
                i += 1
                while i < len(lines) and '<li>' in lines[i] and '</li>' in lines[i]:
                    # Make sure we're not inside a different tag
                    if not any(tag in lines[i] for tag in ['</ul>', '</ol>', '<ul>', '<ol>']):
                        result.append(lines[i])
                    else:
                        break
                    i += 1

                result.append('</ul>')
                continue

        result.append(line)
        i += 1

    return '\n'.join(result)

def update_post(post_id, content):
    url = f"{WP_SITE_URL}/wp/v2/posts/{post_id}"
    response = requests.post(
        url,
        auth=HTTPBasicAuth(WP_USERNAME, WP_APP_PASSWORD),
        json={'content': content},
        headers={'Content-Type': 'application/json'}
    )
    return response.status_code == 200

def main():
    print("🔧 Simple Post Cleanup")
    print("=" * 50)
    print()

    posts = fetch_posts()

    for post in posts:
        post_id = post['id']
        content = post['content']['rendered']
        original = content

        print(f"📄 Post {post_id}...")

        # Apply fixes
        content = fix_broken_headings(content)
        content = fix_markdown_tables(content)
        content = wrap_loose_lis(content)

        # Update if changed
        if content != original:
            if update_post(post_id, content):
                print(f"   ✅ Fixed")
            else:
                print(f"   ❌ Failed")
        else:
            print(f"   ⏭️  OK")

    print()
    print("✅ Done!")

if __name__ == '__main__':
    main()
