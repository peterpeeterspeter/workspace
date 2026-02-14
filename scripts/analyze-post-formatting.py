#!/usr/bin/env python3
"""
Analyze WordPress posts for HTML formatting and affiliate link issues
"""

import json
import re
import requests
from requests.auth import HTTPBasicAuth

# Configuration
WP_SITE_URL = "https://crashcasino.io/wp-json"
WP_USERNAME = "peter"
WP_APP_PASSWORD = "3vRhtTs2khfdLtTiDFqkdeXI"

def fetch_posts(limit=20):
    """Fetch published posts"""
    url = f"{WP_SITE_URL}/wp/v2/posts?per_page={limit}&status=publish"
    response = requests.get(url, auth=HTTPBasicAuth(WP_USERNAME, WP_APP_PASSWORD))
    return response.json()

def analyze_html_formatting(content):
    """Check for HTML formatting issues"""
    issues = []

    # Check for links inside HTML attributes (broken by bad internal linking)
    attr_links = re.findall(r'<[^>]*<a href=["\'][^"\']*["\'][^>]*>', content)
    if attr_links:
        issues.append(f"❌ Links inside HTML attributes: {len(attr_links)} found")

    # Check for broken heading tags
    broken_headings = re.findall(r'<h[1-6][^>]*>[^<]*<a href[^>]*>[^<]*</a>[^<]*</h[1-6]>', content)
    if broken_headings:
        issues.append(f"⚠️  Links inside headings (non-semantic): {len(broken_headings)}")

    # Check for raw <li> without <ul>/<ol>
    # Simplified check - just look for <li> not preceded by </ul> or </ol> in nearby context
    loose_lis = re.findall(r'<li>', content)
    parent_uls = re.findall(r'<ul>|<ol>', content)
    if len(loose_lis) > len(parent_uls) + 10:  # Allow some margin
        issues.append(f"⚠️  Possible <li> tags without proper lists: {len(loose_lis)} <li>, {len(parent_uls)} <ul>/<ol>")

    # Check for tables formatted as paragraphs (markdown-style)
    table_as_text = re.findall(r'\|.*\|', content)
    if len(table_as_text) > 10:
        issues.append(f"⚠️  Markdown tables not converted: {len(table_as_text)} table rows")

    return issues

def check_affiliate_links(content, title):
    """Check for affiliate links"""
    affiliate_patterns = [
        r'cybetplay\.com',
        r'stake\.com',
        r'bc\.game',
        r'roobet\.com',
        r'thunderpick\.com',
        r'metaspins\.com'
    ]

    has_affiliate = any(re.search(pattern, content, re.IGNORECASE) for pattern in affiliate_patterns)

    # Check if it looks like it should have affiliate links
    should_have = any(word in title.lower() for word in ['casino', 'best', 'top', 'review', 'rating'])

    if should_have and not has_affiliate:
        return "❌ Should have affiliate links but doesn't"
    elif has_affiliate:
        return "✅ Has affiliate links"
    else:
        return "⏭️  Doesn't need affiliate links"

def check_internal_links(content):
    """Count internal links"""
    internal_links = re.findall(r'href="https://crashcasino\.io', content)
    return len(internal_links)

def main():
    print("📊 WordPress Post Analysis")
    print("=" * 60)
    print()

    posts = fetch_posts(20)

    print(f"Analyzing {len(posts)} posts...")
    print()

    total_issues = 0

    for post in posts:
        post_id = post['id']
        title = post['title']['rendered']
        content = post['content']['rendered']

        # Strip HTML entities for display
        title_clean = re.sub(r'<[^>]+>', '', title)
        title_clean = title_clean.replace('&#038;', '&').replace('&#8217;', "'")

        print(f"📄 Post {post_id}: {title_clean[:60]}...")

        # Check HTML formatting
        html_issues = analyze_html_formatting(content)

        # Check affiliate links
        affiliate_status = check_affiliate_links(content, title_clean)

        # Check internal links
        internal_count = check_internal_links(content)

        # Report
        if html_issues:
            print("   HTML Issues:")
            for issue in html_issues:
                print(f"   {issue}")
                total_issues += 1
        else:
            print("   ✅ HTML formatting looks good")

        print(f"   {affiliate_status}")
        print(f"   🔗 Internal links: {internal_count}")

        # Show a snippet if there are issues
        if html_issues:
            print()
            print("   Sample broken HTML:")
            # Find first broken heading or attribute
            broken = re.search(r'<h[1-6][^>]*>[^<]{0,30}<a href[^>]*>[^<]{0,20}</a>', content)
            if broken:
                snippet = broken.group(0)[:100]
                print(f"   {snippet}...")
            else:
                broken_attr = re.search(r'<[^>]*<a href=["\'][^"\']*["\'][^>]*>', content)
                if broken_attr:
                    snippet = broken_attr.group(0)[:100]
                    print(f"   {snippet}...")

        print()

    print("=" * 60)
    print(f"Total posts with HTML issues: {total_issues}")
    print()

if __name__ == '__main__':
    main()
