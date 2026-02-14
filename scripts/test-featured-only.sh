#!/usr/bin/env python3
"""
Set featured image ONLY - does NOT touch content
Safest method to add images without risk to content
"""

import requests
import os

# Credentials
SITES = {
    'crashcasino': {
        'url': 'https://crashcasino.io/wp-json',
        'user': 'peter',
        'pass': '3vRhtTs2khfdLtTiDFqkdeXI'
    }
}

def set_featured_image_only(site_key, image_path, alt_text, post_id):
    """Upload image and set as featured - NO content modification"""

    site = SITES[site_key]
    api_url = site['url']

    # Step 1: Upload media
    with open(image_path, 'rb') as f:
        image_data = f.read()

    filename = os.path.basename(image_path)
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

    # Step 2: Set alt text
    requests.post(
        f"{api_url}/wp/v2/media/{media_id}",
        auth=(site['user'], site['pass']),
        headers={'Content-Type': 'application/json'},
        json={'alt_text': alt_text},
        timeout=30
    )

    # Step 3: Set as featured image ONLY (NO content update)
    update_response = requests.post(
        f"{api_url}/wp/v2/posts/{post_id}",
        auth=(site['user'], site['pass']),
        headers={'Content-Type': 'application/json'},
        json={'featured_media': media_id},  # ONLY this field!
        timeout=30
    )

    if update_response.status_code == 200:
        return True, f"Featured image set to media ID {media_id}"
    else:
        return False, f"Failed: {update_response.status_code}"

# Test with post 787
print("🧪 Testing: Set featured image ONLY (no content modification)")
print("=" * 60)

result, message = set_featured_image_only(
    'crashcasino',
    '/root/.openclaw/workspace/temp/images-custom-batch2/crashcasino_787.png',
    'Test image - featured only',
    787
)

print(f"Result: {result}")
print(f"Message: {message}")

if result:
    print()
    print("✅ SUCCESS - Featured image set without touching content")
    print()
    print("Ready for batch:")
    print("  python3 /root/.openclaw/workspace/scripts/set-featured-batch.py")
