#!/usr/bin/env python3
"""
Fixed conversion script that handles tables inside blockquotes
"""

import json
import re
import subprocess

# WordPress credentials
CRASHCASINO_URL = "https://crashcasino.io/wp-json"
CRASHCASINO_USER = "peter"
CRASHCASINO_PASS = "3vRhtTs2khfdLtTiDFqkdeXI"

CRASHGAME_URL = "https://crashgamegambling.com/wp-json"
CRASHGAME_USER = "@peter"
CRASHGAME_PASS = "MioX SygN Xaz6 pK9o RUiK tBMF"


def markdown_to_html(markdown_text):
    """Convert markdown to HTML with proper support for tables inside blockquotes"""
    lines = markdown_text.split('\n')
    html_lines = []
    in_paragraph = False
    in_code_block = False
    in_table = False
    in_blockquote = False
    in_blockquote_table = False
    table_has_header = False
    blockquote_buffer = []

    def flush_blockquote_buffer():
        """Convert buffered blockquote lines to HTML"""
        nonlocal blockquote_buffer
        if not blockquote_buffer:
            return None

        # Join the buffer and check if it contains a table
        bq_text = '\n'.join(blockquote_buffer)
        blockquote_buffer = []

        # Check if the blockquote contains a table
        if '|' in bq_text and not bq_text.strip().startswith('```'):
            # It's a table inside blockquote
            bq_lines = bq_text.split('\n')
            html_parts = ['<blockquote>']
            in_bq_table = False
            table_has_header_bq = False

            for line in bq_lines:
                # Remove the > prefix if present
                clean_line = line.strip()
                if clean_line.startswith('>'):
                    clean_line = clean_line[1:].strip()

                # Check if this line is part of a table
                if '|' in clean_line and clean_line.strip() != '':
                    pipe_count = clean_line.count('|')
                    if pipe_count >= 2:
                        if not in_bq_table:
                            if html_parts and html_parts[-1] != '<blockquote>':
                                html_parts.append('<p>')
                                html_parts.append('</p>')
                            html_parts.append('<table>')
                            in_bq_table = True
                            table_has_header_bq = False
                        else:
                            table_has_header_bq = True

                        # Check if it's a separator row
                        if re.match(r'^[\s\-:]+\|[\s\-:]+\|', clean_line) or re.match(r'^[\s\-:]+\|$', clean_line):
                            continue

                        # Parse table row
                        if clean_line.startswith('|'):
                            clean_line = clean_line[1:]
                        if clean_line.endswith('|'):
                            clean_line = clean_line[:-1]

                        cells = [cell.strip() for cell in clean_line.split('|')]
                        if cells:
                            tag = 'th' if not table_has_header_bq else 'td'
                            html_parts.append('<tr>')
                            for cell in cells:
                                cell = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', cell)
                                cell = re.sub(r'\*(.*?)\*', r'<em>\1</em>', cell)
                                cell = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2" target="_blank" rel="nofollow noopener">\1</a>', cell)
                                html_parts.append(f'<{tag}>{cell}</{tag}>')
                            html_parts.append('</tr>')
                elif clean_line.strip() != '':
                    # Regular blockquote content
                    if in_bq_table:
                        html_parts.append('</tbody></table>')
                        in_bq_table = False
                    # Apply formatting
                    clean_line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', clean_line)
                    clean_line = re.sub(r'\*(.*?)\*', r'<em>\1</em>', clean_line)
                    clean_line = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2" target="_blank" rel="nofollow noopener">\1</a>', clean_line)
                    html_parts.append(f'<p>{clean_line}</p>')

            if in_bq_table:
                html_parts.append('</tbody></table>')

            html_parts.append('</blockquote>')
            return '\n'.join(html_parts)
        else:
            # Regular blockquote
            bq_content = bq_text.replace('> ', '').strip()
            bq_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', bq_content)
            bq_content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', bq_content)
            bq_content = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2" target="_blank" rel="nofollow noopener">\1</a>', bq_content)
            return f'<blockquote>{bq_content}</blockquote>'

    for line in lines:
        # Skip frontmatter markers
        if line.strip() == '---':
            continue

        # Code blocks
        if line.strip().startswith('```'):
            # Flush any pending blockquote
            bq_html = flush_blockquote_buffer()
            if bq_html:
                html_lines.append(bq_html)
                in_paragraph = False

            in_code_block = not in_code_block
            if in_code_block:
                html_lines.append('<pre><code>')
            else:
                html_lines.append('</code></pre>')
            in_paragraph = False
            continue

        if in_code_block:
            html_lines.append(line)
            continue

        # Blockquotes (including tables inside blockquotes)
        if line.strip().startswith('>'):
            if not in_blockquote:
                # Start of blockquote
                if in_paragraph:
                    html_lines.append('</p>')
                    in_paragraph = False
                in_blockquote = True
            blockquote_buffer.append(line)
            # Don't add to html_lines yet - wait for flush
            continue

        # Flush blockquote if we're not in one anymore
        if in_blockquote and not line.strip().startswith('>'):
            bq_html = flush_blockquote_buffer()
            if bq_html:
                html_lines.append(bq_html)
                in_paragraph = False
            in_blockquote = False

        # Tables (not in blockquote)
        if '|' in line and line.strip() != '' and not in_blockquote:
            pipe_count = line.count('|')
            if pipe_count >= 2:
                if in_paragraph:
                    html_lines.append('</p>')
                    in_paragraph = False

                if not in_table:
                    html_lines.append('<table>')
                    in_table = True
                    table_has_header = False

                if re.match(r'^\|?[\s\-:]+\|[\s\-:]+\|', line) or re.match(r'^\|[\s\-:]+\|$', line):
                    if not table_has_header:
                        html_lines.append('</thead><tbody>')
                        table_has_header = True
                    continue

                clean_line = line.strip()
                if clean_line.startswith('|'):
                    clean_line = clean_line[1:]
                if clean_line.endswith('|'):
                    clean_line = clean_line[:-1]

                cells = [cell.strip() for cell in clean_line.split('|')]
                if cells:
                    tag = 'th' if not table_has_header else 'td'
                    html_lines.append('<tr>')
                    for cell in cells:
                        cell = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', cell)
                        cell = re.sub(r'\*(.*?)\*', r'<em>\1</em>', cell)
                        cell = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2" target="_blank" rel="nofollow noopener">\1</a>', cell)
                        html_lines.append(f'<{tag}>{cell}</{tag}>')
                    html_lines.append('</tr>')
                continue

        # End table
        if in_table and ('|' not in line or line.strip() == ''):
            html_lines.append('</tbody></table>')
            in_table = False
            table_has_header = False

        # Headers
        if line.startswith('# '):
            if in_paragraph:
                html_lines.append('</p>')
                in_paragraph = False
            html_lines.append(f'<h1>{line[2:]}</h1>')
            continue
        elif line.startswith('## '):
            if in_paragraph:
                html_lines.append('</p>')
                in_paragraph = False
            html_lines.append(f'<h2>{line[3:]}</h2>')
            continue
        elif line.startswith('### '):
            if in_paragraph:
                html_lines.append('</p>')
                in_paragraph = False
            html_lines.append(f'<h3>{line[4:]}</h3>')
            continue

        # Horizontal rule
        if line.strip() == '---':
            if in_paragraph:
                html_lines.append('</p>')
                in_paragraph = False
            html_lines.append('<hr>')
            continue

        # Empty line
        if line.strip() == '':
            if in_paragraph:
                html_lines.append('</p>')
                in_paragraph = False
            continue

        # Regular paragraph
        formatted_line = line
        formatted_line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', formatted_line)
        formatted_line = re.sub(r'\*(.*?)\*', r'<em>\1</em>', formatted_line)
        formatted_line = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2" target="_blank" rel="nofollow noopener">\1</a>', formatted_line)
        formatted_line = re.sub(r'`([^`]+)`', r'<code>\1</code>', formatted_line)

        if not in_paragraph:
            html_lines.append('<p>')
            in_paragraph = True

        html_lines.append(formatted_line + ' ')

    # Flush any remaining blockquote
    if in_blockquote:
        bq_html = flush_blockquote_buffer()
        if bq_html:
            html_lines.append(bq_html)

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

    skipping = True
    content_lines = []

    for line in lines:
        if line.strip() == '---':
            if skipping:
                skipping = False
                continue
            else:
                skipping = False
                continue

        if not skipping:
            content_lines.append(line)

    return ''.join(content_lines)


