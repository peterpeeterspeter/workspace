#!/usr/bin/env python3
"""
Safe featured image batch processing
Uses direct WordPress REST API - ONLY sets featured_media field
NEVER touches content - zero risk
"""

import json
import os
import requests
import sys

# All site credentials
SITES = {
    'crashcasino': {
        'url': 'https://crashcasino.io/wp-json',
        'user': 'peter',
        'pass': '3vRhtTs2khfdLtTiDFqkdeXI'
    },
    'crashgame': {
        'url': 'https://crashgamegambling.com/wp-json',
        'user': '@peter',
        'pass': 'MioX SygN Xaz6 pK9o RUiK tBMF'
    },
    'freecrash': {
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

def set_featured_image_safe(post, image_dir):
    """Set featured image ONLY - zero content modification risk"""

    site_key = post['site']
    post_id = post['post_id']
    image_file = post['generated_image']
    alt_text = post['alt_text']

    if site_key not in SITES:
        return False, f"Unknown site: {site_key}"

    site = SITES[site_key]
    api_url = site['url']

    image_path = os.path.join(image_dir, image_file)
    if not os.path.exists(image_path):
        return False, f"Image not found: {image_path}"

    try:
        # Upload media
        with open(image_path, 'rb') as f:
            image_data = f.read()

        filename = os.path.basename(image_file)
        content_type = 'image/png' if filename.endswith('.png') else 'image/webp'

        upload_response = requests.post(
            f"{api_url}/wp/v2/media",
            auth=(site['user'], site['pass']),
            headers={
                'Content-Disposition': f'attachment; filename="{filename}"',
                'Content-Type': content_type
            },
            data=image_data,
            timeout=60
        )

        if upload_response.status_code != 201:
            return False, f"Upload failed: {upload_response.status_code}"

        media_info = upload_response.json()
        media_id = media_info['id']

        # Set alt text
        requests.post(
            f"{api_url}/wp/v2/media/{media_id}",
            auth=(site['user'], site['pass']),
            headers={'Content-Type': 'application/json'},
            json={'alt_text': alt_text},
            timeout=30
        )

        # Set featured image ONLY - NO content field sent
        update_response = requests.post(
            f"{api_url}/wp/v2/posts/{post_id}",
            auth=(site['user'], site['pass']),
            headers={'Content-Type': 'application/json'},
            json={'featured_media': media_id},  # ONLY this field!
            timeout=30
        )

        if update_response.status_code == 200:
            return True, f"Media ID {media_id}"
        else:
            return False, f"Failed: {update_response.status_code}"

    except Exception as e:
        return False, f"Error: {str(e)}"

# Get command line args
if len(sys.argv) > 1 and sys.argv[1] == '--test':
    # Test mode: one post
    print("🧪 TEST MODE: One post")
    print("=" * 50)

    test_post = {
        'site': 'crashcasino',
        'post_id': 787,
        'generated_image': 'crashcasino_787.png',
        'alt_text': 'Test image'
    }

    result, message = set_featured_image_safe(
        test_post,
        '/root/.openclaw/workspace/temp/images-custom-batch2'
    )

    if result:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")

elif len(sys.argv) > 1 and sys.argv[1] == '--batch':
    # Batch mode: process generated images
    input_file = '/root/.openclaw/workspace/temp/missing-images-batch2-generated.json'

    with open(input_file, 'r') as f:
        posts = json.load(f)

    print(f"📤 Processing {len(posts)} posts")
    print("Method: Featured image ONLY (no content modification)")
    print("=" * 50)
    print()

    success = 0
    failed = []

    for i, post in enumerate(posts, 1):
        if post.get('status') != 'generated':
            continue

        print(f"[{i}] Post {post['post_id']}: {post['title'][:55]}...")

        result, message = set_featured_image_safe(
            post,
            '/root/.openclaw/workspace/temp/images-custom-batch2'
        )

        if result:
            print(f"  ✅ {message}")
            success += 1
        else:
            print(f"  ❌ {message}")
            failed.append(post)
        print()

    print("=" * 50)
    print(f"✅ {success}/{len(posts)} successful")
    if failed:
        print(f"❌ {len(failed)} failed")

else:
    print("Usage:")
    print("  python3 set-featured-safe.py --test     # Test one post")
    print("  python3 set-featured-safe.py --batch    # Process batch")
