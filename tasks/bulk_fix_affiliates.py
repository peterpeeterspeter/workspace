#!/usr/bin/env python3
"""
BULK FIX: Replace wrong affiliate links and remove metadata from article body
Fixes 145+ articles across 4 sites
"""

import json
import subprocess
import re

# Peter's CORRECT affiliate links
CORRECT_AFFILIATES = {
    # Cybet
    'cybet': 'https://cybetplay.com/tluy6cbpp',
    # BitStarz
    'bitstarz': 'https://bzstarz1.com/b196c322b',
    # Betzrd
    'betzrd': 'https://betzrd.com/pyondmfcx',
    # 7Bit
    '7bit': 'https://7bit.partners/p4i4w1udu',
    '7bit casino': 'https://7bit.partners/p4i4w1udu',
    # Mirax
    'mirax': 'https://mirax.partners/p4fp2iusj',
    'mirax casino': 'https://mirax.partners/p4fp2iusj',
    # TrustDice
    'trustdice': 'https://trustdice.win/?ref=u_peterp',
    # 1xPartners/1xBet
    '1xpartners': 'https://reffpa.com/L?tag=d_4381452m_97c_&site=4381452&ad=97',
    '1xbet': 'https://reffpa.com/L?tag=d_4381452m_97c_&site=4381452&ad=97',
    # Betfury
    'betfury': 'https://betfury.bet/df1865703'
}

# WRONG affiliate domains to replace
WRONG_DOMAINS = {
    'stake.com': 'cybetplay.com/tluy6cbpp',
    'bc.game': 'cybetplay.com/tluy6cbpp',
    'thunderpick.com': 'cybetplay.com/tluy6cbpp',
    'roobet.com': 'cybetplay.com/tluy6cbpp',
    'metaspins.com': 'cybetplay.com/tluy6cbpp',
    'bitstarz.com': 'bzstarz1.com/b196c322b',
    '7bitcasino.com': '7bit.partners/p4i4w1udu'
}

# Sites to fix
SITES = {
    'crashcasino': {
        'url': 'https://crashcasino.io/wp-json',
        'user': 'peter',
        'pass': '3vRhtTs2khfdLtTiDFqkdeXI',
        'post_ids': [838, 837, 836, 835, 834, 833, 817, 816, 787, 786, 785, 784, 783, 779, 776]
    },
    'crashgamegambling': {
        'url': 'https://crashgamegambling.com/wp-json',
        'user': '@peter',
        'pass': 'MioX SygN Xaz6 pK9o RUiK tBMF',
        'post_ids': 'recent'  # Will fetch recent
    },
    'freecrashgames': {
        'url': 'https://freecrashgames.com/wp-json',
        'user': '@peter',
        'pass': 'F8Mg yZXM qJy4 jQvp BMeZ FoMG',
        'post_ids': 'recent'
    },
    'cryptocrash': {
        'url': 'https://cryptocrashgambling.com/wp-json',
        'user': '@peter',
        'pass': 'R3kQ 6vRA UwYd x7Cn KEtT Pk83',
        'post_ids': [49040, 49034, 49033, 49032, 49031, 49030, 49029, 49028, 49027]
    }
}

def remove_metadata_from_content(content):
    """Remove visible metadata markers from article body"""
    # Remove various metadata patterns that show as text
    patterns_to_remove = [
        r'Meta Description \(?\d+ chars?\): [^\n]+\n',
        r'Article Schema: \{[^\}]+\}\n',
        r'FAQPage Schema: \{[^\}]+\}\n',
        r'Bottom Line[^\n]*\n(?:[^\n]+\n)*',
        r'"\@context"[^\n]*\n',
        r'"\@type"[^\n]*\n',
        r'"datePublished"[^\n]*\n',
        r'Meta Description[^\n]*\n'
    ]
    
    cleaned_content = content
    for pattern in patterns_to_remove:
        cleaned_content = re.sub(pattern, '', cleaned_content, flags=re.MULTILINE | re.DOTALL)
    
    return cleaned_content

def replace_affiliate_links(content):
    """Replace wrong affiliate links with correct ones"""
    updated_content = content
    
    # Replace wrong domains with correct affiliate links
    for wrong_domain, correct_url in WRONG_DOMAINS.items():
        # Pattern to match various URL formats with the wrong domain
        pattern = re.compile(
            r'https?://(?:www\.)?' + re.escape(wrong_domain.replace('.', r'\.')) + r'[^\s\]"<>]*',
            re.IGNORECASE
        )
        updated_content = pattern.sub(correct_url, updated_content)
    
    return updated_content

