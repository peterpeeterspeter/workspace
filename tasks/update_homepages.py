#!/usr/bin/env python3
"""
WordPress Homepage Updater
Updates site homepages with new content.
"""

import requests
import json
import os
import markdown2
from dotenv import load_dotenv

load_dotenv()

# Site configurations
SITES = {
    'crashgamegambling.com': {
        'url': os.getenv('WORDPRESS_CRASHGAMEGAMBLING_URL'),
        'user': os.getenv('WORDPRESS_CRASHGAMEGAMBLING_USER'),
        'app_password': os.getenv('WORDPRESS_CRASHGAMEGAMBLING_APP_PASSWORD'),
        'file': 'crashgamegambling-homepage.md'
    },
    'cryptocrashgambling.com': {
        'url': os.getenv('WORDPRESS_CRYPTOCRASH_URL'),
        'user': os.getenv('WORDPRESS_CRYPTOCRASH_USER'),
        'app_password': os.getenv('WORDPRESS_CRYPTOCRASH_APP_PASSWORD'),
        'file': 'cryptocrashgambling-homepage.md'
    },
    'freecrashgames.com': {
        'url': os.getenv('WORDPRESS_FREECRASH_URL'),
        'user': os.getenv('WORDPRESS_FREECRASH_USER'),
        'app_password': os.getenv('WORDPRESS_FREECRASH_APP_PASSWORD'),
        'file': 'freecrashgames-homepage.md'
    },
    'crashcasino.io': {
        'url': os.getenv('WORDPRESS_CRASHCASINO_URL'),
        'user': os.getenv('WORDPRESS_CRASHCASINO_USER'),
        'app_password': os.getenv('WORDPRESS_CRASHCASINO_APP_PASSWORD'),
        'file': 'crashcasino-homepage.md'
    }
}


def get_page_id_by_title(site_config, title='Home'):
    """Get the page ID for the homepage by title."""
    auth = (site_config['user'], site_config['app_password'])
    headers = {'Content-Type': 'application/json'}
    
    # Search for pages
    response = requests.get(
        f"{site_config['url']}/wp/v2/pages?search={title}",
        auth=auth,
        headers=headers
    )
    
    if response.status_code == 200:
        pages = response.json()
        if pages and len(pages) > 0:
            return pages[0]['id']  # Return first matching page ID
    
    return None


def update_homepage(site_config, homepage_file, dry_run=False):
    """Update homepage with new content."""
    
    # Read homepage markdown
    with open(f'/root/.openclaw/workspace/drafts/{homepage_file}', 'r') as f:
        content = f.read()
    
    # Split into frontmatter and content
    lines = content.split('\n')
    frontmatter = {}
    content_lines = []
    in_frontmatter = False
    
    for line in lines:
        if line.strip().startswith('---'):
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter and ':' in line:
            key, value = line.split(':', 1)
            frontmatter[key.strip()] = value.strip()
        else:
            content_lines.append(line)
    
    markdown_content = '\n'.join(content_lines)
    
    # Convert to HTML
    html_content = markdown2.markdown(
        markdown_content,
        extras=['tables', 'fenced-code-blocks', 'header-ids']
    )
    
    # Prepare page data
    page_data = {
        'title': frontmatter.get('Title', 'Home'),
        'content': html_content,
        'status': 'draft' if dry_run else 'publish',
        'excerpt': frontmatter.get('Excerpt', '')[:160]
    }
    
    # Get homepage ID
    page_id = get_page_id_by_title(site_config)
    
    if not page_id:
        return {
            'success': False,
            'error': 'Could not find homepage'
        }
    
    # Update page
    auth = (site_config['user'], site_config['app_password'])
    headers = {'Content-Type': 'application/json'}
    
    if not dry_run:
        response = requests.post(
            f"{site_config['url']}/wp/v2/pages/{page_id}",
            auth=auth,
            headers=headers,
            json=page_data
        )
        
        if response.status_code == 200:
            result = response.json()
            return {
                'success': True,
                'page_id': page_id,
                'url': result['link'],
                'title': result['title']['rendered']
            }
        else:
            return {
                'success': False,
                'error': response.text,
                'status_code': response.status_code
            }
    else:
        return {
            'success': True,
            'dry_run': True,
            'page_id': page_id,
            'title': page_data['title']
        }


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Update WordPress homepages')
    parser.add_argument('--dry-run', action='store_true', help='Test without updating')
    args = parser.parse_args()
    
    print("🏠 UPDATING HOMEPAGES")
    print("=" * 80)
    print()
    
    success_count = 0
    
    for site_name, site_config in SITES.items():
        print(f"📄 {site_name}")
        
        result = update_homepage(site_config, site_config['file'], dry_run=args.dry_run)
        
        if result['success']:
            if result.get('dry_run'):
                print(f"   ✅ DRY RUN: Would update page {result['page_id']}")
            else:
                print(f"   ✅ Updated: {result['url']}")
            success_count += 1
        else:
            print(f"   ❌ Failed: {result.get('error')}")
        
        print()
    
    print("=" * 80)
    print(f"RESULTS: {success_count}/{len(SITES)} updated")


if __name__ == '__main__':
    main()
