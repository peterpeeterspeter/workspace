#!/usr/bin/env python3
"""
Upload batch 2 images to WordPress and insert into content
"""

import json
import os
import requests
import base64

# Site credentials
SITES = {
    'crashcasino': {
        'url': 'https://crashcasino.io/wp-json',
        'user': 'peter',
        'pass': '3vRhtTs2khfdLtTiDFqkdeXI'
    }
}

def upload_and_insert(site_key, image_path, alt_text, post_id):
    """Upload image and insert into post content"""

    site = SITES[site_key]
    api_url = site['url']

    print(f"    → Uploading to {site_key}...")

    # Read image
    with open(image_path, 'rb') as f:
        image_data = f.read()

    filename = os.path.basename(image_path)
    content_type = 'image/png' if filename.endswith('.png') else 'image/webp'

    # Upload media
    upload_url = f"{api_url}/wp/v2/media"
    headers = {
        'Content-Disposition': f'attachment; filename="{filename}"',
        'Content-Type': content_type
    }

    response = requests.post(
        upload_url,
        auth=(site['user'], site['pass']),
        headers=headers,
        data=image_data,
        timeout=60
    )

    if response.status_code != 201:
        return False, f"Upload failed: {response.status_code}"

    media_info = response.json()
    media_id = media_info['id']
    image_url = media_info.get('source_url')

    print(f"    ✓ Media ID {media_id}")

    # Set alt text
    alt_url = f"{api_url}/wp/v2/media/{media_id}"
    requests.post(
        alt_url,
        auth=(site['user'], site['pass']),
        headers={'Content-Type': 'application/json'},
        json={'alt_text': alt_text},
        timeout=30
    )

    # Set as featured image
    post_url = f"{api_url}/wp/v2/posts/{post_id}"
    requests.post(
        post_url,
        auth=(site['user'], site['pass']),
        headers={'Content-Type': 'application/json'},
        json={'featured_media': media_id},
        timeout=30
    )

    print(f"    ✓ Featured set")

    # Insert into content
    post_response = requests.get(post_url, auth=(site['user'], site['pass']), timeout=30)
    post_data = post_response.json()
    current_content = post_data.get('content', {}).get('raw', '')

    image_html = f'<figure class="featured-image-article"><img src="{image_url}" alt="{alt_text}" class="wp-post-image" /></figure>\n\n'

    if image_url not in current_content:
        new_content = image_html + current_content
        requests.post(
            post_url,
            auth=(site['user'], site['pass']),
            headers={'Content-Type': 'application/json'},
            json={'content': new_content},
            timeout=30
        )
        print(f"    ✓ Inserted into content")

    return True, "Success"

def main():
    # Load batch 2 results
    input_file = '/root/.openclaw/workspace/temp/missing-images-batch2-generated.json'

    with open(input_file, 'r') as f:
        posts = json.load(f)

    print(f"📤 Uploading {len(posts)} images to WordPress")
    print()

    success = 0
    failed = []

    for i, post in enumerate(posts, 1):
        if post.get('status') != 'generated':
            continue

        image_path = os.path.join('/root/.openclaw/workspace/temp/images-custom-batch2', post['generated_image'])

        if not os.path.exists(image_path):
            print(f"[{i}] ❌ Image not found: {image_path}")
            continue

        print(f"[{i}] Post {post['post_id']}: {post['title'][:55]}...")

        result, msg = upload_and_insert(
            post['site'],
            image_path,
            post['alt_text'],
            post['post_id']
        )

        if result:
            print(f"  ✅ {msg}")
            success += 1
        else:
            print(f"  ❌ {msg}")
            failed.append(post)
        print()

    print("=" * 50)
    print(f"✅ Uploaded: {success}/{len(posts)}")
    if failed:
        print(f"❌ Failed: {len(failed)}")
    print()
    print("Review images at:")
    for post in posts:
        if post.get('status') == 'generated':
            print(f"  - {post['url']}")

if __name__ == '__main__':
    main()
