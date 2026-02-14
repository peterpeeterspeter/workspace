#!/usr/bin/env python3
"""
Smart Content Repair for Pinch-to-Post
Fixes broken HTML, converts markdown to Gutenberg, adds proper internal links
"""

import json
import re
import requests
from requests.auth import HTTPBasicAuth
from html import unescape
from bs4 import BeautifulSoup

# Configuration
WP_SITE_URL = "https://crashcasino.io/wp-json"
WP_USERNAME = "peter"
WP_APP_PASSWORD = "3vRhtTs2khfdLtTiDFqkdeXI"

AFFILIATE_LINKS = {
    "stake": "https://cybetplay.com/tluy6cbpp",
    "bc.game": "https://cybetplay.com/tluy6cbpp",
    "bcgame": "https://cybetplay.com/tluy6cbpp",
    "roobet": "https://cybetplay.com/tluy6cbpp",
    "thunderpick": "https://cybetplay.com/tluy6cbpp",
    "metaspins": "https://cybetplay.com/tluy6cbpp",
}

def fetch_posts(limit=20):
    """Fetch published posts"""
    url = f"{WP_SITE_URL}/wp/v2/posts?per_page={limit}&status=publish"
    response = requests.get(url, auth=HTTPBasicAuth(WP_USERNAME, WP_APP_PASSWORD))
    response.raise_for_status()
    return response.json()

def remove_broken_internal_links(html):
    """Remove internal links that are breaking HTML structure"""
    # Remove links inside HTML attributes (e.g., id="text<a href...>")
    html = re.sub(r'(<[^>]*)(<a href="https://crashcasino\.io/[^"]*"[^>]*>)([^<]*)(</a>)([^>]*>)',
                  r'\1\3\5', html)

    # Remove links inside heading tags
    for level in range(1, 7):
        pattern = f'<h{level}([^>]*)>([^<]*)((<a href="https://www\.crashcasino\.io/[^"]*"[^>]*>)([^<]+)(</a>))([^<]*)</h{level}>'
        replacement = r'<h{level}\1>\2\5\7</h{level}>'
        html = re.sub(pattern, replacement, html)

    return html

def convert_markdown_tables_to_html(html):
    """Convert markdown tables to HTML tables"""
    # Find markdown table patterns (rows with | separators)
    lines = html.split('\n')
    in_table = False
    table_rows = []
    result = []

    for line in lines:
        # Check if this is a markdown table row
        if '|' in line and line.strip().startswith('|'):
            if not in_table:
                in_table = True
                table_rows = []

            # Parse table cells
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            table_rows.append(cells)

        elif in_table:
            # End of table, convert to HTML
            if table_rows:
                html_table = convert_table_rows_to_html(table_rows)
                result.append(html_table)
            in_table = False
            table_rows = []
            result.append(line)
        else:
            result.append(line)

    # Handle case where table ends at EOF
    if in_table and table_rows:
        html_table = convert_table_rows_to_html(table_rows)
        result.append(html_table)

    return '\n'.join(result)

def convert_table_rows_to_html(rows):
    """Convert parsed table rows to HTML table"""
    if not rows:
        return ''

    html = ['<!-- wp:table -->', '<figure class="wp-block-table">']

    # Check if second row is a separator (contains ---)
    is_header = len(rows) > 1 and any('---' in cell for cell in rows[1])

    html.append('<table>')

    for i, row in enumerate(rows):
        if i == 1 and is_header:
            # Skip separator row
            continue

        tag = 'thead' if i == 0 and is_header else 'tbody'
        cell_tag = 'th' if i == 0 and is_header else 'td'

        if i == 0 or (i == 1 and is_header):
            if i == 0:
                html.append(f'<{tag}>')
        elif i == 1:
            html.append('<tbody>')

        html.append('<tr>')
        for cell in row:
            # Clean up separator characters
            cell = re.sub(r'^-+|-+$', '', cell.strip())
            cell = re.sub(r'^:+:?$|^:|:$|^=+|=+$', '', cell.strip())
            html.append(f'<{cell_tag}>{cell}</{cell_tag}>')
        html.append('</tr>')

        # Close thead after header row
        if i == 0 and is_header:
            html.append('</thead>')

    html.append('</tbody></table></figure>')
    html.append('<!-- /wp:table -->')

    return '\n'.join(html)

