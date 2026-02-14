#!/usr/bin/env python3
"""
Generate images using Laozhang.ai Gemini 3 Pro Image Preview
Model: gemini-3-pro-image-preview (Nano Banana Pro)
Cost: $0.05/image (79% cheaper than official $0.24)
Supports: 1K/2K/4K resolutions, 10 aspect ratios
"""

import json
import os
import requests
import time
import base64
import re

# Configuration
INPUT_FILE = '/root/.openclaw/workspace/temp/missing-images.json'
OUTPUT_DIR = '/root/.openclaw/workspace/temp/images'

# API Configuration
API_KEY = os.environ.get('LAOZHANG_API_KEY')
API_URL = 'https://api.laozhang.ai/v1beta/models/gemini-3-pro-image-preview:generateContent'

# Generation settings
ASPECT_RATIO = '16:9'  # Landscape (good for featured images)
IMAGE_SIZE = '2K'      # Options: 1K, 2K, 4K

def generate_gemini_image(prompt, filename, alt_text):
    """Generate image using Gemini 3 Pro Image Preview via Laozhang.ai"""

    if not API_KEY:
        raise Exception("LAOZHANG_API_KEY environment variable not set")

    # Prepare payload
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {
                "aspectRatio": ASPECT_RATIO,
                "imageSize": IMAGE_SIZE
            }
        }
    }

    # Generate image
    response = requests.post(
        API_URL,
        headers={
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        },
        json=payload,
        timeout=180  # 3 minutes timeout
    )

    if response.status_code != 200:
        error = response.json()
        raise Exception(f"API error: {error}")

    # Extract base64 image data from response
    result = response.json()
    try:
        image_data = result["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]
    except (KeyError, IndexError) as e:
        raise Exception(f"Unexpected response format: {e}")

    # Decode base64 and save
    image_bytes = base64.b64decode(image_data)
    output_path = os.path.join(OUTPUT_DIR, filename)

    # Save as PNG first
    png_path = output_path
    with open(png_path, 'wb') as f:
        f.write(image_bytes)

    # Optimize: convert to WebP and compress
    try:
        from PIL import Image
        img = Image.open(png_path)

        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # Save as WebP with quality 85 (good balance)
        webp_path = png_path.replace('.png', '.webp')
        img.save(webp_path, 'WEBP', quality=85, method=6)

        # Get file sizes
        original_size = os.path.getsize(png_path) / 1024  # KB
        webp_size = os.path.getsize(webp_path) / 1024  # KB
        savings = (1 - webp_size / original_size) * 100

        # Remove PNG
        os.remove(png_path)

        print(f"    ✓ WebP: {webp_size:.0f}KB (saved {savings:.0f}%)")
        return webp_path.replace(OUTPUT_DIR + '/', '')

    except ImportError:
        print(f"    ✓ PNG: {os.path.getsize(png_path) / 1024:.0f}KB")
        print(f"    (Install Pillow: pip install Pillow for WebP conversion)")
        return filename

def main():
    # Load JSON
    with open(INPUT_FILE, 'r') as f:
        posts = json.load(f)

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"🎨 Generating {len(posts)} images with Gemini 3 Pro Image Preview")
    print(f"Model: gemini-3-pro-image-preview (Nano Banana Pro)")
    print(f"Resolution: {IMAGE_SIZE} @ {ASPECT_RATIO}")
    print(f"Endpoint: {API_URL}")
    print(f"Output: {OUTPUT_DIR}")
    print(f"API: {'✅ Configured' if API_KEY else '❌ Missing API_KEY'}")
    print()

    if not API_KEY:
        print("❌ ERROR: LAOZHANG_API_KEY not set")
        print("   Run: export LAOZHANG_API_KEY='your-key'")
        return 1

    # Pricing info
    cost_per_image = 0.05
    print(f"💰 Cost: ${cost_per_image:.3f}/image (79% cheaper than official ${0.24:.2f})")
    print(f"   Estimated total: ${len(posts) * cost_per_image:.2f}")
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
            filename = generate_gemini_image(post['prompt'], post['filename'], post['alt_text'])

            # Update post with generated filename
            post['generated_image'] = filename
            post['status'] = 'generated'

            success_count += 1

            # Rate limiting (10 seconds per image)
            if i < len(posts):
                print(f"    ⏳ Waiting 10s...")
                time.sleep(10.0)

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

    actual_cost = success_count * cost_per_image
    print(f"💰 Actual cost: ${actual_cost:.2f}")
    print(f"   (Official pricing would be: ${success_count * 0.24:.2f})")
    print(f"   Savings: ${success_count * 0.19:.2f} (79%)")

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
