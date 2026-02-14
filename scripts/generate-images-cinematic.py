#!/usr/bin/env python3
"""
Generate images using Laozhang.ai Gemini 3 Pro Image Preview (Nano Banana Pro)
Using cinematic prompts with camera angles, lighting, and scene descriptions
"""

import json
import os
import requests
import time
import base64

# Configuration
INPUT_FILE = '/root/.openclaw/workspace/temp/missing-images-cinematic.json'
OUTPUT_DIR = '/root/.openclaw/workspace/temp/images-cinematic'

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

    print(f"    → Calling Nano Banana Pro...")

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
        size_kb = os.path.getsize(png_path) / 1024
        print(f"    ✓ PNG: {size_kb:.0f}KB")
        print(f"    (Install Pillow: pip install Pillow for WebP conversion)")
        return filename

def main():
    # Load JSON
    with open(INPUT_FILE, 'r') as f:
        posts = json.load(f)

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"🎬 Generating {len(posts)} cinematic images with Nano Banana Pro")
    print(f"Model: Gemini 3 Pro Image Preview")
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
    print(f"💰 Cost: ${cost_per_image:.3f}/image (Nano Banana Pro)")
    print(f"   Total: ${len(posts) * cost_per_image:.2f}")
    print(f"   Resolution: 2K @ 16:9 landscape")
    print()

    # Process each post
    success_count = 0
    failed_posts = []

    for i, post in enumerate(posts, 1):
        print(f"[{i}/{len(posts)}] {post['site']} - Post {post['post_id']}")
        print(f"  Title: {post['title'][:60]}...")

        # Use cinematic prompt
        prompt = post.get('cinematic_prompt', post['prompt'])
        print(f"  Camera: {prompt[:80]}...")

        try:
            # Generate image
            filename = generate_gemini_image(prompt, post['filename'], post['alt_text'])

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
    output_file = INPUT_FILE.replace('-cinematic.json', '-cinematic-generated.json')
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

    if failed_posts:
        print()
        print("Failed posts:")
        for post in failed_posts:
            print(f"  - {post['site']}/{post['post_id']}: {post['error']}")
    else:
        print()
        print("✨ All cinematic images generated!")
        print()
        print("Next step: Upload images")
        print("  python3 /root/.openclaw/workspace/scripts/upload-cinematic.py")

if __name__ == '__main__':
    main()