def fix_lists(html):
    """Wrap loose <li> tags in <ul> or <ol>"""
    # This is complex, so we'll use BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Find all loose <li> tags (not already in <ul> or <ol>)
    for li in soup.find_all('li', recursive=False):
        if li.parent.name not in ['ul', 'ol', 'menu']:
            # Wrap in <ul>
            new_ul = soup.new_tag('ul')
            li.wrap(new_ul)

    return str(soup)

def add_smart_internal_links(html, post_title, all_posts):
    """Add internal links only to plain text, not inside HTML tags"""
    # Extract plain text from HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Get current internal link count
    current_links = len(soup.find_all('a', href=re.compile(r'crashcasino\.io')))
    if current_links >= 3:
        return html, 0

    # Find relevant posts to link to
    keywords = extract_keywords_from_title(post_title)
    relevant_posts = find_relevant_posts(keywords, all_posts, limit=3)

    if not relevant_posts:
        return html, 0

    links_added = 0
    links_to_add = 3 - current_links

    # Add links to paragraph text only
    for p in soup.find_all('p'):
        if links_added >= links_to_add:
            break

        # Get text content
        text = p.get_text()

        # Skip if already has links or is too short
        if p.find('a') or len(text) < 50:
            continue

        # Try to add a link
        for target_post in relevant_posts:
            if links_added >= links_to_add:
                break

            # Find keyword match
            for keyword in target_post['keywords']:
                if keyword.lower() in text.lower():
                    # Create new link
                    new_link = soup.new_tag('a', href=target_post['url'])
                    new_link.string = keyword

                    # Find and replace text node
                    for content in p.contents:
                        if isinstance(content, str) and keyword.lower() in content.lower():
                            # Split the text and insert link
                            parts = re.split(f'({re.escape(keyword)})', content, flags=re.IGNORECASE)
                            new_contents = []
                            for i, part in enumerate(parts):
                                if i % 2 == 1 and part.lower() == keyword.lower():
                                    new_contents.append(new_link)
                                elif part:
                                    new_contents.append(part)
                                    # Reset position for new_link
                                    if new_link not in new_contents:
                                        new_contents.append(part)

                            # Replace the original text node
                            content.replace_with(*new_contents)
                            links_added += 1
                            break

            if links_added >= links_to_add:
                break

    return str(soup), links_added

def extract_keywords_from_title(title):
    """Extract keywords from title"""
    # Remove HTML entities
    title = unescape(title)
    title = re.sub(r'<[^>]+>', '', title)

    # Extract meaningful words
    words = re.findall(r'\b[A-Za-z]{4,}\b', title.lower())

    # Filter to relevant keywords
    relevant = ['crash', 'gambling', 'casino', 'game', 'safe', 'verify',
                'rtp', 'bonus', 'stake', 'roobet', 'aviator', 'provably',
                'fair', 'license', 'curacao', 'strategy', 'guide', 'scam']

    keywords = [w for w in words if w in relevant]

    return keywords[:5] if keywords else ['crash']

def find_relevant_posts(keywords, all_posts, limit=3):
    """Find relevant posts based on keywords"""
    scored = []

    for post in all_posts:
        score = 0
        title = unescape(post['title']['rendered'])
        title = re.sub(r'<[^>]+>', '', title).lower()

        for kw in keywords:
            if kw in title:
                score += 1

        if score > 0:
            scored.append({
                'id': post['id'],
                'title': title,
                'url': post['link'],
                'keywords': keywords,
                'score': score
            })

    scored.sort(key=lambda x: x['score'], reverse=True)
    return scored[:limit]

