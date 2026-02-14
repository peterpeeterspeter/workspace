#!/usr/bin/env python3
import re

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


# Test with the actual crashcasino article
file_path = '/root/.openclaw/workspace/drafts/batch3-crashcasino-007-casino-selection-checklist.md'
markdown_content = get_content_without_frontmatter(file_path)

# Convert to HTML
html_content = markdown_to_html(markdown_content)

# Check for affiliate links
has_cybet = 'cybetplay.com' in html_content
has_bitstarz = 'bzstarz1.com' in html_content
has_affiliate_table = '<table>' in html_content and 'Vetted Safe Crash Casinos' in html_content

print("=" * 60)
print("Conversion Test Results")
print("=" * 60)
print(f"Has <table> tags: {html_content.count('<table>')}")
print(f"Has Cybet affiliate link: {has_cybet}")
print(f"Has BitStarz affiliate link: {has_bitstarz}")
print(f"Has affiliate table section: {has_affiliate_table}")

if has_affiliate_table:
    # Extract the affiliate table section
    import re
    table_match = re.search(r'<blockquote>.*?</blockquote>.*?<table>.*?</table>', html_content, re.DOTALL)
    if table_match:
        print("\nAffiliate table found:")
        print(table_match.group(0)[:800])
    else:
        # Just find the table
        table_match = re.search(r'<table>.*?</table>', html_content, re.DOTALL)
        if table_match:
            print("\nFirst table found:")
            print(table_match.group(0)[:800])
