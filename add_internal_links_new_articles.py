#!/usr/bin/env python3
"""
Add Internal Links to New Articles
"""

import requests
import json

AUTH = ("admin", "GyOC qXGg K82P hxRt ZjbY 2v9k")

# Internal links to add
INTERNAL_LINKS_MAP = {
    "best-secured-credit-cards-for-rebuilding-credit-the-complete-2026-guide": {
        "links": [
            {"anchor": "600-650 FICO score", "url": "https://www.cardfair.com/best-credit-cards-for-a-600-650-fico-score-in-2026/"},
            {"anchor": "secured vs unsecured cards", "url": "https://www.cardfair.com/secured-vs-unsecured-cards-best-for-580-669-scores/"},
            {"anchor": "rebuild credit after bankruptcy", "url": "https://www.cardfair.com/rebuild-credit-after-bankruptcy/"}
        ]
    },
    "best-credit-cards-for-a-600-650-fico-score-in-2026": {
        "links": [
            {"anchor": "secured credit cards", "url": "https://www.cardfair.com/best-secured-credit-cards-for-rebuilding-credit-the-complete-2026-guide/"},
            {"anchor": "graduating from fair to prime credit", "url": "https://www.cardfair.com/how-to-graduate-from-fair-to-prime-credit-in-12-months/"}
        ]
    },
    "secured-vs-unsecured-cards-best-for-580-669-scores": {
        "links": [
            {"anchor": "best secured credit cards", "url": "https://www.cardfair.com/best-secured-credit-cards-for-rebuilding-credit-the-complete-2026-guide/"},
            {"anchor": "600-650 FICO score options", "url": "https://www.cardfair.com/best-credit-cards-for-a-600-650-fico-score-in-2026/"}
        ]
    },
    "how-to-graduate-from-fair-to-prime-credit-in-12-months": {
        "links": [
            {"anchor": "600-650 credit score cards", "url": "https://www.cardfair.com/best-credit-cards-for-a-600-650-fico-score-in-2026/"},
            {"anchor": "factors that improve credit score", "url": "https://www.cardfair.com/10-proven-factors-that-move-a-600-credit-score-to-700-expert-guide/"}
        ]
    },
    "cash-back-vs-low-apr-best-fair-credit-strategies-for-2026": {
        "links": [
            {"anchor": "cards for 600-650 FICO score", "url": "https://www.cardfair.com/best-credit-cards-for-a-600-650-fico-score-in-2026/"},
            {"anchor": "credit building strategies", "url": "https://www.cardfair.com/how-to-graduate-from-fair-to-prime-credit-in-12-months/"}
        ]
    }
}

def get_post_id(slug):
    """Get post ID from slug"""
    url = f"https://cardfair.com/wp-json/wp/v2/posts?slug={slug}"
    try:
        resp = requests.get(url, auth=AUTH, timeout=10)
        if resp.status_code == 200:
            posts = resp.json()
            if posts and len(posts) > 0:
                return posts[0]['id']
    except:
        pass
    return None

def get_post_content(post_id):
    """Get post content"""
    url = f"https://cardfair.com/wp-json/wp/v2/posts/{post_id}"
    try:
        resp = requests.get(url, auth=AUTH, timeout=10)
        if resp.status_code == 200:
            return resp.json()
    except:
        pass
    return None

def add_internal_links(slug, links):
    """Add internal links to post"""
    post_id = get_post_id(slug)
    if not post_id:
        return {"success": False, "error": "Post not found"}
    
    post_data = get_post_content(post_id)
    if not post_data:
        return {"success": False, "error": "Could not fetch post"}
    
    content = post_data.get('content', {}).get('rendered', '')
    title = post_data.get('title', {}).get('rendered', '')
    
    # Add links to content
    updated_content = content
    links_added = 0
    
    for link_data in links:
        anchor = link_data['anchor']
        url = link_data['url']
        
        # Create link HTML
        link_html = f'<a href="{url}">{anchor}</a>'
        
        # Add link if anchor text exists in content
        if anchor.lower() in content.lower():
            # Simple replacement (you may want more sophisticated logic)
            updated_content = updated_content.replace(anchor, link_html, 1)
            links_added += 1
    
    if links_added > 0:
        # Update post
        update_url = f"https://cardfair.com/wp-json/wp/v2/posts/{post_id}"
        payload = {"content": updated_content}
        
        try:
            resp = requests.post(update_url, auth=AUTH, json=payload, timeout=10)
            if resp.status_code == 200:
                return {"success": True, "title": title, "links_added": links_added}
            else:
                return {"success": False, "error": f"HTTP {resp.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    else:
        return {"success": False, "error": "No matching anchor text found"}

def main():
    print("="*80)
    print("🔗 ADDING INTERNAL LINKS TO NEW ARTICLES")
    print("="*80)
    print()
    
    results = []
    
    for slug, data in INTERNAL_LINKS_MAP.items():
        print(f"Processing: {slug}")
        result = add_internal_links(slug, data['links'])
        results.append(result)
        
        if result["success"]:
            print(f"  ✅ Added {result['links_added']} links - {result['title']}")
        else:
            print(f"  ⚠️ {result.get('error')}")
        print()
    
    print("="*80)
    success_count = sum(1 for r in results if r["success"])
    print(f"✅ Internal links added to {success_count}/{len(results)} articles")
    print("="*80)
    
    print("\n📊 Benefits:")
    print("  • Better site structure")
    print("  • Improved crawlability")
    print("  • Link equity distribution")
    print("  • User navigation improvement")
    
    # Save results
    with open('/root/.openclaw/workspace/internal_links_new_articles.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n📁 Results saved: internal_links_new_articles.json")

if __name__ == "__main__":
    main()
