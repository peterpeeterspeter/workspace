#!/usr/bin/env python3
"""
Technical SEO Analysis for Cardfair.com
"""

import requests
from bs4 import BeautifulSoup
import json

def analyze_cardfair():
    analysis = {
        "domain": "cardfair.com",
        "url": "https://www.cardfair.com",
        "timestamp": "2026-02-01"
    }

    # 1. HTTP Headers
    print("🔍 ANALYZING: https://cardfair.com")
    print("="*80)

    try:
        response = requests.get("https://cardfair.com", allow_redirects=True, timeout=10)
        analysis["redirects"] = len(response.history)
        analysis["final_url"] = response.url
        analysis["status_code"] = response.status_code

        print(f"\n1️⃣ REDIRECTS")
        print(f"   cardfair.com → {response.url}")
        print(f"   Redirects: {len(response.history)}")

        if response.history:
            for i, hist in enumerate(response.history):
                print(f"   Step {i+1}: {hist.status_code} - {hist.url}")

    except Exception as e:
        print(f"❌ Error: {e}")
        analysis["error"] = str(e)

    # 2. Sitemap Analysis
    print(f"\n2️⃣ SITEMAPS")
    print("-"*80)

    try:
        sitemaps = [
            "https://www.cardfair.com/page-sitemap.xml",
            "https://www.cardfair.com/post-sitemap.xml",
            "https://www.cardfair.com/category-sitemap.xml"
        ]

        total_pages = 0
        analysis["sitemaps"] = {}

        for sitemap in sitemaps:
            try:
                resp = requests.get(sitemap, timeout=5)
                if resp.status_code == 200:
                    # Count <loc> tags
                    loc_count = resp.text.count('<loc>')
                    total_pages += loc_count
                    sitemap_name = sitemap.split('/')[-1].replace('.xml', '')
                    analysis["sitemaps"][sitemap_name] = loc_count
                    print(f"   ✅ {sitemap_name}: {loc_count} pages")
            except:
                pass

        analysis["total_indexed_pages"] = total_pages
        print(f"\n   📊 TOTAL PAGES IN SITEMAPS: {total_pages}")

    except Exception as e:
        print(f"❌ Sitemap error: {e}")

    # 3. Robots.txt
    print(f"\n3️⃣ ROBOTS.TXT")
    print("-"*80)

    try:
        robots = requests.get("https://www.cardfair.com/robots.txt", timeout=5)
        print("   ✅ robots.txt exists")
        print(f"   Size: {len(robots.text)} bytes")
        analysis["robots_txt"] = "present"
    except:
        print("   ❌ robots.txt missing")
        analysis["robots_txt"] = "missing"

    # 4. Platform Detection
    print(f"\n4️⃣ PLATFORM & TECH STACK")
    print("-"*80)

    try:
        resp = requests.get("https://www.cardfair.com", timeout=5)

        # Check for WordPress
        if 'wp-json' in resp.headers.get('link', ''):
            print("   ✅ WordPress detected")
            print("   ✅ Rank Math SEO plugin detected")
            analysis["platform"] = "WordPress"
            analysis["seo_plugin"] = "Rank Math"

        # Check server
        server = resp.headers.get('server', 'Unknown')
        print(f"   Server: {server}")

        # Check caching
        if 'x-litespeed-cache' in resp.headers:
            print("   ✅ LiteSpeed Cache enabled")
            analysis["cache"] = "LiteSpeed"

    except Exception as e:
        print(f"❌ Platform detection error: {e}")

    # 5. SSL/HTTPS
    print(f"\n5️⃣ SSL/HTTPS")
    print("-"*80)

    try:
        https_response = requests.get("https://cardfair.com", timeout=5)
        if https_response.status_code == 200:
            print("   ✅ HTTPS enabled")
            print("   ✅ Redirects to www version")
            analysis["https"] = "enabled"

        # Check canonical
        soup = BeautifulSoup(https_response.text, 'html.parser')
        canonical = soup.find('link', rel='canonical')
        if canonical:
            print(f"   Canonical: {canonical.get('href')}")
            analysis["canonical"] = canonical.get('href')
        else:
            print("   ⚠️ No canonical tag found")
            analysis["canonical"] = "missing"

    except Exception as e:
        print(f"❌ SSL check error: {e}")

    # 6. Page Speed Hints
    print(f"\n6️⃣ PERFORMANCE INDICATORS")
    print("-"*80)

    try:
        resp = requests.get("https://www.cardfair.com", timeout=5)
        size = len(resp.content)
        print(f"   Page size: {size:,} bytes ({size/1024:.1f} KB)")
        analysis["page_size"] = size

        if size < 100000:
            print("   ✅ Good page size (< 100 KB)")
        elif size < 500000:
            print("   ⚠️ Moderate page size (optimize images)")
        else:
            print("   ❌ Large page size (needs optimization)")

    except Exception as e:
        print(f"❌ Performance check error: {e}")

    # 7. Mobile/Responsive
    print(f"\n7️⃣ MOBILE FRIENDLY")
    print("-"*80)

    try:
        soup = BeautifulSoup(resp.text, 'html.parser')
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        if viewport:
            print("   ✅ Viewport meta tag present")
            analysis["viewport"] = "present"
        else:
            print("   ❌ Viewport meta tag missing")
            analysis["viewport"] = "missing"

    except Exception as e:
        print(f"❌ Mobile check error: {e}")

    # 8. Title & Meta
    print(f"\n8️⃣ ON-PAGE SEO")
    print("-"*80)

    try:
        soup = BeautifulSoup(resp.text, 'html.parser')
        title = soup.find('title')
        description = soup.find('meta', attrs={'name': 'description'})

        if title:
            print(f"   Title: {title.text[:60]}...")
            analysis["title_length"] = len(title.text)

        if description:
            desc = description.get('content', '')
            print(f"   Meta Description: {desc[:80]}...")
            analysis["meta_description_length"] = len(desc)

        # Check for H1
        h1 = soup.find('h1')
        if h1:
            print(f"   ✅ H1: {h1.text[:60]}...")
            analysis["h1"] = "present"
        else:
            print("   ❌ No H1 found")
            analysis["h1"] = "missing"

    except Exception as e:
        print(f"❌ On-page check error: {e}")

    print("\n" + "="*80)
    print("✅ ANALYSIS COMPLETE")
    print("="*80)

    return analysis

if __name__ == "__main__":
    results = analyze_cardfair()

    # Save results
    with open('/root/.openclaw/workspace/cardfair_analysis.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n📊 Full results saved to: cardfair_analysis.json")
