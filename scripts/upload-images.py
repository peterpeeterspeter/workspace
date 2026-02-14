#!/usr/bin/env python3
"""
Upload generated images to WordPress posts via pinch-to-post
"""

import json
import os
import subprocess

# Configuration
INPUT_FILE = '/root/.openclaw/workspace/temp/missing-images-generated.json'
PINCH_SCRIPT = '/root/.openclaw/workspace/scripts/publish-gateway.sh'

def upload_image(site, image_path, alt_text, post_id):
    """Upload image via pinch-to-post"""
    
    # Get site credentials
    sites = {
        'crashcasino': 'crashcasino',
        'crashgame': 'crashgame',
        'freecrash': 'freecrash',
        'cryptocrash': 'cryptocrash'
    }
    
    site_key = sites.get(site)
    if not site_key:
        return False, f"Unknown site: {site}"
    
    # Build command
    cmd = [
        PINCH_SCRIPT,
        'media-upload',
        site_key,
        image_path,
        alt_text,
        '',  # caption (empty)
        str(post_id)
    ]
    
    # Run command
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
            
    except subprocess.TimeoutExpired:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)

def main():
    # Load JSON
    with open(INPUT_FILE, 'r') as f:
        posts = json.load(f)
    
    # Filter posts with generated images
    ready_posts = [p for p in posts if p.get('status') == 'generated' and p.get('generated_image')]
    
    print(f"📤 Uploading {len(ready_posts)} images to WordPress")
    print()
    
    success_count = 0
    failed_posts = []
    
    for i, post in enumerate(ready_posts, 1):
        image_path = os.path.join('/root/.openclaw/workspace/temp/images', post['generated_image'])
        
        # Check if image exists
        if not os.path.exists(image_path):
            print(f"[{i}/{len(ready_posts)}] ❌ Image not found: {image_path}")
            post['upload_status'] = 'failed'
            post['upload_error'] = 'Image file not found'
            failed_posts.append(post)
            continue
        
        print(f"[{i}/{len(ready_posts)}] {post['site']} - Post {post['post_id']}")
        print(f"  Image: {post['generated_image']}")
        print(f"  Alt: {post['alt_text'][:60]}...")
        
        # Upload
        success, output = upload_image(
            post['site'],
            image_path,
            post['alt_text'],
            post['post_id']
        )
        
        if success:
            print(f"  ✅ Uploaded")
            post['upload_status'] = 'uploaded'
            success_count += 1
        else:
            print(f"  ❌ Failed: {output}")
            post['upload_status'] = 'failed'
            post['upload_error'] = output
            failed_posts.append(post)
        
        print()
    
    # Save updated JSON
    output_file = INPUT_FILE.replace('-generated.json', '-uploaded.json')
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
    
    print()
    print("✨ Done! Featured images have been added.")

if __name__ == '__main__':
    main()