def add_affiliate_links(html, title):
    """Add affiliate links if missing"""
    # Check if already has affiliate links
    has_affiliate = any(domain in html.lower() for domain in ['cybetplay.com', 'stake.com'])

    # Check if it should have affiliate links
    should_have = any(word in title.lower() for word in ['casino', 'best', 'top', 'review', 'rating'])

    if not should_have or has_affiliate:
        return html, 0

    # Add affiliate section at the end
    affiliate_section = '''
<!-- wp:paragraph -->
<p><strong>Recommended Crash Casinos:</strong></p>
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":false} -->
<ul>
<li><a href="https://cybetplay.com/tluy6cbpp">Stake</a> - Best overall (9.5/10)</li>
<li><a href="https://cybetplay.com/tluy6cbpp">BC.Game</a> - Huge variety (9.3/10)</li>
<li><a href="https://cybetplay.com/tluy6cbpp">Roobet</a> - Solid choice (9.0/10)</li>
</ul>
<!-- /wp:list -->
'''

    return html + affiliate_section, 1

def update_post(post_id, content):
    """Update post via REST API"""
    url = f"{WP_SITE_URL}/wp/v2/posts/{post_id}"
    response = requests.post(
        url,
        auth=HTTPBasicAuth(WP_USERNAME, WP_APP_PASSWORD),
        json={'content': content},
        headers={'Content-Type': 'application/json'}
    )
    return response.status_code == 200

def main():
    print("🔧 Smart Content Repair for Pinch-to-Post")
    print("=" * 60)
    print()

    # Fetch all posts
    print("📋 Fetching posts...")
    posts = fetch_posts(20)
    print(f"✅ Found {len(posts)} posts")
    print()

    # Process each post
    print("🔄 Processing posts...")
    print()

    fixed_count = 0
    total_fixes = 0

    for post in posts:
        post_id = post['id']
        title = unescape(post['title']['rendered'])
        title = re.sub(r'<[^>]+>', '', title)
        content = post['content']['rendered']

        print(f"📄 [{post_id}] {title[:60]}...")

        fixes_applied = []
        new_content = content

        # 1. Remove broken internal links
        cleaned = remove_broken_internal_links(content)
        if cleaned != content:
            fixes_applied.append("Removed broken internal links")
            new_content = cleaned

        # 2. Convert markdown tables
        with_tables = convert_markdown_tables_to_html(new_content)
        if with_tables != new_content:
            fixes_applied.append("Converted markdown tables to HTML")
            new_content = with_tables

        # 3. Fix lists
        with_fixed_lists = fix_lists(new_content)
        if with_fixed_lists != new_content:
            fixes_applied.append("Fixed list formatting")
            new_content = with_fixed_lists

        # 4. Add internal links
        with_links, links_added = add_smart_internal_links(new_content, title, posts)
        if links_added > 0:
            fixes_applied.append(f"Added {links_added} internal links")
            new_content = with_links

        # 5. Add affiliate links
        with_affiliate, affiliate_added = add_affiliate_links(new_content, title)
        if affiliate_added > 0:
            fixes_applied.append("Added affiliate links section")
            new_content = with_affiliate

        # Update post if fixes were applied
        if fixes_applied:
            if update_post(post_id, new_content):
                print(f"   ✅ Fixed: {', '.join(fixes_applied)}")
                fixed_count += 1
                total_fixes += len(fixes_applied)
            else:
                print(f"   ❌ Update failed")
        else:
            print(f"   ⏭️  No fixes needed")

        print()

    print("=" * 60)
    print(f"📊 SUMMARY")
    print("=" * 60)
    print(f"Posts processed: {len(posts)}")
    print(f"Posts fixed: {fixed_count}")
    print(f"Total fixes applied: {total_fixes}")
    print()
    print("✅ Content repair complete!")

if __name__ == '__main__':
    main()
