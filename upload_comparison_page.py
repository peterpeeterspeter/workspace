#!/usr/bin/env python3
"""
Upload Credit Card Comparison Pages to WordPress via REST API
"""

import requests
import json

AUTH = ("admin", "GyOC qXGg K82P hxRt ZjbY 2v9k")

# Read the HTML content
html_file = '/root/.openclaw/workspace/secured-cards-page.html'

with open(html_file, 'r') as f:
    html_content = f.read()

# Extract title from HTML
import re
title_match = re.search(r'<title>(.*?)</title>', html_content)
title = title_match.group(1) if title_match else "Best Secured Credit Cards 2025"

# Extract meta description
desc_match = re.search(r'<meta name="description" content="([^"]*)"', html_content)
meta_description = desc_match.group(1) if desc_match else ""

print("="*80)
print("📤 UPLOADING COMPARISON PAGE TO WORDPRESS")
print("="*80)
print()
print(f"Title: {title}")
print(f"Slug: secured-credit-cards-2025")
print()

# Create page via WordPress API
url = "https://cardfair.com/wp-json/wp/v2/pages"

payload = {
    "title": title,
    "content": html_content,
    "slug": "secured-credit-cards-2025",
    "status": "publish",
    "meta": {
        "rank_math_title": title,
        "rank_math_description": meta_description,
        "rank_math_focus_keyword": "best secured credit cards 2025",
        "rank_math_canonical_url": "https://www.cardfair.com/secured-credit-cards-2025/"
    }
}

try:
    response = requests.post(url, auth=AUTH, json=payload, timeout=30)

    if response.status_code == 201:
        result = response.json()
        page_url = result.get('link', '')
        page_id = result.get('id', '')

        print("✅ PAGE CREATED SUCCESSFULLY!")
        print()
        print(f"   Page ID: {page_id}")
        print(f"   URL: {page_url}")
        print()
        print("="*80)
        print("🎯 NEXT STEPS:")
        print("="*80)
        print("1. View the page: " + page_url)
        print("2. Add affiliate links to 'Apply Now' buttons")
        print("3. Submit to Google Search Console")
        print("4. Add to navigation menu")
        print()
        print("="*80)
        print("✅ DEPLOYMENT COMPLETE")

    else:
        print(f"❌ Error: HTTP {response.status_code}")
        print(f"Response: {response.text[:500]}")

except Exception as e:
    print(f"❌ Error: {e}")

print()
