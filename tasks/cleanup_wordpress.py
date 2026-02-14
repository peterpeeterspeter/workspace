#!/usr/bin/env python3
"""
WordPress Content Cleanup Script
Identifies and deletes duplicate/off-topic posts from crash gambling sites.

Usage:
    python cleanup_wordpress.py --site crashgamegambling.com --dry-run
    python cleanup_wordpress.py --site crashgamegambling.com --execute

Requirements:
    - WordPress REST API credentials in .env file
    - Application password for authentication
"""

import requests
import json
import os
import argparse
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Site configurations
SITES = {
    'crashgamegambling.com': {
        'url': os.getenv('WORDPRESS_CRASHGAMEGAMBLING_URL'),
        'user': os.getenv('WORDPRESS_CRASHGAMEGAMBLING_USER'),
        'app_password': os.getenv('WORDPRESS_CRASHGAMEGAMBLING_APP_PASSWORD')
    },
    'cryptocrashgambling.com': {
        'url': os.getenv('WORDPRESS_CRYPTOCRASH_URL'),
        'user': os.getenv('WORDPRESS_CRYPTOCRASH_USER'),
        'app_password': os.getenv('WORDPRESS_CRYPTOCRASH_APP_PASSWORD')
    },
    'freecrashgames.com': {
        'url': os.getenv('WORDPRESS_FREECRASH_URL'),
        'user': os.getenv('WORDPRESS_FREECRASH_USER'),
        'app_password': os.getenv('WORDPRESS_FREECRASH_APP_PASSWORD')
    },
    'crashcasino.io': {
        'url': os.getenv('WORDPRESS_CRASHCASINO_URL'),
        'user': os.getenv('WORDPRESS_CRASHCASINO_USER'),
        'app_password': os.getenv('WORDPRESS_CRASHCASINO_APP_PASSWORD')
    }
}


def get_all_posts(site_config):
    """Fetch all posts from WordPress site."""
    url = f"{site_config['url']}/wp/v2/posts"
    auth = (site_config['user'], site_config['app_password'])
    
    all_posts = []
    page = 1
    
    while True:
        params = {'per_page': 100, 'page': page}
        response = requests.get(url, auth=auth, params=params)
        
        if response.status_code != 200:
            print(f"Error fetching posts: {response.status_code}")
            break
        
        posts = response.json()
        if not posts:
            break
        
        all_posts.extend(posts)
        page += 1
    
    return all_posts


def identify_duplicates(posts):
    """Identify duplicate posts (slug or title contains '-2')."""
    duplicates = []
    
    for post in posts:
        slug = post.get('slug', '')
        title = post.get('title', {}).get('rendered', '')
        id = post.get('id')
        date = post.get('date')
        link = post.get('link')
        
        if '-2' in slug or ' 2' in title or '– 2' in title:
            duplicates.append({
                'id': id,
                'title': title,
                'slug': slug,
                'date': date,
                'link': link
            })
    
    return duplicates


def identify_offtopic(posts):
    """Identify off-topic posts (pre-2021, non-crash content)."""
    offtopic = []
    
    for post in posts:
        title = post.get('title', {}).get('rendered', '').lower()
        date = post.get('date', '')
        id = post.get('id')
        link = post.get('link')
        
        # Pre-2021 posts (likely generic casino content)
        if '2020' in date or '2019' in date or '2018' in date:
            # Unless it's crash-specific
            if 'crash' not in title and 'aviator' not in title:
                offtopic.append({
                    'id': id,
                    'title': post.get('title', {}).get('rendered', ''),
                    'date': date,
                    'reason': 'Pre-2021 generic content'
                })
        
        # Clearly off-topic (non-gambling)
        off_topic_keywords = ['ai interpretability', 'cybersecurity', 'python', 'javascript', 'blockchain tutorial']
        if any(keyword in title for keyword in off_topic_keywords):
            offtopic.append({
                'id': id,
                'title': post.get('title', {}).get('rendered', ''),
                'date': date,
                'reason': 'Non-gambling content'
            })
    
    return offtopic


