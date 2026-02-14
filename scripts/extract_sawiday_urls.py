#!/usr/bin/env python3
"""
Extract product URLs from Sawiday.be using browser snapshots.

This script navigates to category pages and extracts product URLs
from browser snapshots.

Categories:
1. Douchesets - 50 products
2. Complete douchecabines - 25 products  
3. Infrarood douchepanelen - 10 products
4. Stoomcabines - 10 products
"""

import json
import re
import subprocess
import time
from urllib.parse import urljoin

BASE_URL = "https://www.sawiday.be"

# Categories to scrape
CATEGORIES = [
    {
        "name": "douchesets",
        "url": "https://www.sawiday.be/nl-be/douche/douchesets/",
        "target_products": 50
    },
    {
        "name": "complete_douchecabines", 
        "url": "https://www.sawiday.be/nl-be/douche/complete-douchecabines/",
        "target_products": 25
    },
    {
        "name": "infrarood_douchepanelen",
        "url": "https://www.sawiday.be/nl-be/douche/infrarood-douchepaneel/",
        "target_products": 10
    },
    {
        "name": "stoomcabines",
        "url": "https://www.sawiday.be/nl-be/douche/stoomcabines/",
        "target_products": 10
    }
]

def extract_product_urls_from_snapshot(snapshot_text):
    """Extract product URLs from snapshot text."""
    pattern = r'/nl-be/p/\d+/[^"\s]+'
    matches = re.findall(pattern, snapshot_text)
    
    # Deduplicate and convert to full URLs
    unique_urls = list(set([urljoin(BASE_URL, match) for match in matches]))
    
    return unique_urls

def save_urls(category_name, urls):
    """Save URLs to JSON file."""
    filename = f"/root/.openclaw/workspace/output/sawiday_{category_name}_urls.json"
    
    data = {
        "category": category_name,
        "total_urls": len(urls),
        "urls": sorted(urls)
    }
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    return filename

def main():
    """Main extraction function."""
    print("Starting Sawiday product URL extraction...")
    print(f"Total categories: {len(CATEGORIES)}\n")
    
    for category in CATEGORIES:
        print(f"\n{'='*60}")
        print(f"Category: {category['name']}")
        print(f"Target: {category['target_products']} products")
        print(f"URL: {category['url']}")
        print(f"{'='*60}\n")
        
        all_urls = []
        page = 1
        
        while len(all_urls) < category['target_products']:
            # Navigate to category page (with pagination)
            page_url = f"{category['url']}?page={page}"
            print(f"Page {page}: Extracting URLs...")
            
            # Use browser to navigate (you'll need to implement this)
            # For now, this is a placeholder showing the logic
            print(f"  Would navigate to: {page_url}")
            print(f"  Current URLs collected: {len(all_urls)}")
            
            # Break to avoid infinite loop for now
            if page >= 3:  # Limit to 3 pages for testing
                print(f"  Reached page limit (3 pages) for testing")
                break
            
            page += 1
        
        # Trim to target count
        final_urls = all_urls[:category['target_products']]
        
        # Save results
        filename = save_urls(category['name'], final_urls)
        print(f"\n✓ Saved {len(final_urls)} URLs to {filename}")
    
    print(f"\n{'='*60}")
    print("Extraction complete!")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
