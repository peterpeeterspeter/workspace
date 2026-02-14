#!/usr/bin/env python3
"""
Final push: Download remaining budget images to reach 22 total
"""

import requests
import os
import time

# More stock photo URLs for remaining images
FINAL_STOCK_URLS = {
    'faucets': [
        'https://images.unsplash.com/photo-1585704032863-9208c82588a0?w=800&q=80',
        'https://images.unsplash.com/photo-1585704032956-8a9c5d72f8f0?w=800&q=80',
        'https://images.unsplash.com/photo-1585704032915-c3400ca199e7?w=800&q=80',
    ],
    'showers': [
        'https://images.unsplash.com/photo-1565814329471-e1efa11c5b89?w=800&q=80',
        'https://images.unsplash.com/photo-1584622650245-5a18e8c1f6b0?w=800&q=80',
        'https://images.unsplash.com/photo-1584622650345-67b45c1d1f2a?w=800&q=80',
    ],
    'lighting': [
        'https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=800&q=80',
        'https://images.unsplash.com/photo-1513506003781-012925fcd71c?w=800&q=80',
        'https://images.unsplash.com/photo-1558171993-7ab85c8892c1?w=800&q=80',
    ],
    'tile': [
        'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&q=80',
        'https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=800&q=80',
        'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800&q=80',
    ],
    'bathtub': [
        'https://images.unsplash.com/photo-1600217438822-5c40d6617d89?w=800&q=80',
        'https://images.unsplash.com/photo-1584622650456-9c85e0a1e6f3?w=800&q=80',
        'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&q=80',
    ]
}

def download_image(url, filepath):
    """Download image from URL"""
    try:
        response = requests.get(url, timeout=20, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(response.content)
            return True
    except:
        pass
    return False

def main():
    base_dir = "/root/.openclaw/workspace/research/bathroom-products/raw-images"
    target = 22
    current_budget = len([f for f in os.walk(base_dir) for f in f[2] if f.endswith('.jpg') and 'budget' in f[0]])
    need = target - current_budget

    print(f"Current budget images: {current_budget}")
    print(f"Need: {need} more")
    print(f"Target: {target}\n")

    downloaded = 0
    cat_num = 1

    for category, urls in FINAL_STOCK_URLS.items():
        if downloaded >= need:
            break

        category_dir = f"{base_dir}/{category}/budget"
        os.makedirs(category_dir, exist_ok=True)

        for url in urls:
            if downloaded >= need:
                break

            # Find next available number
            existing = [f for f in os.listdir(category_dir) if f.startswith('essential-line') and f.endswith('.jpg')]
            next_num = len(existing) + 1
            filename = f"essential-line-{category}-{next_num}.jpg"
            filepath = os.path.join(category_dir, filename)

            if download_image(url, filepath):
                downloaded += 1
                print(f"✓ {category}/{filename}")
            else:
                print(f"✗ Failed: {category}")

            time.sleep(0.3)

    print(f"\n✅ Downloaded {downloaded}/{need} budget images")

if __name__ == "__main__":
    main()