def delete_post(post_id, site_config):
    """Delete a post via WordPress REST API."""
    url = f"{site_config['url']}/wp/v2/posts/{post_id}?force=true"
    auth = (site_config['user'], site_config['app_password'])
    
    response = requests.delete(url, auth=auth)
    return response.status_code == 200


def audit_site(site_name, dry_run=True):
    """Audit a site for duplicates and off-topic content."""
    if site_name not in SITES:
        print(f"Site {site_name} not configured")
        return
    
    site_config = SITES[site_name]
    
    if not site_config['url']:
        print(f"No credentials configured for {site_name}")
        print(f"Add these to your .env file:")
        print(f"  WORDPRESS_{site_name.upper().replace('.', '_')}_URL=https://{site_name}/wp-json")
        print(f"  WORDPRESS_{site_name.upper().replace('.', '_')}_USER=username")
        print(f"  WORDPRESS_{site_name.upper().replace('.', '_')}_APP_PASSWORD=application_password")
        return
    
    print(f"\n{'=' * 70}")
    print(f"AUDITING: {site_name.upper()}")
    print(f"{'=' * 70}")
    
    # Get all posts
    print("\n📊 Fetching all posts...")
    posts = get_all_posts(site_config)
    print(f"✅ Found {len(posts)} posts")
    
    # Identify duplicates
    print("\n🔍 Identifying duplicates...")
    duplicates = identify_duplicates(posts)
    print(f"   Found {len(duplicates)} duplicate posts")
    
    # Identify off-topic
    print("\n🔍 Identifying off-topic content...")
    offtopic = identify_offtopic(posts)
    print(f"   Found {len(offtopic)} off-topic posts")
    
    # Summary
    total_deletions = len(duplicates) + len(offtopic)
    print(f"\n📋 SUMMARY:")
    print(f"   Total posts: {len(posts)}")
    print(f"   Duplicates to delete: {len(duplicates)}")
    print(f"   Off-topic to delete: {len(offtopic)}")
    print(f"   Total deletions: {total_deletions}")
    
    # Show duplicates
    if duplicates:
        print(f"\n🔴 DUPLICATES:")
        for d in duplicates:
            print(f"   [{d['id']}] {d['title'][:60]}")
            print(f"         Slug: {d['slug']}")
            print(f"         Date: {d['date']}")
            print()
    
    # Show off-topic
    if offtopic:
        print(f"\n🟠 OFF-TOPIC:")
        for o in offtopic:
            print(f"   [{o['id']}] {o['title'][:60]}")
            print(f"         Reason: {o['reason']}")
            print(f"         Date: {o['date']}")
            print()
    
    # Execute deletions
    if not dry_run and total_deletions > 0:
        confirm = input(f"\n⚠️  Delete {total_deletions} posts? (yes/no): ")
        if confirm.lower() == 'yes':
            print("\n🗑️  Deleting posts...")
            
            # Delete duplicates
            for d in duplicates:
                if delete_post(d['id'], site_config):
                    print(f"   ✅ Deleted: {d['title'][:50]}")
                else:
                    print(f"   ❌ Failed: {d['title'][:50]}")
            
            # Delete off-topic
            for o in offtopic:
                if delete_post(o['id'], site_config):
                    print(f"   ✅ Deleted: {o['title'][:50]}")
                else:
                    print(f"   ❌ Failed: {o['title'][:50]}")
            
            print(f"\n✅ Cleanup complete!")
        else:
            print("\n❌ Cancelled")
    elif dry_run:
        print(f"\n⚠️  DRY RUN - Use --execute to delete posts")


def main():
    parser = argparse.ArgumentParser(description='WordPress Content Cleanup')
    parser.add_argument('--site', required=True, help='Site to audit (e.g., crashgamegambling.com)')
    parser.add_argument('--execute', action='store_true', help='Execute deletions (not dry-run)')
    
    args = parser.parse_args()
    
    print("\n🔍 WORDPRESS CONTENT CLEANUP")
    print("=" * 70)
    print(f"Mode: {'EXECUTE' if args.execute else 'DRY RUN'}")
    
    audit_site(args.site, dry_run=not args.execute)


if __name__ == '__main__':
    main()
