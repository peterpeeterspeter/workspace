#!/usr/bin/env python3
"""
SAFER upload script with content protection
Tests with 1 image first, preserves existing content
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

def upload_safe_test(site_key, image_path, alt_text, post_id):
    """Upload image and insert into content SAFELY"""

    site = SITES[site_key]
    api_url = site['url']

    print(f"    → Step 1: Fetch current post content...")

    # Fetch current post FIRST
    post_response = requests.get(
        f"{api_url}/wp/v2/posts/{post_id}",
        auth=(site['user'], site['pass']),
        timeout=30
    )

    if post_response.status_code != 200:
        return False, f"Failed to fetch post: {post_response.status_code}"

    post_data = post_response.json()

    # Get EXISTING content (use raw for editing)
    existing_content = post_data.get('content', {}).get('raw', '')
    content_length = len(existing_content)

    print(f"    ✓ Current content length: {content_length} chars")

    if content_length == 0:
        print(f"    ⚠️ WARNING: Post has no content! Skipping content insertion.")
        print(f"    → Will still upload image...")

    print(f"    → Step 2: Uploading media...")

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
        return False, f"Media upload failed: {response.status_code}"

    media_info = response.json()
    media_id = media_info['id']
    image_url = media_info.get('source_url')

    print(f"    ✓ Media uploaded: ID {media_id}")

    # Set alt text
    print(f"    → Step 3: Setting alt text...")
    alt_url = f"{api_url}/wp/v2/media/{media_id}"
    requests.post(
        alt_url,
        auth=(site['user'], site['pass']),
        headers={'Content-Type': 'application/json'},
        json={'alt_text': alt_text},
        timeout=30
    )
    print(f"    ✓ Alt text set")

    # Set as featured image
    print(f"    → Step 4: Setting as featured image...")
    post_url = f"{api_url}/wp/v2/posts/{post_id}"
    requests.post(
        post_url,
        auth=(site['user'], site['pass']),
        headers={'Content-Type': 'application/json'},
        json={'featured_media': media_id},
        timeout=30
    )
    print(f"    ✓ Featured image set")

    # ONLY insert into content if post HAS content
    if content_length > 0:
        print(f"    → Step 5: Inserting image into content...")
        image_html = f'<figure class="featured-image-article"><img src="{image_url}" alt="{alt_text}" class="wp-post-image" /></figure>\n\n'

        # Check if image already exists
        if image_url in existing_content:
            print(f"    ✓ Image already in content, skipping insertion")
        else:
            # PREPEND image to existing content
            new_content = image_html + existing_content

            # Update with BOTH content AND featured_media
            update_response = requests.post(
                post_url,
                auth=(site['user'], site['pass']),
                headers={'Content-Type': 'application/json'},
                json={
                    'content': new_content,
                    'featured_media': media_id
                },
                timeout=30
            )

            if update_response.status_code == 200:
                print(f"    ✓ Image inserted (new content length: {len(new_content)} chars)")

                # VERIFY content wasn't lost
                verify_response = requests.get(
                    f"{api_url}/wp/v2/posts/{post_id}",
                    auth=(site['user'], site['pass']),
                    timeout=30
                )
                verify_data = verify_response.json()
                verify_length = len(verify_data.get('content', {}).get('raw', ''))

                print(f"    ✓ Verified: content is {verify_length} chars")

                if verify_length < content_length:
                    print(f"    ⚠️ WARNING: Content shrank! Lost {content_length - verify_length} chars")
                    return False, "Content verification failed - content was lost"
            else:
                return False, f"Content update failed: {update_response.status_code}"
    else:
        print(f"    → Step 5: SKIPPED (post has no content to protect)")

    return True, "Success - content preserved"

def main():
    # Test with ONE post only
    test_post_id = 787  # Safe Crash Gambling: Red Flags to Avoid
    test_image = '/root/.openclaw/workspace/temp/images-custom-batch2/crashcasino_787.png'

    if not os.path.exists(test_image):
        print(f"❌ Test image not found: {test_image}")
        print("Looking for alternative...")
        # Find any image
        import glob
        images = glob.glob('/root/.openclaw/workspace/temp/images-custom-batch2/*.png')
        if images:
            test_image = images[0]
            test_post_id = int(images[0].split('_')[-1].replace('.png', ''))
            print(f"Found: {test_image} for post {test_post_id}")
        else:
            print("No images found")
            return

    print(f"🧪 SAFE TEST: One image only")
    print(f"Post ID: {test_post_id}")
    print(f"Image: {test_image}")
    print("=" * 60)
    print()

    result, message = upload_safe_test('crashcasino', test_image, "Test image", test_post_id)

    print()
    print("=" * 60)
    if result:
        print(f"✅ TEST PASSED: {message}")
        print()
        print("✨ Content protection working!")
        print("Ready for full batch:")
        print("  python3 /root/.openclaw/workspace/scripts/generate-images-full-safe.py")
    else:
        print(f"❌ TEST FAILED: {message}")

if __name__ == '__main__':
    main()
