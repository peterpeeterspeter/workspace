#!/usr/bin/env python3
"""
Scan recent posts on freecrashgames.com and cryptocrashgambling.com
for HTML issues and affiliate link problems
"""

import json
import subprocess
import sys
from datetime import datetime, timedelta

# WordPress credentials
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

# Affiliate domains to check
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

def get_recent_posts(site_key, days=7, limit=50):
    """Get posts from the last N days"""
    site = SITES[site_key]
    
    # Get posts
    curl_command = [
        'curl', '-s',
        '-u', f"{site['user']}:{site['pass']}",
        f"{site['url']}/wp/v2/posts?per_page={limit}&_fields=id,slug,title,link,date,status,content&order=desc"
    ]
    
    try:
        result = subprocess.run(curl_command, capture_output=True, text=True, check=True)
        posts = json.loads(result.stdout)
        
        # Filter by date
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_posts = []
        
        for post in posts:
            try:
                post_date = datetime.fromisoformat(post['date'].replace('Z', '+00:00'))
                if post_date >= cutoff_date:
                    recent_posts.append(post)
            except:
                continue
        
        return recent_posts
    except Exception as e:
        print(f"❌ Error fetching posts from {site_key}: {e}")
        return []

def check_post_html(post):
    """Check a post for HTML issues"""
    issues = []
    content = post.get('content', {}).get('rendered', '')
    
    # Check for affiliate links
    has_affiliate = any(domain in content for domain in AFFILIATE_DOMAINS)
    
    # Check for broken table tags
    table_open = content.count('<table>')
    table_close = content.count('</table>')
    if table_open != table_close:
        issues.append(f"Mismatched table tags: {table_open} open, {table_close} close")
    
    # Check for broken link tags
    link_open = content.count('<a ')
    link_close = content.count('</a>')
    if link_open != link_close:
        issues.append(f"Mismatched link tags: {link_open} open, {link_close} close")
    
    # Check for markdown artifacts
    markdown_artifacts = [
        '[text](url)',  # Unconverted markdown links
        '**text**',      # Unconverted bold
        '*text*',        # Unconverted italic
        '| text |',      # Unconverted table rows
    ]
    
    for artifact in markdown_artifacts:
        if artifact in content:
            issues.append(f"Unconverted markdown: {artifact}")
    
    # Check for duplicate content (repeated paragraphs)
    paragraphs = content.split('</p>')
    if len(paragraphs) > 10:
        # Check for obvious duplicates (same paragraph appears 3+ times)
        paragraph_counts = {}
        for p in paragraphs:
            clean_p = p.strip()
            if len(clean_p) > 100:  # Only check substantial paragraphs
                paragraph_counts[clean_p] = paragraph_counts.get(clean_p, 0) + 1
        
        for p, count in paragraph_counts.items():
            if count >= 3:
                issues.append(f"Duplicate paragraph (appears {count} times)")
                break
    
    return {
        'has_affiliate': has_affiliate,
        'issues': issues,
        'word_count': len(content.split())
    }

def main():
    print("=" * 80)
    print("HTML & Affiliate Link Audit - Recent Posts")
    print("=" * 80)
    print()
    
    all_issues = []
    
    for site_key in SITES:
        print(f"🔍 Checking {site_key}.com...")
        print("-" * 80)
        
        posts = get_recent_posts(site_key, days=30, limit=100)
        
        if not posts:
            print("  No recent posts found.")
            print()
            continue
        
        print(f"  Found {len(posts)} posts from last 30 days")
        print()
        
        for post in posts:
            post_id = post['id']
            title = post['title']['rendered']
            date = post['date'][:10]
            
            # Check HTML
            check_result = check_post_html(post)
            
            # Report issues
            if check_result['issues'] or not check_result['has_affiliate']:
                print(f"  📄 Post {post_id}: {title[:70]}")
                print(f"     Date: {date} | Words: {check_result['word_count']:,}")
                print(f"     Affiliate links: {'✅' if check_result['has_affiliate'] else '⚠️  NONE'}")
                
                if check_result['issues']:
                    print(f"     Issues:")
                    for issue in check_result['issues']:
                        print(f"       • {issue}")
                    all_issues.append({
                        'site': site_key,
                        'post_id': post_id,
                        'title': title,
                        'issues': check_result['issues']
                    })
                
                print()
        print()
    
    print("=" * 80)
    print(f"SUMMARY: {len(all_issues)} posts with issues found")
    print("=" * 80)
    
    if all_issues:
        print("\n📋 Issues Summary:")
        for item in all_issues:
            print(f"\n{item['site']}.com - Post {item['post_id']}")
            print(f"  {item['title']}")
            for issue in item['issues']:
                print(f"  • {issue}")

if __name__ == '__main__':
    main()
