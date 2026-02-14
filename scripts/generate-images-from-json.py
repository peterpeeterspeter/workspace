#!/usr/bin/env python3
"""
Generate images using DALL-E 3 from missing-images.json
"""

import json
import os
import requests
import time
import urllib.request

# Configuration
INPUT_FILE = '/root/.openclaw/workspace/temp/missing-images.json'
OUTPUT_DIR = '/root/.openclaw/workspace/temp/images'
API_KEY = os.environ.get('OPENAI_API_KEY')

def generate_image_dalle(prompt, filename, alt_text):
    """Generate image using DALL-E 3 API"""
    
    if not API_KEY:
        raise Exception("OPENAI_API_KEY environment variable not set")
    
    # Generate image
    response = requests.post(
        'https://api.openai.com/v1/images/generations',
        headers={
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        },
        json={
            'model': 'dall-e-3',
            'prompt': prompt,
            'n': 1,
            'size': '1024x1792',  # Portrait (best for featured images)
            'style': 'vivid'
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
    # (requires: pip install Pillow)
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
    
    print(f"🎨 Generating {len(posts)} images with DALL-E 3")
    print(f"Output: {OUTPUT_DIR}")
    print(f"API: {'✅ Configured' if API_KEY else '❌ Missing OPENAI_API_KEY'}")
    print()
    
    if not API_KEY:
        print("❌ ERROR: OPENAI_API_KEY not set")
        print("   Run: export OPENAI_API_KEY='your-key-here'")
        return 1
    
    # Process each post
    success_count = 0
    failed_posts = []
    
    for i, post in enumerate(posts, 1):
        print(f"[{i}/{len(posts)}] {post['site']} - Post {post['post_id']}")
        print(f"  Title: {post['title'][:60]}...")
        print(f"  Prompt: {post['prompt'][:80]}...")
        
        try:
            # Generate image
            filename = generate_image_dalle(post['prompt'], post['filename'], post['alt_text'])
            
            # Update post with generated filename
            post['generated_image'] = filename
            post['status'] = 'generated'
            
            success_count += 1
            
            # Rate limiting (DALL-E 3: ~50 images/minute)
            if i < len(posts):
                time.sleep(1.2)
            
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
    
    if failed_posts:
        print("Failed posts:")
        for post in failed_posts:
            print(f"  - {post['site']}/{post['post_id']}: {post['error']}")
    
    print()
    print("🚀 Next step: Upload images")
    print(f"   ./upload-images.py {output_file}")

if __name__ == '__main__':
    main()
