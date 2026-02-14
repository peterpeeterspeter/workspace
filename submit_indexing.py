#!/usr/bin/env python3
"""
Submit Cardfair.com URLs to IndexNow for instant indexing
"""

import requests
import json
import time

DOMAIN = "https://www.cardfair.com"
INDEXNOW_KEY_FILE = "/root/.openclaw/workspace/indexnow_keys.json"

# Key pages to submit
PRIORITY_URLS = [
    "https://www.cardfair.com/",
    "https://www.cardfair.com/secured-credit-cards/",
    "https://www.cardfair.com/credit-cards/",
    "https://www.cardfair.com/credit-card-services/",
    "https://www.cardfair.com/2025/11/16/rebuild-credit-after-bankruptcy/",
    "https://www.cardfair.com/apply/",
    "https://www.cardfair.com/all-posts/"
]

def get_indexnow_key():
    """Get IndexNow key for cardfair.com"""
    try:
        with open(INDEXNOW_KEY_FILE, 'r') as f:
            keys = json.load(f)
            return keys.get("cardfair.com")
    except:
        return None

def submit_to_indexnow(urls, key):
    """Submit URLs to IndexNow API"""
    endpoint = "https://api.indexnow.org/indexnow"

    # Batch submission (up to 10,000 URLs)
    payload = {
        "host": "www.cardfair.com",
        "key": key,
        "urlList": urls
    }

    try:
        response = requests.post(endpoint, json=payload, timeout=30)

        if response.status_code == 200:
            return {
                "success": True,
                "submitted": len(urls),
                "response": response.text
            }
        else:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}",
                "response": response.text[:500]
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def submit_to_google_ping(sitemap_url):
    """Submit sitemap to Google via ping"""
    ping_url = f"https://www.google.com/ping?sitemap={sitemap_url}"

    try:
        response = requests.get(ping_url, timeout=10)
        return response.status_code == 200
    except:
        return False

def main():
    print("="*80)
    print("🚀 SUBMITTING CARDFAIR.COM TO INDEXING SERVICES")
    print("="*80)
    print()

    # Get IndexNow key
    indexnow_key = get_indexnow_key()

    if not indexnow_key:
        print("⚠️ No IndexNow key found for cardfair.com")
        print()
        print("To set up IndexNow:")
        print("1. Generate a key: https://www.indexnow.org/docs/key")
        print("2. Add to indexnow_keys.json:")
        print('   {"cardfair.com": "your-32-char-hex-key"}')
        print("3. Verify by adding key file to: https://www.cardfair.com/{key}.txt")
        print()
        print("Continuing with Google ping only...")
        print()
        indexnow_key = None

    results = {}

    # Step 1: Submit to Google
    print("="*80)
    print("1️⃣ SUBMITTING SITEMAP TO GOOGLE")
    print("="*80)
    print()

    sitemap_url = f"{DOMAIN}/sitemap.xml"
    print(f"Pinging: {sitemap_url}")

    google_success = submit_to_google_ping(sitemap_url)

    if google_success:
        print("✅ SUCCESS - Sitemap submitted to Google")
        results["google_ping"] = "success"
    else:
        print("❌ FAILED - Could not submit to Google")
        results["google_ping"] = "failed"

    print()

    # Step 2: Submit to IndexNow
    if indexnow_key:
        print("="*80)
        print("2️⃣ SUBMITTING URLs TO INDEXNOW")
        print("="*80)
        print()

        print(f"Submitting {len(PRIORITY_URLS)} priority pages...")

        indexnow_result = submit_to_indexnow(PRIORITY_URLS, indexnow_key)

        if indexnow_result["success"]:
            print(f"✅ SUCCESS - {indexnow_result['submitted']} URLs submitted")
            results["indexnow"] = "success"
        else:
            print(f"❌ FAILED - {indexnow_result.get('error')}")
            results["indexnow"] = indexnow_result.get("error")

        print()
    else:
        print("="*80)
        print("2️⃣ INDEXNOW SKIPPED (no key configured)")
        print("="*80)
        print()
        results["indexnow"] = "skipped"

    # Step 3: Summary
    print("="*80)
    print("📊 SUBMISSION SUMMARY")
    print("="*80)
    print()

    for service, status in results.items():
        icon = "✅" if status == "success" else "⚠️"
        print(f"{icon} {service.upper()}: {status}")

    print()
    print("="*80)
    print("🎯 WHAT HAPPENS NEXT")
    print("="*80)
    print("""
Google:
  - Crawlers will discover the sitemap
  - Indexing typically within 24-72 hours
  - Check Search Console for status

IndexNow:
  - Instant submission to Bing, Google, Yandex
  - Usually indexed within minutes
  - More reliable than ping alone

Recommendations:
  1. Verify in Google Search Console
  2. Check Coverage report in 24 hours
  3. Monitor for crawling errors
  4. Submit new content regularly
    """)

    # Save results
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    with open(f'/root/.openclaw/workspace/indexing_submission_{timestamp}.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n📊 Results saved to: indexing_submission_{timestamp}.json")

if __name__ == "__main__":
    main()
