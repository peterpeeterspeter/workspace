#!/usr/bin/env python3
"""
Generate next 5 test images with custom prompts
Posts 834, 833, 817, 816, 787 (skipping already done 855, 838, 837, 836, 835)
"""

import json
import os
import requests
import time
import base64

# Configuration
INPUT_FILE = '/root/.openclaw/workspace/temp/missing-images-custom.json'
OUTPUT_DIR = '/root/.openclaw/workspace/temp/images-custom-batch2'

# API Configuration
API_KEY = os.environ.get('LAOZHANG_API_KEY')
API_URL = 'https://api.laozhang.ai/v1beta/models/gemini-3-pro-image-preview:generateContent'

# Skip these already done posts
SKIP_POSTS = [855, 838, 837, 836, 835]
BATCH_SIZE = 5

# Generation settings
ASPECT_RATIO = '16:9'
IMAGE_SIZE = '2K'

def generate_image(prompt, filename, post_id):
    """Generate image using Gemini 3 Pro"""

    if not API_KEY:
        raise Exception("LAOZHANG_API_KEY not set")

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {
                "aspectRatio": ASPECT_RATIO,
                "imageSize": IMAGE_SIZE
            }
        }
    }

    print(f"    → Nano Banana Pro generating...")

    response = requests.post(
        API_URL,
        headers={'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'},
        json=payload,
        timeout=180
    )

    if response.status_code != 200:
        error = response.json()
        raise Exception(f"API error {response.status_code}: {error}")

    result = response.json()
    try:
        image_data = result["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]
    except (KeyError, IndexError) as e:
        raise Exception(f"Unexpected response: {e}")

    # Decode and save
    image_bytes = base64.b64decode(image_data)
    output_path = os.path.join(OUTPUT_DIR, filename)

    with open(output_path, 'wb') as f:
        f.write(image_bytes)

    # WebP conversion
    try:
        from PIL import Image
        img = Image.open(output_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        webp_path = output_path.replace('.png', '.webp')
        img.save(webp_path, 'WEBP', quality=85, method=6)
        os.remove(output_path)
        size_kb = os.path.getsize(webp_path) / 1024
        print(f"    ✓ WebP: {size_kb:.0f}KB")
        return webp_path.replace(OUTPUT_DIR + '/', '')
    except ImportError:
        size_kb = os.path.getsize(output_path) / 1024
        print(f"    ✓ PNG: {size_kb:.0f}KB")
        return filename

def main():
    with open(INPUT_FILE, 'r') as f:
        all_posts = json.load(f)

    # Filter out already done posts and take next 5
    posts = [p for p in all_posts if p['post_id'] not in SKIP_POSTS][:BATCH_SIZE]

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"🧪 TEST BATCH 2: Next {len(posts)} images with CUSTOM prompts")
    print(f"Model: Nano Banana Pro (Gemini 3 Pro)")
    print(f"Resolution: {IMAGE_SIZE} @ {ASPECT_RATIO}")
    print(f"Output: {OUTPUT_DIR}")
    print(f"API: {'✅ Configured' if API_KEY else '❌ Missing'}")
    print()

    if not API_KEY:
        print("❌ ERROR: LAOZHANG_API_KEY not set")
        print("   Run: export LAOZHANG_API_KEY='your-key'")
        return 1

    cost_per_image = 0.05
    print(f"💰 Cost: ${cost_per_image:.3f}/image")
    print(f"   Test batch: ${len(posts) * cost_per_image:.2f}")
    print(f"   Full run (44 remaining): ${(49 - len(SKIP_POSTS) - len(posts)) * cost_per_image:.2f}")
    print()

    success = 0
    failed = []

    for i, post in enumerate(posts, 1):
        print(f"[{i}/{len(posts)}] {post['site']} - Post {post['post_id']}")
        print(f"  Title: {post['title'][:65]}...")
        print(f"  Custom focus: {post.get('custom_prompt', post.get('prompt', ''))[:80]}...")

        try:
            filename = generate_image(post['custom_prompt'], post['filename'], post['alt_text'])
            post['generated_image'] = filename
            post['status'] = 'generated'
            success += 1

            if i < len(posts):
                print(f"    ⏳ Waiting 10s...")
                time.sleep(10.0)

        except Exception as e:
            print(f"    ❌ {str(e)}")
            post['status'] = 'failed'
            post['error'] = str(e)
            failed.append(post)

        print()

    # Save batch results
    output_file = INPUT_FILE.replace('-custom.json', '-batch2-generated.json')
    with open(output_file, 'w') as f:
        json.dump(posts, f, indent=2)

    print("=" * 50)
    print(f"✅ Test batch 2 complete: {success}/{len(posts)} images")
    print(f"❌ Failed: {len(failed)}")
    print(f"📁 Output: {output_file}")
    print(f"📁 Images: {OUTPUT_DIR}")
    print()

    actual_cost = success * cost_per_image
    print(f"💰 Test batch 2 cost: ${actual_cost:.2f}")

    if failed:
        print("\nFailed:")
        for p in failed:
            print(f"  - {p['site']}/{p['post_id']}: {p.get('error', 'Unknown')}")
    else:
        print("\n✨ All 5 custom images generated successfully!")
        print("\nReady to upload and review:")
        for p in posts:
            print(f"   - Post {p['post_id']}: {p['title'][:50]}...")
        print()
        print("After review, full batch:")
        print("  export LAOZHANG_API_KEY='your-key'")
        print("  python3 /root/.openclaw/workspace/scripts/generate-images-custom.py")

if __name__ == '__main__':
    main()
