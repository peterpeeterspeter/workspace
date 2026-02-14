#!/usr/bin/env python3
"""
Generate XML Sitemap for Cardfair.com
Crawls WordPress sitemaps and creates master sitemap
"""

import requests
import xml.etree.ElementTree as ET
from urllib.parse import urljoin
from datetime import datetime

DOMAIN = "https://www.cardfair.com"
SITEMAPS = [
    "https://www.cardfair.com/page-sitemap.xml",
    "https://www.cardfair.com/post-sitemap.xml",
    "https://www.cardfair.com/category-sitemap.xml"
]

OUTPUT_FILE = "/root/.openclaw/workspace/sitemap-cardfair.xml"

def fetch_sitemap_urls(sitemap_url):
    """Fetch all URLs from a sitemap"""
    urls = []
    try:
        response = requests.get(sitemap_url, timeout=10)
        if response.status_code != 200:
            print(f"  ⚠️ Failed to fetch: {sitemap_url}")
            return urls

        root = ET.fromstring(response.content)

        # Try sitemapindex (sitemap of sitemaps)
        for sm in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap/{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
            urls.append(sm.text)

        # Try urlset (actual URLs)
        for url in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
            urls.append(url.text)

        print(f"  ✅ {sitemap_url}: {len(urls)} URLs")

    except Exception as e:
        print(f"  ❌ Error parsing {sitemap_url}: {e}")

    return urls

def generate_sitemap():
    """Generate master XML sitemap"""
    print("="*80)
    print("🗺️  GENERATING XML SITEMAP FOR CARDFAIR.COM")
    print("="*80)
    print()

    all_urls = []

    # Fetch all sitemaps
    print("Fetching sitemaps...")
    print("-"*80)

    for sitemap in SITEMAPS:
        urls = fetch_sitemap_urls(sitemap)
        all_urls.extend(urls)

    print()
    print(f"Total URLs found: {len(all_urls)}")
    print()

    # Remove duplicates while preserving order
    seen = set()
    unique_urls = []
    for url in all_urls:
        if url not in seen:
            seen.add(url)
            unique_urls.append(url)

    print(f"Unique URLs: {len(unique_urls)}")
    print()

    # Generate XML sitemap
    print("Generating XML sitemap...")
    print("-"*80)

    urlset = ET.Element("urlset")
    urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
    urlset.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    urlset.set("xsi:schemaLocation", "http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd")

    today = datetime.now().strftime("%Y-%m-%d")

    # Prioritize important pages
    priority_map = {
        "/": "1.0",
        "/secured-credit-cards/": "0.9",
        "/credit-cards/": "0.9",
        "/credit-card-services/": "0.8",
        "/apply/": "0.8",
    }

    changefreq_map = {
        "/": "daily",
        "/secured-credit-cards/": "weekly",
        "/credit-cards/": "weekly",
    }

    for url in unique_urls:
        url_elem = ET.SubElement(urlset, "url")

        loc = ET.SubElement(url_elem, "loc")
        loc.text = url

        lastmod = ET.SubElement(url_elem, "lastmod")
        lastmod.text = today

        # Determine priority
        path = url.replace(DOMAIN, "").rstrip("/")
        priority = priority_map.get(path, "0.6")

        prio = ET.SubElement(url_elem, "priority")
        prio.text = priority

        # Determine change frequency
        changefreq = changefreq_map.get(path, "monthly")
        freq = ET.SubElement(url_elem, "changefreq")
        freq.text = changefreq

    # Pretty print XML
    from xml.dom import minidom
    xml_str = ET.tostring(urlset, encoding="unicode")
    pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="  ")

    # Remove extra blank lines
    pretty_xml = "\n".join([line for line in pretty_xml.split("\n") if line.strip()])

    # Save to file
    with open(OUTPUT_FILE, "w") as f:
        f.write(pretty_xml)

    print(f"✅ Sitemap generated: {OUTPUT_FILE}")
    print()

    # Statistics
    print("="*80)
    print("📊 SITEMAP STATISTICS")
    print("="*80)
    print(f"Total URLs: {len(unique_urls)}")
    print(f"File size: {len(pretty_xml):,} bytes ({len(pretty_xml)/1024:.1f} KB)")
    print()

    print("Priority distribution:")
    print("-"*80)
    priorities = {}
    for url in unique_urls:
        path = url.replace(DOMAIN, "").rstrip("/")
        prio = priority_map.get(path, "0.6")
        priorities[prio] = priorities.get(prio, 0) + 1

    for prio in sorted(priorities.keys(), reverse=True):
        count = priorities[prio]
        bar = "█" * int(count / 5)
        print(f"  Priority {prio}: {count:3d} pages {bar}")

    print()
    print("="*80)
    print("🎯 NEXT STEPS")
    print("="*80)
    print("""
1. Upload sitemap to WordPress:
   - Copy sitemap-cardfair.xml to WordPress root
   - OR use Rank Math to regenerate sitemap automatically

2. Submit to Google Search Console:
   - https://search.google.com/search-console
   - Sitemaps → Add new sitemap
   - Submit: sitemap.xml

3. Submit to Bing Webmaster Tools:
   - https://www.bing.com/webmasters
   - Sitemaps → Submit sitemap

4. Submit to IndexNow for instant indexing:
   - Use indexnow_submitter.py

5. Monitor indexing:
   - Check GSC Coverage report
   - Verify pages are being indexed
    """)

if __name__ == "__main__":
    generate_sitemap()
