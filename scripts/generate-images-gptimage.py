#!/usr/bin/env python3
"""
Generate images using Laozhang.ai gpt-image-1 API
Cheaper and faster than DALL-E 3
"""

import json
import os
import requests
import time
import urllib.request

# Configuration
INPUT_FILE = '/root/.openclaw/workspace/temp/missing-images.json'
OUTPUT_DIR = '/root/.openclaw/workspace/temp/images'

# API Configuration
API_KEY = os.environ.get('LAOZHANG_API_KEY')
API_BASE = os.environ.get('LAOZHANG_API_BASE', 'https://api.laozhang.ai/v1')

# Model selection: gpt-image-1 (recommended) or dall-e-3
IMAGE_MODEL = os.environ.get('IMAGE_MODEL', 'gpt-image-1')

def generate_image(prompt, filename, alt_text):
    """Generate image using gpt-image-1 API via Laozhang.ai"""

    if not API_KEY:
        raise Exception("LAOZHANG_API_KEY environment variable not set")

    # Generate image
    response = requests.post(
        f'{API_BASE}/images/generations',
        headers={
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        },
        json={
            'model': IMAGE_MODEL,
            'prompt': prompt,
            'n': 1,
            'size': '1024x1024',  # gpt-image-1 supports square
        },
        timeout=30
    )

    if response.status_code != 200:
        error = response.json()
        raise Exception(f"API error: {error.get('error', {}).get('message', 'Unknown error')}")

    # Get image URL
    data = response.json()
    image_url = data['data'][0]['url']

    # Download image
    output_path = os.path.join(OUTPUT_DIR, filename)
    urllib.request.urlretrieve(image_url, output_path)

    # Optimize: convert to WebP and compress
    try:
        from PIL import Image
        img = Image.open(output_path)

        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # Save as WebP with quality 85 (good balance)
        webp_path = output_path.replace('.png', '.webp')
        img.save(webp_path, 'WEBP', quality=85, method=6)

        # Get file sizes
        original_size = os.path.getsize(output_path) / 1024  # KB
        webp_size = os.path.getsize(webp_path) / 1024  # KB
        savings = (1 - webp_size / original_size) * 100

        # Remove PNG
        os.remove(output_path)

        print(f"    ✓ WebP: {webp_size:.0f}KB (saved {savings:.0f}%)")
        return webp_path.replace(OUTPUT_DIR + '/', '')

    except ImportError:
        print(f"    ✓ PNG: {os.path.getsize(output_path) / 1024:.0f}KB")
        print(f"    (Install Pillow: pip install Pillow for WebP conversion)")
        return filename

def main():
    # Load JSON
    with open(INPUT_FILE, 'r') as f:
        posts = json.load(f)

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"🎨 Generating {len(posts)} images with {IMAGE_MODEL}")
    print(f"Provider: Laozhang.ai")
    print(f"Endpoint: {API_BASE}")
    print(f"Output: {OUTPUT_DIR}")
    print(f"API: {'✅ Configured' if API_KEY else '❌ Missing API_KEY'}")
    print()

    if not API_KEY:
        print("❌ ERROR: LAOZHANG_API_KEY not set")
        print("   Run: export LAOZHANG_API_KEY='your-key'")
        return 1

    # Pricing info
    if IMAGE_MODEL == 'gpt-image-1':
        cost_per_image = 0.01
        print(f"💰 Model: gpt-image-1 (~${cost_per_image:.3f}/image)")
        print(f"   Great for text, charts, graphics")
    elif IMAGE_MODEL == 'dall-e-3':
        cost_per_image = 0.012
        print(f"💰 Model: dall-e-3 (~${cost_per_image:.3f}/image)")
        print(f"   High quality, artistic")
    print()

    # Process each post
    success_count = 0
    failed_posts = []

    for i, post in enumerate(posts, 1):
        print(f"[{i}/{len(posts)}] {post['site']} - Post {post['post_id']}")
        print(f"  Title: {post['title'][:60]}...")
        print(f"  Prompt: {post['prompt'][:80]}...")

        try:
            # Generate image
            filename = generate_image(post['prompt'], post['filename'], post['alt_text'])

            # Update post with generated filename
            post['generated_image'] = filename
            post['status'] = 'generated'

            success_count += 1

            # Rate limiting
            if i < len(posts):
                time.sleep(1.0)

        except Exception as e:
            print(f"    ❌ ERROR: {str(e)}")
            post['status'] = 'failed'
            post['error'] = str(e)
            failed_posts.append(post)

        print()

    # Save updated JSON
    output_file = INPUT_FILE.replace('.json', '-generated.json')
    with open(output_file, 'w') as f:
        json.dump(posts, f, indent=2)

    # Summary
    print("=" * 50)
    print(f"✅ Successfully generated: {success_count}/{len(posts)} images")
    print(f"❌ Failed: {len(failed_posts)} images")
    print(f"📁 Output: {output_file}")
    print(f"📁 Images: {OUTPUT_DIR}")
    print()

    estimated_cost = success_count * cost_per_image
    print(f"💰 Estimated cost: ${estimated_cost:.2f}")

    if failed_posts:
        print()
        print("Failed posts:")
        for post in failed_posts:
            print(f"  - {post['site']}/{post['post_id']}: {post['error']}")

    print()
    print("🚀 Next step: Upload images")
    print(f"   ./upload-images.py {output_file}")

if __name__ == '__main__':
    main()
