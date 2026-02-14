#!/usr/bin/env python3
"""
Deep scan for broken HTML/affiliate issues across all posts
"""

import json
import subprocess
import re

SITES = {
    'freecrashgames': {
        'url': 'https://freecrashgames.com/wp-json',
        'user': '@peter',
        'pass': 'F8Mg yZXM qJy4 jQvp BMeZ FoMG'
    },
    'cryptocrash': {
        'url': 'https://cryptocrashgambling.com/wp-json',
        'user': '@peter',
        'pass': 'R3kQ 6vRA UwYd x7Cn KEtT Pk83'
    }
}

AFFILIATE_DOMAINS = [
    'cybetplay.com',
    'bzstarz1.com', 
    'betzrd.com',
    '7bit.partners',
    'mirax.partners',
    'trustdice.win',
    'reffpa.com',
    'betfury.bet'
]

def check_post_deep(post_id, site):
    """Deep check a single post for issues"""
    site_config = SITES[site]
    
    curl_command = [
        'curl', '-s',
        '-u', f"{site_config['user']}:{site_config['pass']}",
        f"{site_config['url']}/wp/v2/posts/{post_id}?_fields=id,title,content,date"
    ]
    
    try:
        result = subprocess.run(curl_command, capture_output=True, text=True, check=True)
        post = json.loads(result.stdout)
        content = post.get('content', {}).get('rendered', '')
        
        issues = []
        
        # Check for raw markdown in content
        markdown_patterns = [
            (r'\[([^\]]+)\]\([^\)]+\)', 'Raw markdown link'),
            (r'\*\*[^*]+\*\*', 'Raw markdown bold'),
            (r'(?<!\*)\*(?!\*)([^*]+)\*(?!\*)', 'Raw markdown italic'),
            (r'^\|.*\|$', 'Raw markdown table row', True),
            (r'^[\|\- :]+$', 'Raw markdown table separator', True),
        ]
        
        lines = content.split('\n')
        for i, line in enumerate(lines):
            for pattern, desc, *multiline in markdown_patterns:
                flags = re.MULTILINE if multiline and multiline[0] else 0
                if re.search(pattern, line, flags):
                    # Skip if this is inside a code block
                    if '<code>' not in lines[max(0,i-2):i+3]:
                        issues.append(f"{desc} at line {i}")
                        break
        
        # Check for broken tables (unclosed tags)
        if content.count('<table>') != content.count('</table>'):
            issues.append(f"Unclosed table tags ({content.count('<table>')} open, {content.count('</table>')} closed)")
        
        # Check for broken links
        if content.count('<a ') != content.count('</a>'):
            issues.append(f"Unclosed link tags ({content.count('<a ')} open, {content.count('</a>')} closed)")
        
        # Check for broken attributes in links (common issue)
        bad_links = re.findall(r'<a href="([^"]*)"(?!.*rel=)', content)
        if bad_links:
            issues.append(f"Links without rel attribute: {len(bad_links)} found")
        
        # Check affiliate links present for commercial content
        title = post.get('title', {}).get('rendered', '').lower()
        should_have_affiliate = any(word in title for word in ['best', 'top', 'casino', 'bonus', 'review'])
        has_affiliate = any(domain in content for domain in AFFILIATE_DOMAINS)
        
        if should_have_affiliate and not has_affiliate:
            issues.append("Missing affiliate links (commercial content)")
        
        return {
            'post_id': post_id,
            'title': post.get('title', {}).get('rendered', ''),
            'date': post.get('date', ''),
            'issues': issues,
            'has_affiliate': has_affiliate
        }
        
    except Exception as e:
        return {
            'post_id': post_id,
            'error': str(e)
        }

def main():
    print("=" * 80)
    print("DEEP HTML SCAN - All Posts")
    print("=" * 80)
    print()
    
    for site in SITES:
        print(f"\n🔍 Scanning {site}.com...")
        print("-" * 80)
        
        site_config = SITES[site]
        
        # Get all posts
        curl_command = [
            'curl', '-s',
            '-u', f"{site_config['user']}:{site_config['pass']}",
            f"{site_config['url']}/wp/v2/posts?per_page=100&_fields=id"
        ]
        
        try:
            result = subprocess.run(curl_command, capture_output=True, text=True, check=True)
            posts = json.loads(result.stdout)
            post_ids = [p['id'] for p in posts]
            
            print(f"Found {len(post_ids)} posts")
            
            posts_with_issues = []
            
            for post_id in post_ids:
                result = check_post_deep(post_id, site)
                
                if result.get('issues'):
                    posts_with_issues.append(result)
                    print(f"\n  ❌ Post {post_id}: {result['title'][:60]}")
                    print(f"     Date: {result['date'][:10]}")
                    print(f"     Issues:")
                    for issue in result['issues']:
                        print(f"       • {issue}")
                elif 'error' in result:
                    print(f"\n  ⚠️  Post {post_id}: Error - {result['error']}")
            
            if not posts_with_issues:
                print("\n  ✅ No HTML issues found!")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print("\n" + "=" * 80)
    print("Scan complete!")
    print("=" * 80)

if __name__ == '__main__':
    main()
