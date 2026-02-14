#!/usr/bin/env python3
"""
Smart Internal Link Builder for Pinch-to-Post
Analyzes WordPress posts and adds contextually relevant internal links
"""

import json
import re
import requests
from requests.auth import HTTPBasicAuth
from typing import List, Dict, Set
import urllib.parse

# Configuration
WP_SITE_URL = "https://crashcasino.io/wp-json"
WP_USERNAME = "peter"
WP_APP_PASSWORD = "3vRhtTs2khfdLtTiDFqkdeXI"

# Keywords to match for internal linking
LINK_KEYWORDS = [
    'crash', 'gambling', 'casino', 'game', 'bet', 'safe', 'verify',
    'rtp', 'bonus', 'stake', 'bcgame', 'roobet', 'aviator', 'provably',
    'fair', 'license', 'curacao', 'strategy', 'guide', 'scam', 'avoid',
    'rating', 'review', 'withdrawal', 'deposit'
]

def fetch_posts() -> List[Dict]:
    """Fetch all published posts"""
    url = f"{WP_SITE_URL}/wp/v2/posts?per_page=100&status=publish"
    response = requests.get(url, auth=HTTPBasicAuth(WP_USERNAME, WP_APP_PASSWORD))
    response.raise_for_status()
    return response.json()

def extract_text_from_html(html: str) -> str:
    """Extract plain text from HTML"""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', html)
    # Decode HTML entities
    text = text.replace('&amp;', '&').replace('&#038;', '&')
    text = text.replace('&nbsp;', ' ')
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_keywords(text: str) -> Set[str]:
    """Extract keywords from text"""
    words = text.lower().split()
    keywords = set()
    for word in words:
        word = word.strip('.,!?;:()"\'')
        if word in LINK_KEYWORDS:
            keywords.add(word)
    return keywords

def find_relevant_posts(post_id: int, keywords: Set[str], all_posts: List[Dict]) -> List[Dict]:
    """Find relevant posts based on keywords"""
    relevant = []
    for post in all_posts:
        if post['id'] == post_id:
            continue

        title = extract_text_from_html(post['title']['rendered']).lower()
        content = extract_text_from_html(post['content']['rendered']).lower()

        # Count keyword matches
        matches = 0
        for kw in keywords:
            if kw in title or kw in content:
                matches += 1

        if matches > 0:
            relevant.append({
                'id': post['id'],
                'title': extract_text_from_html(post['title']['rendered']),
                'url': post['link'],
                'matches': matches
            })

    # Sort by number of matches
    relevant.sort(key=lambda x: x['matches'], reverse=True)
    return relevant[:3]  # Top 3

def count_internal_links(content: str) -> int:
    """Count internal links in content"""
    return len(re.findall(r'href="https://crashcasino\.io', content))

def add_internal_link(content: str, target_post: Dict, keyword: str) -> str:
    """Add an internal link to content"""
    # Find first occurrence of keyword in content and wrap with link
    # Look for keyword not already in a link
    pattern = rf'(?<!href=")(?<!>)\b({re.escape(keyword)})\b(?![^<]*</a>)'

    def replacer(match):
        return f'<a href="{target_post["url"]}">{match.group(1)}</a>'

    new_content = re.sub(pattern, replacer, content, count=1, flags=re.IGNORECASE)

    # If keyword not found, add link at end
    if new_content == content:
        new_content = content + f'\n\n<p><strong>Related:</strong> <a href="{target_post["url"]}">{target_post["title"]}</a></p>'

    return new_content

def update_post(post_id: int, content: str) -> bool:
    """Update post with new content"""
    url = f"{WP_SITE_URL}/wp/v2/posts/{post_id}"
    data = {'content': content}

    response = requests.post(
        url,
        auth=HTTPBasicAuth(WP_USERNAME, WP_APP_PASSWORD),
        json=data,
        headers={'Content-Type': 'application/json'}
    )

    return response.status_code == 200

def main():
    print("🔗 Smart Internal Link Builder")
    print("=" * 50)
    print()

    # Fetch all posts
    print("📋 Fetching published posts...")
    posts = fetch_posts()
    print(f"✅ Found {len(posts)} posts")
    print()

    # Process each post
    print("🔄 Processing posts...")
    print()

    updated = 0
    skipped = 0
    total_links_added = 0

    for post in posts:
        post_id = post['id']
        title = extract_text_from_html(post['title']['rendered'])
        content = post['content']['rendered']

        # Count existing internal links
        current_links = count_internal_links(content)

        # Skip if already has 3+ links
        if current_links >= 3:
            print(f"⏭️  [{post_id}] \"{title}\" - Already has {current_links} links")
            skipped += 1
            continue

        print(f"📝 [{post_id}] \"{title}\"")
        print(f"   Current internal links: {current_links}")

        # Extract keywords from post
        text = extract_text_from_html(content)
        keywords = extract_keywords(text)

        if not keywords:
            print("   ⚠️  No keywords found")
            continue

        # Find relevant posts
        relevant = find_relevant_posts(post_id, keywords, posts)

        if not relevant:
            print("   ⚠️  No relevant posts found")
            continue

        # Add links
        links_to_add = min(3 - current_links, len(relevant))
        links_added = 0
        new_content = content

        for target_post in relevant[:links_to_add]:
            # Use first matched keyword
            keyword = list(keywords)[0] if keywords else 'related'

            # Check if already linked
            if target_post['url'] in new_content:
                continue

            new_content = add_internal_link(new_content, target_post, keyword)
            links_added += 1
            print(f"   ➕ Added link to: \"{target_post['title']}\"")

        # Update post if links added
        if links_added > 0:
            if update_post(post_id, new_content):
                print(f"   ✅ Updated (+{links_added} links)")
                updated += 1
                total_links_added += links_added
            else:
                print("   ❌ Update failed")
        else:
            print("   ⚠️  No links added")

        print()

    # Summary
    print("=" * 50)
    print("📊 SUMMARY")
    print("=" * 50)
    print(f"Total posts analyzed: {len(posts)}")
    print(f"Posts updated: {updated}")
    print(f"Posts skipped: {skipped}")
    print(f"Total links added: {total_links_added}")
    print()
    print("✅ Done!")

if __name__ == '__main__':
    main()
