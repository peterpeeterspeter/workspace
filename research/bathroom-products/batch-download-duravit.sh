#!/bin/bash

# Batch download Duravit images by category
# Goal: Fill gaps to reach ~100 products (200 images)

cd /root/.openclaw/workspace/research/bathroom-products

python3 << 'PYTHON_EOF'
import json
import subprocess
import os
import time
from urllib.parse import urlparse

with open('metadata/duravit-image-urls.json', 'r') as f:
    data = json.load(f)

# Categorize images by URL patterns
def categorize_image(url):
    url_lower = url.lower()
    if 'faucet' in url_lower or 'tap' in url_lower or 'mixer' in url_lower:
        return 'faucets'
    elif 'toilet' in url_lower or 'wc' in url_lower:
        return 'toilets'
    elif 'shower' in url_lower or 'rain' in url_lower:
        return 'showers'
    elif 'sink' in url_lower or 'basin' in url_lower or 'washbasin' in url_lower:
        return 'sinks'
    elif 'vanity' in url_lower or 'furniture' in url_lower or 'cabinet' in url_lower:
        return 'vanity'
    elif 'tile' in url_lower or 'ceramic' in url_lower:
        return 'tile'
    elif 'bath' in url_lower or 'tub' in url_lower:
        return 'bathtub'
    elif 'light' in url_lower or 'lamp' in url_lower or 'led' in url_lower:
        return 'lighting'
    else:
        return None

# Download with better error handling
def smart_download(images, category, tier, target=12):
    base_dir = f"raw-images/{category}/{tier}"
    os.makedirs(base_dir, exist_ok=True)
    
    downloaded = 0
    attempts = 0
    max_attempts = target * 3  # Try 3x more images than needed
    
    for img in images:
        if attempts >= max_attempts or downloaded >= target:
            break
        attempts += 1
        
        url = img['url']
        filename = url.split('/')[-1].split('?')[0][:50]
        filepath = f"{base_dir}/duravit-{filename}"
        
        if os.path.exists(filepath) or os.path.exists(filepath.replace('.jpg', '_1.jpg')):
            continue
        
        try:
            result = subprocess.run(
                ['wget', '-q', '-O', filepath, url, '--timeout=15', '--tries=2'],
                capture_output=True, timeout=20
            )
            if result.returncode == 0 and os.path.getsize(filepath) > 10000:  # >10KB
                downloaded += 1
                print(f"✓ {category}: {downloaded}/{target}")
            else:
                os.remove(filepath) if os.path.exists(filepath) else None
        except:
            pass
        
        time.sleep(0.3)
    
    return downloaded

# Process all images
categorized = {}
for img in data['images']:
    cat = categorize_image(img['url'])
    if cat and cat not in categorized:
        categorized[cat] = []
    if cat:
        categorized[cat].append(img)

# Download targets
targets = {
    'faucets': 6,
    'toilets': 4,
    'sinks': 6,
    'showers': 4,
    'vanity': 6,
    'tile': 4,
    'bathtub': 4,
    'lighting': 4
}

print("🚀 Batch downloading Duravit images...\n")

for category, target in targets.items():
    if category in categorized:
        count = smart_download(categorized[category], category, 'premium', target)
        print(f"  → {category}: {count} images\n")
    else:
        print(f"  ⚠ {category}: no images found\n")

print("\n✅ Batch download complete!")

PYTHON_EOF
