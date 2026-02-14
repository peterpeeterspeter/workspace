#!/usr/bin/env python3
"""
Test image generation with first post only
"""

import json
import os
import requests
import urllib.request

# Configuration
API_KEY = os.environ.get('LAOZHANG_API_KEY')
API_BASE = os.environ.get('LAOZHANG_API_BASE', 'https://api.laozhang.ai/v1')
OUTPUT_DIR = '/root/.openclaw/workspace/temp/images'

# Load just first post
with open('/root/.openclaw/workspace/temp/missing-images.json', 'r') as f:
    posts = json.load(f)

test_post = posts[0]

print("🧪 Testing Laozhang.ai API with 1 image")
print("=" * 50)
print(f"Post: {test_post['title']}")
print(f"Prompt: {test_post['prompt'][:80]}...")
print(f"API Base: {API_BASE}")
print(f"API Key: {'✅ Configured' if API_KEY else '❌ Missing'}")
print()

if not API_KEY:
    print("❌ LAOZHANG_API_KEY not set!")
    exit(1)

try:
    print("Generating image...")
    print("  → Calling DALL-E 3 via Laozhang.ai...")

    # Generate image
    response = requests.post(
        f'{API_BASE}/images/generations',
        headers={
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        },
        json={
            'model': 'dall-e-3',
            'prompt': test_post['prompt'],
            'n': 1,
            'size': '1024x1792',
            'style': 'vivid'
        },
        timeout=60
    )

    if response.status_code != 200:
        error = response.json()
        raise Exception(f"API error {response.status_code}: {error.get('error', {}).get('message', 'Unknown error')}")

    # Get image URL
    data = response.json()
    image_url = data['data'][0]['url']
    print(f"  ✓ Image generated: {image_url[:60]}...")

    # Download image
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, test_post['filename'])
    urllib.request.urlretrieve(image_url, output_path)
    print(f"  ✓ Downloaded: {output_path}")

    # Optimize to WebP
    from PIL import Image
    img = Image.open(output_path)

    if img.mode != 'RGB':
        img = img.convert('RGB')

    webp_path = output_path.replace('.png', '.webp')
    img.save(webp_path, 'WEBP', quality=85, method=6)
    os.remove(output_path)

    size_kb = os.path.getsize(webp_path) / 1024
    print(f"  ✓ Optimized: {size_kb:.0f}KB WebP")

    print()
    print("✅ SUCCESS!")
    print()
    print("API key is working. Ready for full batch.")
    print(f"Cost for this test: ~$0.012")
    print(f"Estimated cost for all 49 images: ${49 * 0.012:.2f}")
    print()
    print("Ready to generate all 49 images? (y/n)")

except Exception as e:
    print()
    print(f"❌ FAILED: {e}")
    exit(1)
