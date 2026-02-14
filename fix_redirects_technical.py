#!/usr/bin/env python3
"""
Fix redirects via WordPress Custom Permalinks plugin
Alternative approach if redirect plugins don't work
"""

import requests
import json

AUTH = ("admin", "GyOC qXGg K82P hxRt ZjbY 2v9k")

# Redirects to implement
REDIRECTS = [
    {
        "source": "/shortcodes/",
        "target": "/secured-credit-cards/",
        "type": "301"
    },
    {
        "source": "/typography/",
        "target": "/credit-cards/",
        "type": "301"
    },
    {
        "source": "/blog-classic-2-columns/",
        "target": "/all-posts/",
        "type": "301"
    },
    {
        "source": "/blog-classic-3-columns/",
        "target": "/all-posts/",
        "type": "301"
    }
]

def test_redirect(source_path):
    """Test if a redirect exists"""
    url = f"https://www.cardfair.com{source_path}"
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        final_url = response.url
        status = response.status_code

        # Check if it redirects to the right place
        if response.history:
            # There was a redirect
            return {
                "working": True,
                "status": status,
                "final_url": final_url,
                "redirects": len(response.history)
            }
        else:
            # No redirect - 404 or direct
            return {
                "working": status == 200,
                "status": status,
                "final_url": final_url,
                "redirects": 0
            }
    except Exception as e:
        return {
            "working": False,
            "error": str(e)
        }

def try_wordpress_redirect_method():
    """Try different WordPress redirect methods"""

    print("="*80)
    print("🔧 TESTING WORDPRESS REDIRECT METHODS")
    print("="*80)
    print()

    # Method 1: Check for redirect plugins
    print("1️⃣ Checking for redirect plugins...")
    print("-"*80)

    plugins_to_check = [
        "redirection/redirection.php",
        "safe-redirect-manager/safe-redirect-manager.php",
        "wordpress-seo/wp-seo.php",  # Yoast has redirect manager
    ]

    url = "https://cardfair.com/wp-json/wp/v2/plugins"
    try:
        response = requests.get(url, auth=AUTH, timeout=5)
        if response.status_code == 200:
            print("   ✅ Can access plugins API")
        else:
            print(f"   ⚠️ Plugins API returned: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    print()

    # Method 2: Check posts for any existing redirects
    print("2️⃣ Checking for existing redirect posts...")
    print("-"*80)

    url = "https://cardfair.com/wp-json/wp/v2/posts?per_page=100&_fields=slug,link,status"
    try:
        response = requests.get(url, auth=AUTH, timeout=5)
        if response.status_code == 200:
            posts = response.json()
            print(f"   ✅ Found {len(posts)} posts")

            # Check if any match our broken URLs
            broken_slugs = ["shortcodes", "typography", "blog-classic-2-columns", "blog-classic-3-columns"]
            for post in posts:
                if post.get('slug') in broken_slugs:
                    print(f"   ⚠️ Found matching post: {post['slug']} ({post.get('status', 'unknown')})")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    print()

    # Method 3: Try .htaccess via WordPress file system (if available)
    print("3️⃣ Checking .htaccess access...")
    print("-"*80)

    try:
        # Check if we can access .htaccess
        url = "https://cardfair.com/.htaccess"
        response = requests.head(url, timeout=5)

        if response.status_code == 403 or response.status_code == 404:
            print("   ⚠️ .htaccess not directly accessible (expected - security)")
            print("   💡 Use FTP/File Manager or cPanel to edit")
        elif response.status_code == 200:
            print("   ⚠️ .htaccess is publicly accessible (security risk!)")
    except Exception as e:
        print(f"   ℹ️ .htaccess check: {str(e)[:50]}")

    print()

    # Method 4: Test current redirect status
    print("4️⃣ Testing current redirect status...")
    print("-"*80)

    for redirect in REDIRECTS:
        source = redirect['source']
        result = test_redirect(source)

        if result.get('working'):
            if result.get('redirects', 0) > 0:
                print(f"   ✅ {source} → {result['final_url']}")
            else:
                print(f"   ⚠️ {source} → {result['status']} (no redirect)")
        else:
            print(f"   ❌ {source} → {result.get('error', 'Failed')}")

    print()

    print("="*80)
    print("📋 RECOMMENDED SOLUTION")
    print("="*80)
    print()
    print("Since WordPress API redirects failed earlier, here are your options:")
    print()
    print("OPTION 1: Edit .htaccess (Recommended, 2 min)")
    print("─────────────────────────────────────────────")
    print("1. Access server via:")
    print("   - cPanel → File Manager")
    print("   - FTP/SFTP client")
    print("   - WordPress hosting panel")
    print()
    print("2. Download .htaccess file")
    print("3. Append redirect rules (ready in: htaccess_redirects.txt)")
    print("4. Re-upload .htaccess")
    print()
    print("OPTION 2: Use Redirection Plugin")
    print("─────────────────────────────────────")
    print("1. Install: Redirection (free, 2+ million installs)")
    print("2. Go to: Tools → Redirection")
    print("3. Add 301 redirects manually:")
    for r in REDIRECTS:
        print(f"   - {r['source']} → {r['target']}")
    print()
    print("OPTION 3: Custom Permalinks Plugin")
    print("─────────────────────────────────────")
    print("1. Install: Custom Permalinks plugin")
    print("2. Add redirect rules via plugin interface")
    print()
    print("OPTION 4: Let me try via FTP automation")
    print("─────────────────────────────────────")
    print("Provide FTP credentials and I'll upload .htaccess automatically")
    print()

if __name__ == "__main__":
    try_wordpress_redirect_method()

    print("="*80)
    print("📁 READY-TO-USE FILES")
    print("="*80)
    print()
    print("• htaccess_redirects.txt - Copy-paste ready redirect rules")
    print("• Just append to existing .htaccess file")
    print()
