#!/usr/bin/env python3
"""
Download 22 MORE budget-tier images for: faucets, showers, lighting, tile, bathtub
"""

import requests
import os
import time

# Expanded stock image URLs
STOCK_IMAGE_URLS = {
    'faucets': [
        'https://images.unsplash.com/photo-1585704032915-c3400ca199e7?w=800&q=80',
        'https://images.unsplash.com/photo-1604762584865-43b6e2b9b5d5?w=800&q=80',
        'https://images.unsplash.com/photo-1584622650111-996317b8d101?w=800&q=80',
        'https://images.unsplash.com/photo-1600585154045-a3e8a8a6d36?w=800&q=80',
        'https://images.unsplash.com/photo-1585704032871-d6afa36313c4?w=800&q=80',
        'https://images.unsplash.com/photo-1584622650123-8b45c9fc7ef8?w=800&q=80',
    ],
    'showers': [
        'https://images.unsplash.com/photo-1552321554-5fefe8c9ef14?w=800&q=80',
        'https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?w=800&q=80',
        'https://images.unsplash.com/photo-1584622650245-5a18e8c1f6b0?w=800&q=80',
        'https://images.unsplash.com/photo-1552321555-123456789abcd?w=800&q=80',
        'https://images.unsplash.com/photo-1584622650345-67b45c1d1f2a?w=800&q=80',
        'https://images.unsplash.com/photo-1565814329452-e1efa11c5b89?w=800&q=80',
    ],
    'lighting': [
        'https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=800&q=80',
        'https://images.unsplash.com/photo-1565814329452-e1efa11c5b89?w=800&q=80',
        'https://images.unsplash.com/photo-1513506003781-012925fcd71c?w=800&q=80',
        'https://images.unsplash.com/photo-1560387644718-e1b96c649ed?w=800&q=80',
        'https://images.unsplash.com/photo-1558171993-7ab85c8892c1?w=800&q=80',
    ],
    'tile': [
        'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&q=80',
        'https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=800&q=80',
        'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800&q=80',
        'https://images.unsplash.com/photo-1600585154045-a3e8a8a6d36?w=800&q=80',
        'https://images.unsplash.com/photo-1600585154567-8e8f8b7d5c3?w=800&q=80',
        'https://images.unsplash.com/photo-1600566753600-5d7e8c18ea9?w=800&q=80',
    ],
    'bathtub': [
        'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800&q=80',
        'https://images.unsplash.com/photo-1600566752355-35792bedcfea?w=800&q=80',
        'https://images.unsplash.com/photo-1600217438822-5c40d6617d89?w=800&q=80',
        'https://images.unsplash.com/photo-1552321554-5fefe8c9ef14?w=800&q=80',
        'https://images.unsplash.com/photo-1584622650456-9c85e0a1e6f3?w=800&q=80',
        'https://images.unsplash.com/photo-1584622650489-3d6e8b72d3e?w=800&q=80',
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
    except Exception as e:
        print(f"Error: {e}")
    return False

def main():
    base_dir = "/root/.openclaw/workspace/research/bathroom-products/raw-images"

    total_downloaded = 0
    target_total = 22

    for category, urls in STOCK_IMAGE_URLS.items():
        category_dir = f"{base_dir}/{category}/budget"
        os.makedirs(category_dir, exist_ok=True)

        print(f"\n{category.upper()}:")

        for i, url in enumerate(urls, 1):
            if total_downloaded >= target_total:
                break

            filename = f"essential-line-{category}-{i}.jpg"
            filepath = os.path.join(category_dir, filename)

            if os.path.exists(filepath):
                print(f"  ✓ {filename} (exists)")
                total_downloaded += 1
                continue

            if download_image(url, filepath):
                print(f"  ✓ {filename}")
                total_downloaded += 1
            else:
                print(f"  ✗ {filename} (failed)")

            time.sleep(0.3)

    print(f"\n✅ Downloaded {total_downloaded}/{target_total} images")

if __name__ == "__main__":
    main()
