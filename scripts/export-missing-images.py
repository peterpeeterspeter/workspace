#!/usr/bin/env python3
"""
Export posts missing featured images to JSON for batch processing
"""

import json
import requests
import urllib.parse

# Site credentials
SITES = {
    'crashcasino': {
        'url': 'https://crashcasino.io/wp-json',
        'auth': ('peter', '3vRhtTs2khfdLtTiDFqkdeXI'),
        'domain': 'crashcasino.io'
    },
    'crashgame': {
        'url': 'https://crashgamegambling.com/wp-json',
        'auth': ('@peter', 'MioX SygN Xaz6 pK9o RUiK tBMF'),
        'domain': 'crashgamegambling.com'
    },
    'freecrash': {
        'url': 'https://freecrashgames.com/wp-json',
        'auth': ('@peter', 'F8Mg yZXM qJy4 jQvp BMeZ FoMG'),
        'domain': 'freecrashgames.com'
    },
    'cryptocrash': {
        'url': 'https://cryptocrashgambling.com/wp-json',
        'auth': ('@peter', 'R3kQ 6vRA UwYd x7Cn KEtT Pk83'),
        'domain': 'cryptocrashgambling.com'
    }
}

def clean_title(title):
    """Strip HTML tags and truncate"""
    import re
    clean = re.sub('<[^<]+?>', '', title)
    clean = clean.strip()
    return clean[:100]

def generate_prompt(title, site):
    """Generate image prompt based on title keywords"""
    
    # Base prompt
    base = "Professional gambling illustration, crash game multiplier rocket, casino chips, modern sleek design, 1200x630"
    
    title_lower = title.lower()
    
    # Customize based on content
    if any(kw in title_lower for kw in ['rigged', 'fairness', 'verify', 'scam', 'legit']):
        return f"{base}, trust badges, security symbols, blue and white color scheme, professional"
    elif any(kw in title_lower for kw in ['bonus', 'codes', 'free', 'promo', 'offer']):
        return f"{base}, bonus coins, gift boxes, gold and green accents, celebration"
    elif any(kw in title_lower for kw in ['strategy', 'cashout', 'mistakes', 'win', 'profit']):
        return f"{base}, charts, upward trends, profit symbols, professional business style"
    elif any(kw in title_lower for kw in ['bitcoin', 'crypto', 'no-kyc', 'anonymous', 'vpn']):
        return f"{base}, bitcoin symbols, blockchain network, purple and gold theme, futuristic"
    elif any(kw in title_lower for kw in ['india', 'chinese', 'german', 'global']):
        return f"{base}, multicultural elements, globe, diverse players, inclusive"
    else:
        return f"{base}, casino gaming aesthetic, high quality"

def get_missing_images(site_key):
    """Get posts without featured images for a site"""
    site = SITES[site_key]
    
    # Fetch posts
    response = requests.get(
        f"{site['url']}/wp/v2/posts",
        params={'per_page': 100, '_fields': 'id,title,link,featured_media'},
        auth=site['auth']
    )
    
    if response.status_code != 200:
        print(f"Error fetching {site_key}: {response.status_code}")
        return []
    
    posts = response.json()
    
    # Filter posts without featured images
    missing = []
    for post in posts:
        if not post.get('featured_media') or post.get('featured_media') == 0:
            title = clean_title(post['title']['rendered'])
            
            missing.append({
                'site': site_key,
                'domain': site['domain'],
                'post_id': post['id'],
                'title': title,
                'url': post['link'],
                'prompt': generate_prompt(title, site_key),
                'alt_text': f"Featured image for article: {title}",
                'filename': f"{site_key}_{post['id']}.png"
            })
    
    return missing

def main():
    all_missing = []
    
    print("🔍 Scanning for posts without featured images...\n")
    
    # Check each site
    for site_key in SITES.keys():
        print(f"Checking {site_key}...", end=" ")
        missing = get_missing_images(site_key)
        print(f"Found {len(missing)} posts")
        all_missing.extend(missing)
    
    # Export to JSON
    output_file = '/root/.openclaw/workspace/temp/missing-images.json'
    with open(output_file, 'w') as f:
        json.dump(all_missing, f, indent=2)
    
    print(f"\n✅ Exported {len(all_missing)} posts to: {output_file}")
    
    # Print summary
    print("\n📊 Summary by site:")
    for site_key in SITES.keys():
        count = len([p for p in all_missing if p['site'] == site_key])
        print(f"  {site_key}: {count} posts")
    
    # Show sample
    print("\n📝 Sample entry:")
    if all_missing:
        sample = all_missing[0]
        print(json.dumps(sample, indent=2))
    
    print("\n🚀 Next steps:")
    print("1. Choose image API: DALL-E 3 (recommended) or Stability AI")
    print("2. Set API key: export OPENAI_API_KEY='your-key'")
    print("3. Run generator: ./generate-images-from-json.py")

if __name__ == '__main__':
    main()
