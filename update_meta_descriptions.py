#!/usr/bin/env python3
"""
SEO Meta Description Generator for Cardfair.com
Generates optimized meta descriptions for WordPress pages
"""

import requests
import json

# WordPress REST API credentials
WP_URL = "https://cardfair.com/wp-json/wp/v2"
AUTH = ("admin", "GyOC qXGg K82P hxRt ZjbY 2v9k")

# Page data with SEO-optimized meta descriptions
PAGES_TO_UPDATE = {
    260: {  # Home
        "title": "Cardfair | Honest Credit Card Reviews & Comparisons",
        "meta_description": "Compare fair credit card offers with transparent rates, no hidden fees, and expert reviews. Find the best credit cards for bad credit, secured cards, and rebuild your score today.",
        "yoast_meta": {
            "focuskw": "fair credit cards",
            "title": "Cardfair | Honest Credit Card Reviews & Comparisons",
            "metadesc": "Compare fair credit card offers with transparent rates, no hidden fees, and expert reviews. Find the best credit cards for bad credit, secured cards, and rebuild your score today."
        }
    },
    205: {  # Credit Cards
        "title": "Credit Cards - Compare Fair Credit Card Offers | Cardfair",
        "meta_description": "Discover fair credit card offers for every credit level. Compare rates, fees, and rewards. Get approved for credit cards that work for you, not against you.",
        "yoast_meta": {
            "focuskw": "credit card offers",
            "title": "Credit Cards - Compare Fair Credit Card Offers | Cardfair",
            "metadesc": "Discover fair credit card offers for every credit level. Compare rates, fees, and rewards. Get approved for credit cards that work for you."
        }
    },
    1345: {  # Secured Credit Cards
        "title": "Secured Credit Cards for Bad Credit | Rebuild Your Score | Cardfair",
        "meta_description": "Get approved for secured credit cards even with bad credit. Build credit history with fair terms, low fees, and transparent rates. Start rebuilding today.",
        "yoast_meta": {
            "focuskw": "secured credit cards bad credit",
            "title": "Secured Credit Cards for Bad Credit | Rebuild Your Score | Cardfair",
            "metadesc": "Get approved for secured credit cards even with bad credit. Build credit history with fair terms, low fees, and transparent rates."
        }
    },
    217: {  # Our Services
        "title": "Credit Card Services | Expert Guidance & Tools | Cardfair",
        "meta_description": "Free credit card comparison tools, expert guidance, and personalized recommendations. Find the right credit card based on your credit score and financial goals.",
        "yoast_meta": {
            "focuskw": "credit card services",
            "title": "Credit Card Services | Expert Guidance & Tools | Cardfair",
            "metadesc": "Free credit card comparison tools, expert guidance, and personalized recommendations. Find the right card based on your credit score and goals."
        }
    },
    764: {  # Apply Now
        "title": "Apply for Fair Credit Cards | Get Approved Today | Cardfair",
        "meta_description": "Apply for fair credit cards with high approval rates. Quick online application, instant decision for some cards. Start your journey to better credit now.",
        "yoast_meta": {
            "focuskw": "apply for credit cards",
            "title": "Apply for Fair Credit Cards | Get Approved Today | Cardfair",
            "metadesc": "Apply for fair credit cards with high approval rates. Quick online application, instant decisions. Start your journey to better credit."
        }
    },
    179: {  # Credit Rewards
        "title": "Credit Card Rewards Programs | Maximize Your Benefits | Cardfair",
        "meta_description": "Compare credit card rewards programs. Earn cashback, points, and miles on every purchase. Find rewards cards that match your spending habits.",
        "yoast_meta": {
            "focuskw": "credit card rewards",
            "title": "Credit Card Rewards Programs | Maximize Your Benefits | Cardfair",
            "metadesc": "Compare credit card rewards programs. Earn cashback, points, and miles on every purchase. Find rewards cards that match your spending."
        }
    }
}

def update_page_meta(page_id, meta_data):
    """Update page meta description via WordPress REST API"""
    url = f"{WP_URL}/pages/{page_id}"

    # Prepare update payload
    payload = {
        "title": meta_data["title"],
        "excerpt": meta_data["meta_description"],
        "meta": meta_data.get("yoast_meta", {})
    }

    try:
        response = requests.post(url, auth=AUTH, json=payload, timeout=10)

        if response.status_code == 200:
            return {
                "success": True,
                "page_id": page_id,
                "title": meta_data["title"][:50] + "..."
            }
        else:
            return {
                "success": False,
                "page_id": page_id,
                "error": f"HTTP {response.status_code}"
            }
    except Exception as e:
        return {
            "success": False,
            "page_id": page_id,
            "error": str(e)
        }

def main():
    print("="*80)
    print("🚀 UPDATING META DESCRIPTIONS FOR CARDFAIR.COM")
    print("="*80)
    print()

    results = []

    for page_id, meta_data in PAGES_TO_UPDATE.items():
        print(f"Updating page {page_id}...")

        result = update_page_meta(page_id, meta_data)
        results.append(result)

        if result["success"]:
            print(f"  ✅ {result['title']}")
        else:
            print(f"  ❌ ERROR: {result.get('error')}")

        print()

    print("="*80)
    success_count = sum(1 for r in results if r["success"])
    print(f"✅ Successfully updated: {success_count}/{len(results)} pages")
    print("="*80)

    # Save results
    with open('/root/.openclaw/workspace/meta_update_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("\n📊 Results saved to: meta_update_results.json")

if __name__ == "__main__":
    main()
