#!/usr/bin/env python3
"""
Upload images directly via WordPress REST API
Bypass pinch-to-post for direct media upload
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

def upload_featured_image(site_key, image_path, alt_text, post_id):
    """Upload image and set as featured image for a post"""

    if site_key not in SITES:
        return False, f"Unknown site: {site_key}"

    site = SITES[site_key]
    api_url = site['url']

    print(f"    → Uploading to {site_key}...")

    # Read image file
    if not os.path.exists(image_path):
        return False, f"Image not found: {image_path}"

    with open(image_path, 'rb') as f:
        image_data = f.read()

    # Get filename and extension
    filename = os.path.basename(image_path)
    content_type = 'image/png' if filename.endswith('.png') else 'image/webp'

    # Upload media to WordPress
    upload_url = f"{api_url}/wp/v2/media"
    headers = {
        'Content-Disposition': f'attachment; filename="{filename}"',
        'Content-Type': content_type
    }

    try:
        # Upload image
        response = requests.post(
            upload_url,
            auth=(site['user'], site['pass']),
            headers=headers,
            data=image_data,
            timeout=60
        )

        if response.status_code != 201:
            return False, f"Upload failed: {response.status_code} - {response.text}"

        media_info = response.json()
        media_id = media_info['id']
        print(f"    ✓ Media uploaded: ID {media_id}")

        # Set alt text
        alt_url = f"{api_url}/wp/v2/media/{media_id}"
        alt_response = requests.post(
            alt_url,
            auth=(site['user'], site['pass']),
            headers={'Content-Type': 'application/json'},
            json={'alt_text': alt_text},
            timeout=30
        )

        if alt_response.status_code == 200:
            print(f"    ✓ Alt text set")

        # Set as featured image for the post
        post_url = f"{api_url}/wp/v2/posts/{post_id}"
        post_response = requests.post(
            post_url,
            auth=(site['user'], site['pass']),
            headers={'Content-Type': 'application/json'},
            json={'featured_media': media_id},
            timeout=30
        )

        if post_response.status_code == 200:
            print(f"    ✓ Set as featured image for post {post_id}")
            return True, "Success"
        else:
            return False, f"Failed to set featured: {post_response.status_code}"

    except Exception as e:
        return False, f"Error: {str(e)}"

def main():
    # Load test batch JSON
    input_file = '/root/.openclaw/workspace/temp/missing-images-test-batch.json'

    with open(input_file, 'r') as f:
        posts = json.load(f)

    # Filter posts with generated images
    ready_posts = [p for p in posts if p.get('status') == 'generated' and p.get('generated_image')]

    print(f"📤 Uploading {len(ready_posts)} test images to WordPress")
    print(f"Method: Direct REST API upload")
    print()

    success_count = 0
    failed_posts = []

    for i, post in enumerate(ready_posts, 1):
        image_path = os.path.join('/root/.openclaw/workspace/temp/images', post['generated_image'])

        print(f"[{i}/{len(ready_posts)}] {post['site']} - Post {post['post_id']}")
        print(f"  Image: {post['generated_image']}")
        print(f"  Alt: {post['alt_text'][:60]}...")

        # Upload
        success, output = upload_featured_image(
            post['site'],
            image_path,
            post['alt_text'],
            post['post_id']
        )

        if success:
            print(f"  ✅ {output}")
            post['upload_status'] = 'uploaded'
            post['media_id'] = output
            success_count += 1
        else:
            print(f"  ❌ {output}")
            post['upload_status'] = 'failed'
            post['upload_error'] = output
            failed_posts.append(post)

        print()

    # Save updated JSON
    output_file = input_file.replace('-test-batch.json', '-test-uploaded.json')
    with open(output_file, 'w') as f:
        json.dump(posts, f, indent=2)

    # Summary
    print("=" * 50)
    print(f"✅ Successfully uploaded: {success_count}/{len(ready_posts)} images")
    print(f"❌ Failed: {len(failed_posts)} uploads")
    print(f"📁 Log: {output_file}")
    print()

    if failed_posts:
        print("Failed uploads:")
        for post in failed_posts:
            print(f"  - {post['site']}/{post['post_id']}: {post.get('upload_error', 'Unknown error')}")
    else:
        print("✨ All test images uploaded successfully!")
        print()
        print("Next steps:")
        print("1. Check the posts to verify images are displaying:")
        for post in ready_posts:
            print(f"   - {post['url']}")
        print()
        print("2. If good, run full batch:")
        print("   export LAOZHANG_API_KEY='your-key'")
        print("   python3 /root/.openclaw/workspace/scripts/generate-images-gemini.py")

if __name__ == '__main__':
    main()
