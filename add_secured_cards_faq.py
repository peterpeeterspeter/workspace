#!/usr/bin/env python3
"""
Add FAQ Schema to Secured Credit Cards page
"""

import requests
import json

AUTH = ("admin", "GyOC qXGg K82P hxRt ZjbY 2v9k")

# FAQ Schema for Secured Credit Cards page
FAQ_SCHEMA = {
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

def update_page_schema(page_id, schema_data):
    """Update page schema via WordPress REST API"""
    url = f"https://cardfair.com/wp-json/wp/v2/pages/{page_id}"

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
                "page_id": page_id,
                "schema_type": schema_data.get("@type", "Unknown")
            }
        else:
            return {
                "success": False,
                "page_id": page_id,
                "error": f"HTTP {response.status_code}: {response.text[:200]}"
            }
    except Exception as e:
        return {
            "success": False,
            "page_id": page_id,
            "error": str(e)
        }

print("="*80)
print("📋 ADDING FAQ SCHEMA TO SECURED CREDIT CARDS PAGE")
print("="*80)
print()

print("Updating page 1345 (Secured Credit Cards)...")

result = update_page_schema(1345, FAQ_SCHEMA)

if result["success"]:
    print("✅ SUCCESS - FAQ Schema added!")
    print(f"   Page ID: {result['page_id']}")
    print(f"   Schema Type: {result['schema_type']}")
else:
    print(f"❌ FAILED: {result['error']}")

print()
print("="*80)
print("🎯 BENEFITS:")
print("  - FAQ dropdown in Google search results")
print("  - Higher CTR from SERP")
print("  - Better E-E-A-T signals")
print("  - More real estate in search results")
print("="*80)

# Save result
with open('/root/.openclaw/workspace/secured_cards_faq_results.json', 'w') as f:
    json.dump(result, f, indent=2)
