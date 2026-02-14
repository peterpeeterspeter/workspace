#!/usr/bin/env python3
"""
Update Rank Math SEO Meta via WordPress REST API
Uses the meta field to update Rank Math data
"""

import requests
import json

WP_URL = "https://cardfair.com/wp-json/wp/v2"
AUTH = ("admin", "GyOC qXGg K82P hxRt ZjbY 2v9k")

# Rank Math meta data structure
RANK_MATH_PAGES = {
    260: {  # Homepage
        "rankmath_title": "Cardfair | Honest Credit Card Reviews & Comparisons",
        "rankmath_description": "Compare fair credit card offers with transparent rates, no hidden fees, and expert reviews. Find the best credit cards for bad credit, secured cards, and rebuild your score today.",
        "rankmath_focus_keyword": "fair credit cards",
        "rankmath_canonical_url": "https://www.cardfair.com/",
        "rankmath_robots": ["index", "follow"]
    },
    205: {  # Credit Cards
        "rankmath_title": "Credit Cards - Compare Fair Credit Card Offers | Cardfair",
        "rankmath_description": "Discover fair credit card offers for every credit level. Compare rates, fees, and rewards. Get approved for credit cards that work for you, not against you.",
        "rankmath_focus_keyword": "credit card offers",
        "rankmath_canonical_url": "https://www.cardfair.com/credit-cards/",
        "rankmath_robots": ["index", "follow"]
    },
    1345: {  # Secured Credit Cards
        "rankmath_title": "Secured Credit Cards for Bad Credit | Rebuild Your Score | Cardfair",
        "rankmath_description": "Get approved for secured credit cards even with bad credit. Build credit history with fair terms, low fees, and transparent rates. Start rebuilding today.",
        "rankmath_focus_keyword": "secured credit cards bad credit",
        "rankmath_canonical_url": "https://www.cardfair.com/secured-credit-cards/",
        "rankmath_robots": ["index", "follow"]
    },
    217: {  # Our Services
        "rankmath_title": "Credit Card Services | Expert Guidance & Tools | Cardfair",
        "rankmath_description": "Free credit card comparison tools, expert guidance, and personalized recommendations. Find the right credit card based on your credit score and financial goals.",
        "rankmath_focus_keyword": "credit card services",
        "rankmath_canonical_url": "https://www.cardfair.com/our-services/",
        "rankmath_robots": ["index", "follow"]
    },
    764: {  # Apply Now
        "rankmath_title": "Apply for Fair Credit Cards | Get Approved Today | Cardfair",
        "rankmath_description": "Apply for fair credit cards with high approval rates. Quick online application, instant decision for some cards. Start your journey to better credit now.",
        "rankmath_focus_keyword": "apply for credit cards",
        "rankmath_canonical_url": "https://www.cardfair.com/apply-now/",
        "rankmath_robots": ["index", "follow"]
    },
    179: {  # Credit Rewards
        "rankmath_title": "Credit Card Rewards Programs | Maximize Your Benefits | Cardfair",
        "rankmath_description": "Compare credit card rewards programs. Earn cashback, points, and miles on every purchase. Find rewards cards that match your spending habits.",
        "rankmath_focus_keyword": "credit card rewards",
        "rankmath_canonical_url": "https://www.cardfair.com/credit-rewards/",
        "rankmath_robots": ["index", "follow"]
    }
}

def update_rankmath_meta(page_id, meta_data):
    """Update Rank Math meta via WordPress REST API"""
    url = f"{WP_URL}/pages/{page_id}"

    # Build meta payload for Rank Math
    payload = {
        "title": meta_data.get("rankmath_title", ""),
        "excerpt": meta_data.get("rankmath_description", ""),
        "meta": {
            "rankmath_title": meta_data.get("rankmath_title", ""),
            "rankmath_description": meta_data.get("rankmath_description", ""),
            "rankmath_focus_keyword": meta_data.get("rankmath_focus_keyword", ""),
            "rankmath_canonical_url": meta_data.get("rankmath_canonical_url", ""),
            "rankmath_robots": meta_data.get("rankmath_robots", ["index", "follow"]),
            "rankmath_advanced_robots": {
                "index": True,
                "follow": True
            }
        }
    }

    try:
        response = requests.post(url, auth=AUTH, json=payload, timeout=10)

        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "page_id": page_id,
                "title": meta_data.get("rankmath_title", "")[:50] + "...",
                "focuskw": meta_data.get("rankmath_focus_keyword", "")
            }
        else:
            return {
                "success": False,
                "page_id": page_id,
                "error": f"HTTP {response.status_code}: {response.text[:100]}"
            }
    except Exception as e:
        return {
            "success": False,
            "page_id": page_id,
            "error": str(e)
        }

def main():
    print("="*80)
    print("🔧 UPDATING RANK MATH SEO META FOR CARDFAIR.COM")
    print("="*80)
    print()

    results = []

    for page_id, meta_data in RANK_MATH_PAGES.items():
        print(f"Updating page {page_id}...")
        print(f"  Focus keyword: {meta_data.get('rankmath_focus_keyword')}")

        result = update_rankmath_meta(page_id, meta_data)
        results.append(result)

        if result["success"]:
            print(f"  ✅ SUCCESS")
        else:
            print(f"  ❌ ERROR: {result.get('error')}")

        print()

    print("="*80)
    success_count = sum(1 for r in results if r["success"])
    print(f"✅ Successfully updated: {success_count}/{len(results)} pages via Rank Math")
    print("="*80)

    # Save results
    with open('/root/.openclaw/workspace/rankmath_update_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("\n📊 Results saved to: rankmath_update_results.json")

    # Show summary
    print("\n📋 SUMMARY:")
    print("-"*80)
    for r in results:
        if r["success"]:
            print(f"✅ Page {r['page_id']}: {r['title']}")
            print(f"   Focus: {r.get('focuskw', 'N/A')}")

if __name__ == "__main__":
    main()
