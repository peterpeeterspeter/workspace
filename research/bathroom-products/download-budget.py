#!/usr/bin/env python3
"""
Download budget-tier bathroom product images from free sources
Naming: essential-line-[category]-[product].jpg
"""

import requests
import os
import time
import json

# Pixabay API (free, no key needed for basic search)
PIXABAY_URL = "https://pixabay.com/api/"

# Categories and search terms
CATEGORIES = {
    'faucets': ['bathroom faucet', 'kitchen tap', 'water tap'],
    'toilets': ['toilet', 'wc', 'bathroom toilet'],
    'showers': ['shower', 'shower head', 'rain shower'],
    'vanity': ['bathroom vanity', 'sink cabinet', 'washbasin'],
    'tile': ['bathroom tiles', 'wall tiles'],
    'lighting': ['bathroom light', 'vanity light', 'mirror light'],
    'bathtub': ['bathtub', 'bath tub']
}

def download_image(url, filepath):
    """Download image from URL"""
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(response.content)
            return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
    return False

def main():
    base_dir = "/root/.openclaw/workspace/research/bathroom-products/raw-images"

    # Download 3-4 images per category for budget tier
    for category, search_terms in CATEGORIES.items():
        category_dir = f"{base_dir}/{category}/budget"
        os.makedirs(category_dir, exist_ok=True)

        count = 0
        target = 3 if category != 'faucets' else 4

        # For demo, use placeholder approach
        # In production, would use actual APIs
        print(f"Budget {category}: {count}/{target} (skipping - need API key)")

    print("\nNote: Budget tier requires free image source with API access")
    print("Options: Pixabay (free key), Unsplash API, or Pexels API")

if __name__ == "__main__":
    main()