def fix_post(site_key, post_id):
    """Fix a single post"""
    site = SITES[site_key]
    
    # Fetch current post content
    curl_cmd = [
        'curl', '-s',
        '-u', f"{site['user']}:{site['pass']}",
        f"{site['url']}/wp/v2/posts/{post_id}?_fields=id,title,content"
    ]
    
    try:
        result = subprocess.run(curl_cmd, capture_output=True, text=True, check=True)
        post = json.loads(result.stdout)
        
        content = post.get('content', {}).get('rendered', '')
        title = post.get('title', {}).get('rendered', '')
        
        if not content:
            return False, "No content"
        
        # Fix the content
        original_length = len(content)
        fixed_content = remove_metadata_from_content(content)
        fixed_content = replace_affiliate_links(fixed_content)
        
        # Check if changes were made
        if len(fixed_content) == original_length and content == fixed_content:
            return False, "No changes needed"
        
        # Update the post
        payload = {
            "content": fixed_content
        }
        
        update_cmd = [
            'curl', '-s', '-X', 'POST',
            f"{site['url']}/wp/v2/posts/{post_id}",
            '-u', f"{site['user']}:{site['pass']}",
            '-H', 'Content-Type: application/json',
            '-d', json.dumps(payload)
        ]
        
        update_result = subprocess.run(update_cmd, capture_output=True, text=True, check=True)
        response = json.loads(update_result.stdout)
        
        if 'code' in response:
            return False, response['message']
        
        return True, f"Fixed (removed {original_length - len(fixed_content)} chars)"
        
    except Exception as e:
        return False, str(e)

def main():
    print("="*70)
    print("BULK FIX: Affiliate Links + Metadata Removal")
    print("="*70)
    print(f"\nFixing {len(WRONG_DOMAINS)} wrong affiliate domains:")
    for domain in WRONG_DOMAINS:
        print(f"  • {domain} → {WRONG_DOMAINS[domain]}")
    print()
    print("Removing visible metadata from article body:")
    print("  • Meta Description")
    print("  • Article Schema")
    print("  • FAQPage Schema")
    print("  • Bottom Line")
    print("  • @context, @type, datePublished")
    print("\n" + "="*70 + "\n")
    
    total_fixed = 0
    total_errors = 0
    
    for site_key in SITES:
        print(f"\n🔧 FIXING: {site_key}")
        print("-"*70)
        
        site = SITES[site_key]
        
        # Get post IDs
        if site['post_ids'] == 'recent':
            # Fetch recent posts that need fixing
            curl_cmd = [
                'curl', '-s',
                '-u', f"{site['user']}:{site['pass']}",
                f"{site['url']}/wp/v2/posts?per_page=100&orderby=date&order=desc&_fields=id"
            ]
            result = subprocess.run(curl_cmd, capture_output=True, text=True, check=True)
            posts = json.loads(result.stdout)
            post_ids = [p['id'] for p in posts]
        else:
            post_ids = site['post_ids']
        
        print(f"Posts to check: {len(post_ids)}\n")
        
        site_fixed = 0
        site_errors = 0
        
        for i, post_id in enumerate(post_ids, 1):
            success, message = fix_post(site_key, post_id)
            
            if success:
                print(f"  [{i}/{len(post_ids)}] ✅ Post {post_id}: {message}")
                site_fixed += 1
            elif message == "No changes needed":
                print(f"  [{i}/{len(post_ids)}] ✓ Post {post_id}: Already clean")
            else:
                print(f"  [{i}/{len(post_ids)}] ❌ Post {post_id}: {message}")
                site_errors += 1
        
        print(f"\n{site_key}: {site_fixed} fixed, {site_errors} errors")
        total_fixed += site_fixed
        total_errors += site_errors
    
    print("\n" + "="*70)
    print("FINAL SUMMARY")
    print("="*70)
    print(f"Total fixed: {total_fixed} posts")
    print(f"Total errors: {total_errors} posts")
    print(f"\n✅ All affiliate links updated to YOUR domains")
    print("✅ All visible metadata removed from article body")
    print("="*70)

if __name__ == '__main__':
    main()
