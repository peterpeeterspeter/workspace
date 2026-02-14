#!/usr/bin/env python3
"""
IMPROVED BULK FIX: More comprehensive metadata removal
"""

import json
import subprocess
import re

# Peter's CORRECT affiliate links
CORRECT_AFFILIATES = {
    'cybet': 'https://cybetplay.com/tluy6cbpp',
    'bitstarz': 'https://bzstarz1.com/b196c322b',
    'betzrd': 'https://betzrd.com/pyondmfcx',
    '7bit': 'https://7bit.partners/p4i4w1udu',
    '7bit casino': 'https://7bit.partners/p4i4w1udu',
    'mirax': 'https://mirax.partners/p4fp2iusj',
    'mirax casino': 'https://mirax.partners/p4fp2iusj',
    'trustdice': 'https://trustdice.win/?ref=u_peterp',
    '1xpartners': 'https://reffpa.com/L?tag=d_4381452m_97c_&site=4381452&ad=97',
    '1xbet': 'https://reffpa.com/L?tag=d_4381452m_97c_&site=4381452&ad=97',
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

def remove_metadata_comprehensive(content):
    """Remove ALL metadata sections that show as visible text"""
    
    # Remove structured JSON schemas
    content = re.sub(
        r'\{ "@context": "[^"]+".*?\}\s*\n',
        '',
        content,
        flags=re.DOTALL
    )
    
    # Remove metadata section headers
    content = re.sub(
        r'Internal Links:.*?(?=\n\n|\Z)',
        '',
        content,
        flags=re.DOTALL
    )
    
    content = re.sub(
        r'External Authority Links:.*?(?=\n\n|\Z)',
        '',
        content,
        flags=re.DOTALL
    )
    
    content = re.sub(
        r'Responsible Gambling Resources:.*?(?=\n\n|\Z)',
        '',
        content,
        flags=re.DOTALL
    )
    
    content = re.sub(
        r'Read More.*?(?=\n\n|\Z)',
        '',
        content,
        flags=re.DOTALL
    )
    
    # Remove individual metadata labels
    content = re.sub(r'^Meta Description.*?\n', '', content, flags=re.MULTILINE)
    content = re.sub(r'^Article Schema:.*?\n', '', content, flags=re.MULTILINE)
    content = re.sub(r'^FAQPage Schema:.*?\n', '', content, flags=re.MULTILINE)
    content = re.sub(r'^Bottom Line.*?(?=\n\n|\Z)', '', content, flags=re.MULTILINE|re.DOTALL)
    content = re.sub(r'^@context.*?\n', '', content, flags=re.MULTILINE)
    content = re.sub(r'^@type.*?\n', '', content, flags=re.MULTILINE)
    content = re.sub(r'^datePublished.*?\n', '', content, flags=re.MULTILINE)
    
    # Clean up multiple blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    return content.strip()

def replace_affiliate_links(content):
    """Replace wrong affiliate links with correct ones"""
    updated_content = content
    
    for wrong_domain, correct_url in WRONG_DOMAINS.items():
        # Match various URL formats
        pattern = re.compile(
            r'https?://(?:www\.)?' + re.escape(wrong_domain) + r'[^\s\]"<>]*',
            re.IGNORECASE
        )
        updated_content = pattern.sub(correct_url, updated_content)
    
    return updated_content

def fix_post(site_url, site_user, site_pass, post_id):
    """Fix a single post"""
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
        
        # Apply fixes
        fixed_content = remove_metadata_comprehensive(content)
        fixed_content = replace_affiliate_links(fixed_content)
        
        # Check if changes were made
        if content == fixed_content:
            return False, "No changes needed"
        
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
            # Non-JSON response (probably HTML error)
            return False, f"Error: {update_result.stdout[:200]}"
        
        if 'code' in response:
            return False, response.get('message', 'Unknown error')
        
        return True, "Fixed"
        
    except Exception as e:
        return False, str(e)

def process_site(site_name, site_url, site_user, site_pass, post_ids):
    """Process all posts for a site"""
    print(f"\n{'='*70}")
    print(f"PROCESSING: {site_name}")
    print(f"{'='*70}\n")
    
    fixed = 0
    errors = 0
    
    for i, post_id in enumerate(post_ids[:50], 1):  # Limit to 50 at a time
        success, message = fix_post(site_url, site_user, site_pass, post_id)
        
        if success:
            print(f"  [{i}] ✅ Post {post_id} fixed")
            fixed += 1
        elif "No changes needed" in message:
            print(f"  [{i}] ✓ Post {post_id} clean")
        else:
            print(f"  [{i}] ❌ Post {post_id}: {message}")
            errors += 1
    
    print(f"\n{site_name}: {fixed} fixed, {errors} errors")
    return fixed, errors

# Main execution
if __name__ == '__main__':
    print("="*70)
    print("BULK FIX v2 - Comprehensive Metadata Removal")
    print("="*70)
    
    # Process crashcasino.io (specific posts that need fixing)
    crashcasino_ids = [838, 837, 836, 835, 834, 833, 817, 816, 787, 786, 785, 784, 783, 779, 776]
    
    process_site(
        "crashcasino.io",
        "https://crashcasino.io/wp-json",
        "peter",
        "3vRhtTs2khfdLtTiDFqkdeXI",
        crashcasino_ids
    )
    
    print("\n" + "="*70)
    print("✅ First batch complete!")
    print("="*70)
    print("\nTo fix remaining sites, run this script again with:")
    print("  • crashgamegambling.com")
    print("  • freecrashgames.com")
    print("  • cryptocrashgambling.com")
