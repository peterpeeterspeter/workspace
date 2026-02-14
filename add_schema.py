#!/usr/bin/env python3
"""
Add Schema Markup to Cardfair.com via WordPress REST API
Adds Organization and FAQ schema to key pages
"""

import requests
import json

AUTH = ("admin", "GyOC qXGg K82P hxRt ZjbY 2v9k")

# Schema markup for key pages
SCHEMA_PAGES = {
    260: {  # Homepage - Organization Schema
        "schema": {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": "Cardfair",
            "url": "https://www.cardfair.com/",
            "logo": "https://www.cardfair.com/logo.png",
            "description": "Fair credit card reviews, comparisons, and expert guidance. Compare transparent credit card offers with no hidden fees.",
            "sameAs": [],
            "contactPoint": {
                "@type": "ContactPoint",
                "contactType": "customer service",
                "url": "https://www.cardfair.com/contacts/"
            }
        }
    },
    1345: {  # Secured Credit Cards - FAQ Schema
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
                }
            ]
        }
    },
    1334: {  # Bankruptcy Timeline - FAQ Schema
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
                }
            ]
        }
    }
}

def add_schema_to_page(page_id, schema_data):
    """Add schema markup to page via WordPress meta"""
    url = f"https://cardfair.com/wp-json/wp/v2/pages/{page_id}"

    # Convert schema to JSON-LD
    schema_jsonld = f'\n<script type="application/ld+json">\n{json.dumps(schema_data, indent=2)}\n</script>\n'

    # Get current page content
    get_response = requests.get(url, auth=AUTH, timeout=10)
    if get_response.status_code != 200:
        return {"success": False, "page_id": page_id, "error": "Failed to fetch page"}

    page_data = get_response.json()
    current_content = page_data.get('content', {}).get('rendered', '')

    # Add schema to content
    updated_content = current_content + schema_jsonld

    # Update page
    payload = {
        "content": updated_content,
        "meta": {
            "rank_math_schema": json.dumps(schema_data)
        }
    }

    try:
        response = requests.post(url, auth=AUTH, json=payload, timeout=10)

        if response.status_code == 200:
            return {
                "success": True,
                "page_id": page_id,
                "schema_type": schema_data.get("@type", "Unknown")
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
    print("📋 ADDING SCHEMA MARKUP TO CARDFAIR.COM")
    print("="*80)
    print()

    results = []

    for page_id, schema_data in SCHEMA_PAGES.items():
        schema_type = schema_data["schema"]["@type"]
        print(f"Adding {schema_type} schema to page {page_id}...")

        result = add_schema_to_page(page_id, schema_data["schema"])
        results.append(result)

        if result["success"]:
            print(f"  ✅ SUCCESS")
        else:
            print(f"  ❌ FAILED: {result.get('error')}")

        print()

    print("="*80)
    success_count = sum(1 for r in results if r["success"])
    print(f"✅ Successfully added: {success_count}/{len(results)} schema markups")
    print("="*80)

    # Save results
    with open('/root/.openclaw/workspace/schema_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("\n📊 Results saved to: schema_results.json")

    # Summary
    print("\n📋 SCHEMA ADDED:")
    print("-"*80)
    for r in results:
        if r["success"]:
            print(f"✅ Page {r['page_id']}: {r['schema_type']}")

    print("\n🎯 BENEFITS:")
    print("  - Rich snippets in Google search results")
    print("  - FAQ dropdown in SERPs")
    print("  - Better CTR (click-through rate)")
    print("  - Improved E-E-A-T signals")

if __name__ == "__main__":
    main()
