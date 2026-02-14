#!/usr/bin/env python3
"""Test markdown table conversion"""

import re

def markdown_to_html_fixed(markdown_text):
    """Convert markdown to HTML with proper table support"""
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
                        # 3. Links [text](url)
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

        # Links
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


# Test with the affiliate table
test_markdown = """
| Casino | Crash Games | Min Deposit | Key Feature | ⭐ Play Now |
|--------|-------------|-------------|-------------|------------|
| **Cybet** | Aviator, Crash X | $20 | Instant withdrawals, 50% RS commission | [Play](https://cybetplay.com/tluy6cbpp) |
| **BitStarz** | Aviator, Spaceman | $20 | Fastest payouts, industry reputation | [Play](https://bzstarz1.com/b196c322b) |
| **Betzrd** | Crash, Aviator | $10 | Smooth UX, strong crash lineup | [Play](https://betzrd.com/pyondmfcx) |
| **7Bit Casino** | Multiple variants | $20 | Excellent mobile, huge game library | [Play](https://7bit.partners/p4i4w1udu) |
"""

print("=" * 60)
print("TEST: Markdown Table Conversion")
print("=" * 60)
print("\nINPUT (Markdown):")
print(test_markdown)
print("\nOUTPUT (HTML):")
result = markdown_to_html_fixed(test_markdown)
print(result)
