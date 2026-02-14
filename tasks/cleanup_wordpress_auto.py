#!/usr/bin/env python3
"""
WordPress Content Cleanup Script - Non-Interactive
Identifies and deletes duplicate/off-topic posts from crash gambling sites.

Usage:
    python cleanup_wordpress_auto.py --site crashgamegambling.com

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
    url = site_config['url']
    auth = (site_config['user'], site_config['app_password'])

    posts = []
    page = 1
    per_page = 100

    while True:
        response = requests.get(
            f"{url}/wp/v2/posts?per_page={per_page}&page={page}",
            auth=auth
        )

        if response.status_code != 200:
            break

        batch = response.json()
        if not batch:
            break

        posts.extend(batch)
        page += 1

    return posts


def identify_duplicates(posts):
    """Identify duplicate posts (by title or slug with '-2')."""
    duplicates = []

    # Track seen titles
    seen_titles = {}

    for post in posts:
        title = post['title']['rendered'].strip().lower()
        slug = post['slug']
        post_id = post['id']

        # Check for -2 in slug
        if '-2' in slug or slug.endswith('-2'):
            duplicates.append({
                'id': post_id,
                'title': post['title']['rendered'],
                'slug': slug,
                'date': post['date'],
                'reason': 'Duplicate (slug has -2)'
            })
            continue

        # Check for duplicate titles
        if title in seen_titles:
            # Mark both as duplicates (keep the older one)
            original_id = seen_titles[title]
            if post['date'] < posts[original_id]['date']:
                duplicates.append({
                    'id': post_id,
                    'title': post['title']['rendered'],
                    'slug': slug,
                    'date': post['date'],
                    'reason': 'Duplicate title'
                })
            else:
                duplicates.append({
                    'id': posts[original_id]['id'],
                    'title': posts[original_id]['title']['rendered'],
                    'slug': posts[original_id]['slug'],
                    'date': posts[original_id]['date'],
                    'reason': 'Duplicate title'
                })
        else:
            seen_titles[title] = post_id

    return duplicates


def identify_off_topic(posts):
    """Identify off-topic posts (pre-2021 generic content)."""
    off_topic = []

    for post in posts:
        date_str = post['date']
        title = post['title']['rendered'].lower()
        slug = post['slug']

        # Check if pre-2021
        date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        if date_obj.year < 2021:
            # Check if crash-related
            crash_keywords = ['crash', 'aviator', 'bustabit', 'stake', 'bc.game', 'bcgame']
            if not any(keyword in title or keyword in slug for keyword in crash_keywords):
                off_topic.append({
                    'id': post['id'],
                    'title': post['title']['rendered'],
                    'slug': slug,
                    'date': date_str,
                    'reason': 'Pre-2021 generic content'
                })

    return off_topic


def delete_post(site_config, post_id):
    """Delete a post."""
    url = site_config['url']
    auth = (site_config['user'], site_config['app_password'])

    response = requests.delete(
        f"{url}/wp/v2/posts/{post_id}?force=true",
        auth=auth
    )

    return response.status_code == 200


def cleanup_site(site_name):
    """Cleanup a single site."""
    site_config = SITES.get(site_name)

    if not site_config:
        print(f"❌ Unknown site: {site_name}")
        return

    print(f"\n{'='*70}")
    print(f"CLEANING UP: {site_name.upper()}")
    print(f"{'='*70}\n")

    # Fetch all posts
    print("📊 Fetching all posts...")
    posts = get_all_posts(site_config)
    print(f"✅ Found {len(posts)} posts\n")

    # Identify duplicates
    print("🔍 Identifying duplicates...")
    duplicates = identify_duplicates(posts)
    print(f"   Found {len(duplicates)} duplicate posts\n")

    # Identify off-topic
    print("🔍 Identifying off-topic content...")
    off_topic = identify_off_topic(posts)
    print(f"   Found {len(off_topic)} off-topic posts\n")

    # Combine all to delete
    to_delete = duplicates + off_topic

    print(f"📋 SUMMARY:")
    print(f"   Total posts: {len(posts)}")
    print(f"   Duplicates to delete: {len(duplicates)}")
    print(f"   Off-topic to delete: {len(off_topic)}")
    print(f"   Total deletions: {len(to_delete)}\n")

    if not to_delete:
        print("✅ No posts to delete!")
        return

    # Delete posts
    print("🗑️  DELETING POSTS...")
    deleted = 0
    failed = 0

    for i, post in enumerate(to_delete, 1):
        print(f"   [{i}/{len(to_delete)}] Deleting: {post['title'][:50]}... ", end='', flush=True)

        if delete_post(site_config, post['id']):
            print("✅")
            deleted += 1
        else:
            print("❌")
            failed += 1

    print(f"\n✅ DELETION COMPLETE!")
    print(f"   Successfully deleted: {deleted}")
    print(f"   Failed: {failed}")


def main():
    parser = argparse.ArgumentParser(description='WordPress Cleanup (Non-Interactive)')
    parser.add_argument('--site', required=True, help='Site to cleanup')
    args = parser.parse_args()

    cleanup_site(args.site)


if __name__ == '__main__':
    main()