def update_wordpress_post(site_url, username, password, post_id, title, content, excerpt):
    """Update existing post via WordPress REST API"""
    print(f"Updating post {post_id}...")

    payload = {
        "title": title,
        "content": content,
        "excerpt": excerpt
    }

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
            print(f"❌ Error: {response['message']}")
            return False

        print(f"✓ Success!")
        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    articles = [
        {
            'file': '/root/.openclaw/workspace/drafts/batch3-crashcasino-007-casino-selection-checklist.md',
            'url': CRASHCASINO_URL,
            'user': CRASHCASINO_USER,
            'pass': CRASHCASINO_PASS,
            'post_id': 818,
            'name': 'How to Choose a Safe Crash Casino'
        },
        {
            'file': '/root/.openclaw/workspace/drafts/batch3-crashcasino-008-crash-casino-scams.md',
            'url': CRASHCASINO_URL,
            'user': CRASHCASINO_USER,
            'pass': CRASHCASINO_PASS,
            'post_id': 819,
            'name': 'Crash Casino Scams'
        }
    ]

    print("=" * 60)
    print("Fixing Affiliate Links in crashcasino.io Articles")
    print("=" * 60)
    print()

    for article in articles:
        print(f"Processing: {article['name']}")

        title, description = extract_frontmatter(article['file'])
        markdown_content = get_content_without_frontmatter(article['file'])
        html_content = markdown_to_html(markdown_content)

        # Verify affiliate links are present
        has_affiliate = any(domain in html_content for domain in ['cybetplay.com', 'bzstarz1.com', 'betzrd.com', '7bit.partners'])
        print(f"  Affiliate links present: {has_affiliate}")

        result = update_wordpress_post(
            article['url'],
            article['user'],
            article['pass'],
            article['post_id'],
            title,
            html_content,
            description
        )

        print()

    print("Done!")


if __name__ == '__main__':
    main()
