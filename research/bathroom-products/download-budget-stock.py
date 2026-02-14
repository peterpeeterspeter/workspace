#!/usr/bin/env python3
"""
Download budget-tier bathroom product images from free stock sources
Naming: essential-line-[category]-[product-number].jpg
"""

import requests
import os
import time
import urllib.parse

# Use public domain image URLs (Wikimedia, Pixabay public URLs, etc.)
STOCK_IMAGE_URLS = {
    'vanity': [
        'https://images.unsplash.com/photo-1552321554-5fefe8c9ef14?w=800&q=80',
        'https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=800&q=80',
        'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&q=80',
    ],
    'faucets': [
        'https://images.unsplash.com/photo-1585704032915-c3400ca199e7?w=800&q=80',
        'https://images.unsplash.com/photo-1604762584865-43b6e2b9b5d5?w=800&q=80',
    ],
    'toilets': [
        'https://images.unsplash.com/photo-1620626011761-996317b8d101?w=800&q=80',
        'https://images.unsplash.com/photo-1552321554-5fefe8c9ef14?w=800&q=80',
    ],
    'showers': [
        'https://images.unsplash.com/photo-1552321554-5fefe8c9ef14?w=800&q=80',
        'https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?w=800&q=80',
    ],
    'bathtub': [
        'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800&q=80',
        'https://images.unsplash.com/photo-1600566752355-35792bedcfea?w=800&q=80',
    ],
    'tile': [
        'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&q=80',
        'https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=800&q=80',
    ],
    'lighting': [
        'https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=800&q=80',
        'https://images.unsplash.com/photo-1565814329452-e1efa11c5b89?w=800&q=80',
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
        print(f"Error downloading {url}: {e}")
    return False

def main():
    base_dir = "/root/.openclaw/workspace/research/bathroom-products/raw-images"

    total_downloaded = 0

    for category, urls in STOCK_IMAGE_URLS.items():
        category_dir = f"{base_dir}/{category}/budget"
        os.makedirs(category_dir, exist_ok=True)

        print(f"\n{category.upper()}:")

        for i, url in enumerate(urls, 1):
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

            time.sleep(0.5)  # Be respectful

    print(f"\n✅ Downloaded {total_downloaded} budget-tier images")

if __name__ == "__main__":
    main()
