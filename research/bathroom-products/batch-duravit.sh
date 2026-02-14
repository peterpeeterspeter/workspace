#!/bin/bash

# Batch download Duravit images by category
cd /root/.openclaw/workspace/research/bathroom-products

python3 << 'PYEOF'
import json
import subprocess
import os
import time

with open('metadata/duravit-image-urls.json', 'r') as f:
    data = json.load(f)

def categorize(url):
    url = url.lower()
    if 'faucet' in url or 'tap' in url or 'mixer' in url:
        return 'faucets'
    elif 'toilet' in url or 'wc' in url:
        return 'toilets'
    elif 'shower' in url or 'rain' in url:
        return 'showers'
    elif 'sink' in url or 'basin' in url or 'washbasin' in url:
        return 'sinks'
    elif 'vanity' in url or 'furniture' in url or 'cabinet' in url:
        return 'vanity'
    elif 'tile' in url or 'ceramic' in url:
        return 'tile'
    elif 'bath' in url or 'tub' in url:
        return 'bathtub'
    elif 'light' in url or 'lamp' in url or 'led' in url:
        return 'lighting'
    return None

categorized = {}
for img in data['images']:
    cat = categorize(img['url'])
    if cat and cat not in categorized:
        categorized[cat] = []
    if cat:
        categorized[cat].append(img)

def download(images, category, tier, target=8):
    base_dir = f"raw-images/{category}/{tier}"
    os.makedirs(base_dir, exist_ok=True)
    
    downloaded = 0
    for img in images[:target*3]:
        if downloaded >= target:
            break
        url = img['url']
        filename = url.split('/')[-1].split('?')[0][:40]
        filepath = f"{base_dir}/duravit-{filename}"
        
        if os.path.exists(filepath):
            continue
        
        try:
            subprocess.run(['wget', '-q', '-O', filepath, url, '--timeout=10'], 
                         capture_output=True, timeout=15)
            if os.path.exists(filepath) and os.path.getsize(filepath) > 10000:
                downloaded += 1
                print(f"{category}: {downloaded}/{target}")
        except:
            pass
        time.sleep(0.2)
    
    return downloaded

print("Downloading Duravit batch...")

for cat in ['faucets','toilets','sinks','showers','vanity','tile','bathtub']:
    if cat in categorized:
        download(categorized[cat], cat, 'premium', 6)

print("Done!")
PYEOF
