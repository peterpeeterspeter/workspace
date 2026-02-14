#!/usr/bin/env python3
"""
Fix Schema Markup for Cardfair.com
Update with correct page URLs
"""

import requests
import json

AUTH = ("admin", "GyOC qXGg K82P hxRt ZjbY 2v9k")

# Schema markup with correct URLs
SCHEMA_UPDATES = {
    "https://www.cardfair.com/2025/11/16/rebuild-credit-after-bankruptcy/": {
        "schema": {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": "How long does it take to rebuild credit after bankruptcy?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "Rebuilding credit after bankruptcy typically takes 12-24 months. You can see improvement within 6-12 months with responsible credit use, but a Chapter 7 bankruptcy stays on your report for 10 years, Chapter 13 for 7 years."
                    }
                },
                {
                    "@type": "Question",
                    "name": "Can I get a credit card after bankruptcy?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "Yes, you can get a secured credit card immediately after bankruptcy. Many secured cards approve people with past bankruptcies. After 12-24 months of responsible use, you may qualify for unsecured cards."
                    }
                },
                {
                    "@type": "Question",
                    "name": "What's the fastest way to rebuild credit after bankruptcy?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "The fastest way is to: 1) Get a secured credit card, 2) Make on-time payments 100% of the time, 3) Keep credit utilization below 30%, 4) Become an authorized user on someone else's card, 5) Use credit-builder tools like Experian Boost."
                    }
                },
                {
                    "@type": "Question",
                    "name": "Should I pay off all debt after bankruptcy?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "Not necessarily. Focus on debts that survived bankruptcy and secured debts. Build an emergency fund first, then systematically rebuild credit using a mix of credit types (secured card, credit builder loan)."
                    }
                }
            ]
        }
    },
    "https://www.cardfair.com/secured-credit-cards/": {
        "schema": {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": "What is a secured credit card?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "A secured credit card requires a cash deposit that becomes your credit limit. It's designed for people with bad credit or no credit history to build or rebuild their credit score."
                    }
                },
                {
                    "@type": "Question",
                    "name": "How do secured credit cards help rebuild credit?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "Secured cards report to all three credit bureaus. By making on-time payments and keeping balances low, you demonstrate responsible credit behavior, which gradually improves your credit score."
                    }
                },
                {
                    "@type": "Question",
                    "name": "What credit score do I need for a secured card?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "Most secured credit cards approve people with credit scores below 600, and many have no credit check. They're specifically designed for people with bad credit or limited credit history."
                    }
                },
                {
                    "@type": "Question",
                    "name": "How much is the deposit for a secured card?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "Secured card deposits typically range from $200 to $3,000, depending on the card. Your credit limit usually equals your deposit amount."
                    }
                },
                {
                    "@type": "Question",
                    "name": "When can I upgrade from a secured to unsecured card?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "Most secured card issuers allow upgrades after 6-18 months of on-time payments. Some automatically review your account, others require you to apply. When you upgrade, you'll get your deposit back."
                    }
                }
            ]
        }
    }
}

def get_page_id_by_slug(slug):
    """Get page ID by slug via WordPress API"""
    url = f"https://cardfair.com/wp-json/wp/v2/pages?slug={slug}"
    try:
        response = requests.get(url, auth=AUTH, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                return data[0]['id']
    except Exception as e:
        print(f"Error fetching page ID for {slug}: {e}")
    return None

def get_post_id_by_path(path):
    """Get post ID by path via WordPress API"""
    # Extract slug from path
    slug = path.strip('/').split('/')[-1]
    url = f"https://cardfair.com/wp-json/wp/v2/posts?slug={slug}"
    try:
        response = requests.get(url, auth=AUTH, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                return data[0]['id']
    except Exception as e:
        print(f"Error fetching post ID for {slug}: {e}")
    return None

def update_rankmath_schema(post_id, schema_data):
    """Update RankMath schema via WordPress meta"""
    url = f"https://cardfair.com/wp-json/wp/v2/posts/{post_id}"

    payload = {
        "meta": {
            "rank_math_schema": json.dumps(schema_data)
        }
    }

    try:
        response = requests.post(url, auth=AUTH, json=payload, timeout=10)

        if response.status_code == 200:
            return {
                "success": True,
                "post_id": post_id,
                "schema_type": schema_data.get("@type", "Unknown")
            }
        else:
            return {
                "success": False,
                "post_id": post_id,
                "error": f"HTTP {response.status_code}: {response.text[:200]}"
            }
    except Exception as e:
        return {
            "success": False,
            "post_id": post_id,
            "error": str(e)
        }

def main():
    print("="*80)
    print("📋 FIXING SCHEMA MARKUP FOR CARDFAIR.COM")
    print("="*80)
    print()

    results = []

    for url, schema_data in SCHEMA_UPDATES.items():
        schema_type = schema_data["schema"]["@type"]

        # Get post ID
        if "/2025/" in url:
            # It's a post
            post_id = get_post_id_by_path(url)
            content_type = "post"
        else:
            # It's a page
            slug = url.strip('/').split('/')[-1]
            post_id = get_page_id_by_slug(slug)
            content_type = "page"

        if not post_id:
            print(f"❌ Could not find {content_type} for: {url}")
            results.append({
                "success": False,
                "url": url,
                "error": "Could not find post/page ID"
            })
            continue

        print(f"Adding {schema_type} schema to {content_type} {post_id}...")

        result = update_rankmath_schema(post_id, schema_data["schema"])
        result["url"] = url
        results.append(result)

        if result["success"]:
            print(f"  ✅ SUCCESS")
        else:
            print(f"  ❌ FAILED: {result.get('error')}")

        print()

    print("="*80)
    success_count = sum(1 for r in results if r["success"])
    print(f"✅ Successfully updated: {success_count}/{len(results)} schema markups")
    print("="*80)

    # Save results
    with open('/root/.openclaw/workspace/schema_fix_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("\n📊 Results saved to: schema_fix_results.json")

    # Summary
    print("\n📋 SCHEMA UPDATED:")
    print("-"*80)
    for r in results:
        if r["success"]:
            print(f"✅ {r.get('url', 'Unknown')}: {r['schema_type']}")
        else:
            print(f"❌ {r.get('url', 'Unknown')}: {r.get('error', 'Unknown')}")

if __name__ == "__main__":
    main()
