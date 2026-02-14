#!/usr/bin/env python3
"""
Update Batch 3 Articles with Fixed Affiliate Links
Republishes the 4 articles with corrected HTML table conversion
"""

import json
import re
import subprocess
import sys
from datetime import datetime

# WordPress credentials
CRASHGAME_URL = "https://crashgamegambling.com/wp-json"
CRASHGAME_USER = "peter"
CRASHGAME_PASS = "MioX SygN Xaz6 pK9o RUiK tBMF"

CRASHCASINO_URL = "https://crashcasino.io/wp-json"
CRASHCASINO_USER = "peter"
CRASHCASINO_PASS = "3vRhtTs2khfdLtTiDFqkdeXI"

def markdown_to_html(markdown_text):
    """Convert markdown to HTML with proper table and link support"""
    lines = markdown_text.split('\n')
    html_lines = []
    in_paragraph = False
    in_code_block = False
    in_table = False
    table_has_header = False

    for line in lines:
        # Skip frontmatter
        if line.strip() == '---':
            continue

        # Code blocks
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            if in_code_block:
                html_lines.append('<pre><code>')
            else:
                html_lines.append('</code></pre>')
            in_paragraph = False
            continue

        if in_code_block:
            html_lines.append(f'{line}')
            continue

        # Tables - improved detection
        if '|' in line and line.strip() != '' and not line.strip().startswith('>'):
            # Count pipe characters to confirm it's a table
            pipe_count = line.count('|')
            if pipe_count >= 2:  # At least 2 pipes means it's likely a table row
                if not in_table:
                    html_lines.append('<table>')
                    in_table = True
                    table_has_header = False

                # Check if it's a separator row
                if re.match(r'^\|?[\s\-:]+\|[\s\-:]+\|', line) or re.match(r'^\|[\s\-:]+\|$', line):
                    if not table_has_header:
                        html_lines.append('</thead><tbody>')
                        table_has_header = True
                    continue

                # Parse table row
                # Remove leading/trailing pipes if present
                clean_line = line.strip()
                if clean_line.startswith('|'):
                    clean_line = clean_line[1:]
                if clean_line.endswith('|'):
                    clean_line = clean_line[:-1]

                cells = [cell.strip() for cell in clean_line.split('|')]
                if cells:
                    tag = 'th' if not table_has_header else 'td'
                    html_lines.append(f'<tr>')
                    for cell in cells:
                        # Apply formatting within cells - ORDER MATTERS
                        # 1. Bold **text**
                        cell = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', cell)
                        # 2. Italic *text*
                        cell = re.sub(r'\*(.*?)\*', r'<em>\1</em>', cell)
                        # 3. Links [text](url) - FIXED with proper HTML attributes
                        cell = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2" target="_blank" rel="nofollow noopener">\1</a>', cell)

                        html_lines.append(f'<{tag}>{cell}</{tag}>')
                    html_lines.append('</tr>')
                continue

        # End table
        if in_table and ('|' not in line or line.strip() == ''):
            html_lines.append('</tbody></table>')
            in_table = False
            table_has_header = False
            in_paragraph = False
            # Continue processing this line

        # Headers (outside tables)
        if line.startswith('# ') and not in_table:
            if in_paragraph:
                html_lines.append('</p>')
                in_paragraph = False
            html_lines.append(f'<h1>{line[2:]}</h1>')
            continue
        elif line.startswith('## ') and not in_table:
            if in_paragraph:
                html_lines.append('</p>')
                in_paragraph = False
            html_lines.append(f'<h2>{line[3:]}</h2>')
            continue
        elif line.startswith('### ') and not in_table:
            if in_paragraph:
                html_lines.append('</p>')
                in_paragraph = False
            html_lines.append(f'<h3>{line[4:]}</h3>')
            continue

        # Horizontal rule
        if line.strip() == '---' and not in_table:
            if in_paragraph:
                html_lines.append('</p>')
                in_paragraph = False
            html_lines.append('<hr>')
            continue

        # Blockquotes
        if line.strip().startswith('> ') and not in_table:
            if in_paragraph:
                html_lines.append('</p>')
                in_paragraph = False
            # Extract blockquote content and handle inline formatting
            bq_content = line.strip()[2:]
            # Apply formatting
            bq_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', bq_content)
            bq_content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', bq_content)
            bq_content = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2" target="_blank" rel="nofollow noopener">\1</a>', bq_content)
            html_lines.append(f'<blockquote>{bq_content}</blockquote>')
            # Handle multi-line blockquotes
            html_lines.append('<p>')
            in_paragraph = True
            continue

        # Empty line
        if line.strip() == '':
            if in_paragraph:
                html_lines.append('</p>')
                in_paragraph = False
            continue

        # Regular paragraph (skip if we're in a table)
        if in_table:
            continue

        formatted_line = line

        # Bold
        formatted_line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', formatted_line)

        # Italic
        formatted_line = re.sub(r'\*(.*?)\*', r'<em>\1</em>', formatted_line)

        # Links with proper HTML attributes
        formatted_line = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2" target="_blank" rel="nofollow noopener">\1</a>', formatted_line)

        # Inline code
        formatted_line = re.sub(r'`([^`]+)`', r'<code>\1</code>', formatted_line)

        if not in_paragraph:
            html_lines.append('<p>')
            in_paragraph = True

        html_lines.append(formatted_line + ' ')

    # Close any open tags
    if in_paragraph:
        html_lines.append('</p>')
    if in_table:
        html_lines.append('</tbody></table>')

    return '\n'.join(html_lines)


