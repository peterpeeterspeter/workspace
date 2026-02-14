#!/usr/bin/env python3
"""
Check for broken internal links and 404 sources
"""

import requests
import re

AUTH = ("admin", "GyOC qXGg K82P hxRt ZjbY 2v9k")

# Common broken link patterns to check
POTENTIAL_BROKEN_LINKS = [
    "/shortcodes/",
    "/typography/",
    "/blog-classic-2-columns/",
    "/blog-classic-3-columns/",
    "/all-posts",
]

def check_page_exists(path):
    """Check if a page exists"""
    url = f"https://www.cardfair.com{path}"
    try:
        response = requests.head(url, timeout=5, allow_redirects=True)
        return response.status_code == 200
    except:
        return False

print("="*80)
print("🔍 CHECKING FOR BROKEN LINKS ON CARDFAIR.COM")
print("="*80)
print()

print("Testing previously drafted demo pages...")
print("-"*80)

broken_links = []
working_links = []

for path in POTENTIAL_BROKEN_LINKS:
    exists = check_page_exists(path)
    status = "✅ 200 OK" if exists else "❌ 404/Redirect"
    print(f"{status} - {path}")

    if not exists:
        broken_links.append(path)
    else:
        working_links.append(path)

print()
print("="*80)
print("SUMMARY")
print("="*80)

if broken_links:
    print(f"\n❌ BROKEN LINKS FOUND ({len(broken_links)}):")
    for link in broken_links:
        print(f"  - {link}")
    print("\n🔧 These need 301 redirects!")
else:
    print("\n✅ All tested links are working!")

if working_links:
    print(f"\n✅ WORKING LINKS ({len(working_links)}):")
    for link in working_links:
        print(f"  - {link}")

print()
print("="*80)
print("🔧 RECOMMENDED ACTIONS")
print("="*80)
print("""
1. Set up 301 redirects for broken demo pages:
   - /shortcodes/ → /secured-credit-cards/
   - /typography/ → /credit-cards/
   - /blog-classic-* → /blog/ (if exists)

2. Check Google Search Console for 404 report:
   - Coverage → Not found (404)
   - Identify top 404 pages
   - Add redirects

3. Submit updated sitemap to GSC
""")
