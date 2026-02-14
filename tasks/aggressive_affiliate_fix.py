#!/usr/bin/env python3
"""
AGGRESSIVE AFFILIATE LINK REPLACEMENT
Replace ALL wrong affiliate domains with Peter's correct links
"""

import json
import subprocess
import re

# Mapping: wrong domain → correct affiliate URL
DOMAIN_REPLACEMENTS = {
    'stake.com': 'https://cybetplay.com/tluy6cbpp',
    'bc.game': 'https://cybetplay.com/tluy6cbpp',
    'thunderpick.com': 'https://cybetplay.com/tluy6cbpp',
    'roobet.com': 'https://cybetplay.com/tluy6cbpp',
    'metaspins.com': 'https://cybetplay.com/tluy6cbpp',
    'bitstarz.com': 'https://bzstarz1.com/b196c322b',
    '7bitcasino.com': 'https://7bit.partners/p4i4w1udu'
}

def replace_all_affiliate_domains(content):
    """Replace ALL occurrences of wrong domains with correct affiliate URLs"""
    updated = content
    
    for wrong_domain, correct_url in DOMAIN_REPLACEMENTS.items():
        # Match the domain with or without www, http, or https
        # This pattern will match:
        # - https://stake.com/crash
        # - http://www.stake.com/crash
        # - stake.com/crash
        # - www.stake.com/crash
        pattern = re.compile(
            r'\(?\s?(?:https?:)?//(?:www\.)?' + re.escape(wrong_domain) + r'[^\s\)"<>]*\)?',
            re.IGNORECASE
        )
        updated = pattern.sub(correct_url, updated)
    
    return updated

def fix_post_aggressive(site_url, site_user, site_pass, post_id):
    """Fix a single post with aggressive replacement"""
    try:
        # Fetch post
        curl_cmd = [
            'curl', '-s',
            '-u', f"{site_user}:{site_pass}",
            f"{site_url}/wp/v2/posts/{post_id}?_fields=id,title,content"
        ]
        
        result = subprocess.run(curl_cmd, capture_output=True, text=True, check=True)
        post = json.loads(result.stdout)
        
        content = post.get('content', {}).get('rendered', '')
        title = post.get('title', {}).get('rendered', '')
        
        if not content:
            return False, "No content"
        
        # Count wrong domains before
        wrong_count = sum(1 for domain in DOMAIN_REPLACEMENTS if domain in content.lower())
        
        # Apply aggressive replacement
        fixed_content = replace_all_affiliate_domains(content)
        
        # Count wrong domains after
        wrong_count_after = sum(1 for domain in DOMAIN_REPLACEMENTS if domain in fixed_content.lower())
        
        if content == fixed_content:
            return False, "No changes"
        
        # Update post
        payload = {"content": fixed_content}
        
        update_cmd = [
            'curl', '-s', '-X', 'POST',
            f"{site_url}/wp/v2/posts/{post_id}",
            '-u', f"{site_user}:{site_pass}",
            '-H', 'Content-Type: application/json',
            '-d', json.dumps(payload)
        ]
        
        update_result = subprocess.run(update_cmd, capture_output=True, text=True)
        
        try:
            response = json.loads(update_result.stdout)
        except:
            return False, f"Error: {update_result.stdout[:200]}"
        
        if 'code' in response:
            return False, response.get('message', 'Unknown error')
        
        return True, f"Fixed {wrong_count - wrong_count_after} domains"
        
    except Exception as e:
        return False, str(e)

# Fix crashcasino.io posts that still have wrong affiliate links
problem_posts = [838, 837, 835, 834, 783, 786]

print("="*70)
print("AGGRESSIVE AFFILIATE LINK REPLACEMENT")
print("="*70)
print("\nReplacing ALL wrong domains with YOUR correct affiliate links\n")

for post_id in problem_posts:
    success, message = fix_post_aggressive(
        "https://crashcasino.io/wp-json",
        "peter",
        "3vRhtTs2khfdLtTiDFqkdeXI",
        post_id
    )
    
    status = "✅" if success else ("⚠️" if "No changes" in message else "❌")
    print(f"{status} Post {post_id}: {message}")

print("\n" + "="*70)
print("Done! All wrong affiliate domains should now be replaced")
print("="*70)
