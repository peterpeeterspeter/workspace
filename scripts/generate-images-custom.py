#!/usr/bin/env python3
"""
Generate images using Laozhang.ai Nano Banana Pro (Gemini 3 Pro)
Using custom prompts tailored to each article
"""

import json
import os
import requests
import time
import base64

# Configuration
INPUT_FILE = '/root/.openclaw/workspace/temp/missing-images-custom.json'
OUTPUT_DIR = '/root/.openclaw/workspace/temp/images-custom'

# API Configuration
API_KEY = os.environ.get('LAOZHANG_API_KEY')
API_URL = 'https://api.laozhang.ai/v1beta/models/gemini-3-pro-image-preview:generateContent'

# Generation settings
ASPECT_RATIO = '16:9'
IMAGE_SIZE = '2K'

def generate_image(prompt, filename, alt_text, post_id):
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
        posts = json.load(f)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"🎬 Generating {len(posts)} custom images with Nano Banana Pro")
    print(f"Resolution: {IMAGE_SIZE} @ {ASPECT_RATIO}")
    print(f"Output: {OUTPUT_DIR}")
    print(f"API: {'✅' if API_KEY else '❌'}")
    print()

    if not API_KEY:
        print("❌ Set LAOZHANG_API_KEY")
        return 1

    cost_per_image = 0.05
    print(f"💰 ${cost_per_image}/image × {len(posts)} = ${len(posts) * cost_per_image:.2f}")
    print()

    success = 0
    failed = []

    for i, post in enumerate(posts, 1):
        print(f"[{i}/{len(posts)}] {post['site']}/{post['post_id']}")
        print(f"  {post['title'][:55]}...")

        prompt = post.get('custom_prompt', post['prompt'])
        print(f"  Focus: {prompt[:100]}...")

        try:
            filename = generate_image(prompt, post['filename'], post['alt_text'], post['post_id'])
            post['generated_image'] = filename
            post['status'] = 'generated'
            success += 1

            if i < len(posts):
                print(f"    ⏳ 10s...")
                time.sleep(10.0)

        except Exception as e:
            print(f"    ❌ {str(e)}")
            post['status'] = 'failed'
            post['error'] = str(e)
            failed.append(post)

        print()

    # Save results
    output_file = INPUT_FILE.replace('-custom.json', '-custom-generated.json')
    with open(output_file, 'w') as f:
        json.dump(posts, f, indent=2)

    print("=" * 50)
    print(f"✅ {success}/{len(posts)} generated")
    print(f"❌ {len(failed)} failed")
    print(f"📁 {output_file}")
    print()

    actual_cost = success * cost_per_image
    print(f"💰 Cost: ${actual_cost:.2f}")

    if failed:
        print("\nFailed:")
        for p in failed[:5]:
            print(f"  - {p['site']}/{p['post_id']}")
    else:
        print("\n✨ All custom images generated!")
        print("\nNext: Upload with")
        print("  python3 /root/.openclaw/workspace/scripts/upload-custom.py")

if __name__ == '__main__':
    main()
