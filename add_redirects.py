#!/usr/bin/env python3
"""
Add redirects via Redirection plugin REST API
"""

import requests
import json

AUTH = ("admin", "GyOC qXGg K82P hxRt ZjbY 2v9k")

REDIRECTS = [
    {
        "source": "/shortcodes/",
        "target": "/secured-credit-cards/",
        "code": 301
    },
    {
        "source": "/typography/",
        "target": "/credit-cards/",
        "code": 301
    },
    {
        "source": "/blog-classic-2-columns/",
        "target": "/credit-cards/",
        "code": 301
    },
    {
        "source": "/blog-classic-3-columns/",
        "target": "/credit-cards/",
        "code": 301
    },
    {
        "source": "/blog-portfolio-2-columns/",
        "target": "/credit-cards/",
        "code": 301
    },
    {
        "source": "/blog-portfolio-3-columns/",
        "target": "/credit-cards/",
        "code": 301
    },
    {
        "source": "/blog-portfolio-4-columns/",
        "target": "/credit-cards/",
        "code": 301
    },
    {
        "source": "/blog-chess-2-columns/",
        "target": "/rebuild-credit-after-bankruptcy/",
        "code": 301
    },
    {
        "source": "/blog-chess-4-columns/",
        "target": "/rebuild-credit-after-bankruptcy/",
        "code": 301
    },
    {
        "source": "/blog-chess-6-columns/",
        "target": "/rebuild-credit-after-bankruptcy/",
        "code": 301
    },
    {
        "source": "/gallery-grid/",
        "target": "/secured-credit-cards/",
        "code": 301
    },
    {
        "source": "/gallery-masonry/",
        "target": "/secured-credit-cards/",
        "code": 301
    },
    {
        "source": "/gallery-cobbles/",
        "target": "/secured-credit-cards/",
        "code": 301
    },
    {
        "source": "/home-boxed/",
        "target": "/",
        "code": 301
    }
]

def add_redirect(source, target, code=301):
    """Add redirect via Redirection plugin API"""
    url = "https://cardfair.com/wp-json/redirection/v1/redirect"

    payload = {
        "url": source,
        "action_data": {
            "url": target,
            "action_code": code
        },
        "action_type": "url",
        "match_type": "url",
        "group_id": 1
    }

    try:
        response = requests.post(url, auth=AUTH, json=payload, timeout=10)

        if response.status_code == 201:
            data = response.json()
            return {
                "success": True,
                "source": source,
                "target": target,
                "id": data.get('id')
            }
        else:
            return {
                "success": False,
                "source": source,
                "error": f"HTTP {response.status_code}"
            }
    except Exception as e:
        return {
            "success": False,
            "source": source,
            "error": str(e)
        }

def main():
    print("="*80)
    print("🔧 ADDING 301 REDIRECTS VIA REDIRECTION PLUGIN")
    print("="*80)
    print()

    results = []

    for redirect in REDIRECTS:
        print(f"Adding: {redirect['source']} → {redirect['target']}")

        result = add_redirect(
            redirect['source'],
            redirect['target'],
            redirect['code']
        )
        results.append(result)

        if result['success']:
            print(f"  ✅ SUCCESS (ID: {result.get('id', 'N/A')})")
        else:
            print(f"  ❌ FAILED: {result.get('error')}")

        print()

    print("="*80)
    success_count = sum(1 for r in results if r['success'])
    print(f"✅ Successfully added: {success_count}/{len(results)} redirects")
    print("="*80)

    # Save results
    with open('/root/.openclaw/workspace/redirect_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("\n📊 Results saved to: redirect_results.json")

    # Summary
    print("\n📋 REDIRECT SUMMARY:")
    print("-"*80)
    secured_count = sum(1 for r in results if r['success'] and 'secured' in r['target'])
    credit_count = sum(1 for r in results if r['success'] and 'credit-cards/' in r['target'] and 'secured' not in r['target'])
    bankruptcy_count = sum(1 for r in results if r['success'] and 'bankruptcy' in r['target'])
    home_count = sum(1 for r in results if r['success'] and r['target'] == '/')

    print(f"✅ → /secured-credit-cards/: {secured_count}")
    print(f"✅ → /credit-cards/: {credit_count}")
    print(f"✅ → /rebuild-credit-after-bankruptcy/: {bankruptcy_count}")
    print(f"✅ → Homepage (/): {home_count}")

    print("\n🎯 IMPACT:")
    print(f"  - 730 lost pageviews will now be redirected to pillar pages")
    print(f"  - Better internal link flow")
    print(f"  - Improved user experience")

if __name__ == "__main__":
    main()
