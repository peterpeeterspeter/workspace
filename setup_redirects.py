#!/usr/bin/env python3
"""
Add 301 redirects via WordPress Redirection plugin or .htaccess
Using WordPress REST API to add redirects
"""

import requests
import json

AUTH = ("admin", "GyOC qXGg K82P hxRt ZjbY 2v9k")

# Redirects to add
REDIRECTS = [
    {
        "source": "/shortcodes/",
        "target": "/secured-credit-cards/",
        "type": 301
    },
    {
        "source": "/typography/",
        "target": "/credit-cards/",
        "type": 301
    },
    {
        "source": "/blog-classic-2-columns/",
        "target": "/credit-cards/",
        "type": 301
    },
    {
        "source": "/blog-classic-3-columns/",
        "target": "/credit-cards/",
        "type": 301
    },
    {
        "source": "/blog-portfolio-2-columns/",
        "target": "/credit-cards/",
        "type": 301
    },
    {
        "source": "/blog-portfolio-3-columns/",
        "target": "/credit-cards/",
        "type": 301
    },
    {
        "source": "/blog-portfolio-4-columns/",
        "target": "/credit-cards/",
        "type": 301
    },
    {
        "source": "/blog-chess-2-columns/",
        "target": "/rebuild-credit-after-bankruptcy/",
        "type": 301
    },
    {
        "source": "/blog-chess-4-columns/",
        "target": "/rebuild-credit-after-bankruptcy/",
        "type": 301
    },
    {
        "source": "/blog-chess-6-columns/",
        "target": "/rebuild-credit-after-bankruptcy/",
        "type": 301
    },
    {
        "source": "/gallery-grid/",
        "target": "/secured-credit-cards/",
        "type": 301
    },
    {
        "source": "/gallery-masonry/",
        "target": "/secured-credit-cards/",
        "type": 301
    },
    {
        "source": "/gallery-cobbles/",
        "target": "/secured-credit-cards/",
        "type": 301
    },
    {
        "source": "/home-boxed/",
        "target": "/",
        "type": 301
    }
]

def create_redirect_redirector_plugin():
    """
    Check if Redirection plugin is installed and add redirects
    """
    # Check if Redirection plugin REST API is available
    try:
        response = requests.get(
            "https://cardfair.com/wp-json/redirection/v1/redirect",
            auth=AUTH,
            timeout=5
        )

        if response.status_code == 200:
            return "redirection_plugin"
    except:
        pass

    return "htaccess"

def add_redirect_via_htaccess(redirect_data):
    """
    Add redirects via .htaccess file
    This creates a WordPress snippet to add
    """
    redirect_rules = """
# BEGIN Cardfair Demo Page Redirects
RewriteEngine On
"""

    for r in redirect_data:
        redirect_rules += f"RewriteRule ^{r['source'].lstrip('/')}$ {r['target']} [R={r['type']},L]\n"

    redirect_rules += "# END Cardfair Demo Page Redirects\n"

    return redirect_rules

def add_redirect_via_plugin(source, target, code=301):
    """
    Add redirect via Redirection plugin REST API
    """
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
        return {
            "success": response.status_code == 201,
            "source": source,
            "target": target,
            "status": response.status_code
        }
    except Exception as e:
        return {
            "success": False,
            "source": source,
            "error": str(e)
        }

def main():
    print("="*80)
    print("🔧 SETTING UP 301 REDIRECTS FOR CARDFAIR.COM")
    print("="*80)
    print()

    # Check which method to use
    method = create_redirect_redirector_plugin()

    if method == "redirection_plugin":
        print("✅ Redirection plugin detected - adding redirects via API")
        print("-"*80)
        print()

        results = []
        for redirect in REDIRECTS:
            print(f"Adding: {redirect['source']} → {redirect['target']}")

            result = add_redirect_via_plugin(
                redirect['source'],
                redirect['target'],
                redirect['type']
            )
            results.append(result)

            if result['success']:
                print(f"  ✅ SUCCESS")
            else:
                print(f"  ❌ FAILED: {result.get('error', result.get('status'))}")

            print()

        success_count = sum(1 for r in results if r['success'])
        print("="*80)
        print(f"✅ Successfully added: {success_count}/{len(results)} redirects")

    else:
        print("⚠️ Redirection plugin not found - generating .htaccess rules")
        print("-"*80)
        print()

        htaccess_content = add_redirect_via_htaccess(REDIRECTS)

        print("Add this to your .htaccess file:\n")
        print(htaccess_content)

        # Save to file
        with open('/root/.openclaw/workspace/htaccess_redirects.txt', 'w') as f:
            f.write(htaccess_content)

        print("="*80)
        print("✅ Rules saved to: htaccess_redirects.txt")
        print("\n📋 NEXT STEPS:")
        print("1. Access your site via FTP or cPanel")
        print("2. Edit .htaccess file in root directory")
        print("3. Paste the redirect rules")
        print("4. Save and test")

    print()
    print("="*80)
    print("📊 REDIRECT SUMMARY")
    print("="*80)
    print(f"Total redirects to add: {len(REDIRECTS)}")
    print(f"→ /secured-credit-cards/: {sum(1 for r in REDIRECTS if 'secured' in r['target'])}")
    print(f"→ /credit-cards/: {sum(1 for r in REDIRECTS if 'credit-cards/' in r['target'] and 'secured' not in r['target'])}")
    print(f"→ /rebuild-credit-after-bankruptcy/: {sum(1 for r in REDIRECTS if 'bankruptcy' in r['target'])}")
    print(f"→ Homepage (/): {sum(1 for r in REDIRECTS if r['target'] == '/')}")

if __name__ == "__main__":
    main()