def extract_frontmatter(markdown_file):
    """Extract title and description from frontmatter"""
    with open(markdown_file, 'r') as f:
        lines = f.readlines()

    title = "Untitled"
    description = ""

    for line in lines:
        if line.startswith('title:'):
            title = line.split(':', 1)[1].strip().strip('"').strip("'")
        elif line.startswith('description:'):
            description = line.split(':', 1)[1].strip().strip('"').strip("'")

    return title, description


def get_content_without_frontmatter(markdown_file):
    """Get markdown content without frontmatter"""
    with open(markdown_file, 'r') as f:
        lines = f.readlines()

    # Skip lines between first and second ---
    skipping = True
    content_lines = []

    for line in lines:
        if line.strip() == '---':
            if skipping:
                skipping = False
                continue
            else:
                # Second ---, start keeping content
                skipping = False
                continue

        if not skipping:
            content_lines.append(line)

    return ''.join(content_lines)


def update_wordpress_post(site_url, username, password, post_id, title, content, excerpt):
    """Update existing post via WordPress REST API"""
    print(f"Updating post {post_id} on {site_url}...")

    # Build JSON payload
    payload = {
        "title": title,
        "content": content,
        "excerpt": excerpt
    }

    # Use curl to update
    curl_command = [
        'curl', '-s', '-X', 'POST',
        f"{site_url}/wp/v2/posts/{post_id}",
        '-u', f"{username}:{password}",
        '-H', 'Content-Type: application/json',
        '-d', json.dumps(payload)
    ]

    try:
        result = subprocess.run(curl_command, capture_output=True, text=True, check=True)
        response = json.loads(result.stdout)

        if 'code' in response:
            print(f"❌ Error updating: {response}")
            return False

        print(f"✓ Updated successfully!")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Error executing curl: {e}")
        print(f"  stderr: {e.stderr}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing response: {e}")
        print(f"  Response: {result.stdout}")
        return False


def main():
    print("=" * 60)
    print("Update Batch 3 Articles - Fix Affiliate Links")
    print("=" * 60)
    print()

    articles = [
        {
            'file': '/root/.openclaw/workspace/drafts/batch3-crashgame-003-cashout-strategies.md',
            'url': CRASHGAME_URL,
            'user': '@peter',  # crashgamegambling.com requires @peter
            'pass': CRASHGAME_PASS,
            'post_id': 49613,  # From TASKBOARD.md
            'name': 'Crash Gambling Cashout Strategies'
        },
        {
            'file': '/root/.openclaw/workspace/drafts/batch3-crashgame-004-crash-variants.md',
            'url': CRASHGAME_URL,
            'user': '@peter',  # crashgamegambling.com requires @peter
            'pass': CRASHGAME_PASS,
            'post_id': 49614,
            'name': 'Crash Game Variants'
        },
        {
            'file': '/root/.openclaw/workspace/drafts/crashcasino-how-to-choose-safe-crash-casino-checklist.md',
            'url': CRASHCASINO_URL,
            'user': CRASHCASINO_USER,
            'pass': CRASHCASINO_PASS,
            'post_id': 818,
            'name': 'How to Choose a Safe Crash Casino'
        },
        {
            'file': '/root/.openclaw/workspace/drafts/crashcasino-crash-casino-scams-exposed.md',
            'url': CRASHCASINO_URL,
            'user': CRASHCASINO_USER,
            'pass': CRASHCASINO_PASS,
            'post_id': 819,
            'name': 'Crash Casino Scams'
        }
    ]

    results = []

    for i, article in enumerate(articles, 1):
        print(f"[{i}/4] Updating: {article['name']} (Post ID: {article['post_id']})")

        # Check if file exists
        try:
            with open(article['file'], 'r') as f:
                pass
        except FileNotFoundError:
            print(f"⚠️  File not found: {article['file']}")
            print(f"   Trying alternate filename...")
            # Try the batch3 filename instead
            alt_file = article['file'].replace('crashgamegambling-cashout-strategy-maximum-profit.md', 'batch3-crashgame-003-cashout-strategies.md')
            alt_file = alt_file.replace('crashgamegambling-crash-variants-rocket-game-types.md', 'batch3-crashgame-004-crash-variants.md')
            alt_file = alt_file.replace('crashcasino-how-to-choose-safe-crash-casino-checklist.md', 'batch3-crashcasino-007-casino-selection-checklist.md')
            alt_file = alt_file.replace('crashcasino-crash-casino-scams-exposed.md', 'batch3-crashcasino-008-crash-casino-scams.md')
            
            try:
                with open(alt_file, 'r') as f:
                    article['file'] = alt_file
                    print(f"   ✓ Found: {alt_file}")
            except FileNotFoundError:
                print(f"   ❌ Alternate file also not found. Skipping.")
                print()
                continue

        # Extract frontmatter
        title, description = extract_frontmatter(article['file'])

        # Get content without frontmatter
        markdown_content = get_content_without_frontmatter(article['file'])

        # Convert to HTML
        html_content = markdown_to_html(markdown_content)

        # Update post
        result = update_wordpress_post(
            article['url'],
            article['user'],
            article['pass'],
            article['post_id'],
            title,
            html_content,
            description
        )

        if result:
            results.append(article['name'])

        print()

    print("=" * 60)
    print(f"✓ Updated {len(results)}/{len(articles)} articles successfully!")
    print("=" * 60)

    if results:
        print("\n📝 Updated Articles:")
        for result in results:
            print(f"  • {result}")


if __name__ == '__main__':
    main()
