#!/usr/bin/env python3
"""
Convert Sawiday product JSON files to CSV with proper category mapping
Maps categories based on JSON filename patterns to granular categories
"""
import json
import csv
import urllib.request
from urllib.parse import urljoin
from typing import List, Dict
import os
import re

BASE_URL = "http://23.95.148.204:8081/"
OUTPUT_DIR = "/root/.openclaw/workspace/research/bathroom-products"
CSV_OUTPUT = os.path.join(OUTPUT_DIR, "sawiday-products.csv")

# Granular category mapping from filename patterns
CATEGORY_MAP = {
    # BATHTUBS - Granular
    'baden-vrijstaande': 'baden-vrijstaande',
    'bathtubs-vrijstaande': 'baden-vrijstaande',
    'baden-inbouw': 'baden-inbouw',
    'bathtubs-inbouw': 'baden-inbouw',
    'baden-hoek': 'baden-hoek',
    'bathtubs-hoek': 'baden-hoek',
    'bathtubs-half-vrijstaande': 'baden-vrijstaande',  # Map half to vrijstaande
    'bathtubs-whirlpool': 'baden-alle',  # Catch-all
    
    # Catch-all for bathtubs
    'bathtubs-alle': 'baden-alle',
    'bathtubs': 'baden-alle',
    'baden': 'baden-alle',
    
    # TOILETTEN - Granular
    'toiletten-wandclosets': 'toiletten-wandclosets',
    'toiletten-staande': 'toiletten-staande',
    'toiletten-inbouwsets': 'toiletten-inbouwsets',
    
    # Catch-all for toilets
    'toiletten-alle': 'toiletten-alle',
    'toiletten': 'toiletten-alle',
    
    # SHOWERS, VANITIES, FAUCETS - Non-granular (use -alle)
    'douche-alle': 'douche-alle',
    'douche': 'douche-alle',
    'wastafels-alle': 'wastafels-alle',
    'wastafels': 'wastafels-alle',
    'kranen-alle': 'kranen-alle',
    'kranen': 'kranen-alle',
    
    # Other categories
    'spiegels': 'spiegels-alle',
    'tegels': 'tegels-alle',
}

def map_category_from_filename(filename: str) -> str:
    """Map JSON filename to granular category"""
    filename_lower = filename.lower()

    # Try exact patterns first
    for pattern, category in CATEGORY_MAP.items():
        if pattern in filename_lower:
            return category

    # Default fallback
    return 'other'

def list_sawiday_files() -> List[str]:
    """List all sawiday JSON files on the server"""
    try:
        with urllib.request.urlopen(BASE_URL) as response:
            html = response.read().decode('utf-8')

        files = []
        for line in html.split('\n'):
            if 'sawiday' in line and '.json' in line:
                start = line.find('href="') + 6
                end = line.find('.json"', start)
                if start > 5 and end > start:
                    filename = line[start:end+5]
                    if filename.startswith('sawiday'):
                        files.append(filename)
        return sorted(set(files))
    except Exception as e:
        print(f"Error listing files: {e}")
        return []

def download_json(filename: str) -> List[Dict]:
    """Download and parse a JSON file"""
    url = urljoin(BASE_URL, filename)
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode('utf-8'))
        return data if isinstance(data, list) else []
    except Exception as e:
        print(f"Error downloading {filename}: {e}")
        return []

def extract_product_fields(product: Dict, source_category: str) -> Dict:
    """Extract and normalize product fields"""
    return {
        'name': product.get('name', ''),
        'brand': product.get('brand', ''),
        'product_id': product.get('product_id', ''),
        'price_eur': product.get('price_eur', ''),
        'url': product.get('url', ''),
        'image_url': product.get('image_url', ''),
        'category': source_category
    }

def main():
    print("🔍 Listing Sawiday JSON files...")
    files = list_sawiday_files()
    print(f"   Found {len(files)} files\n")

    if not files:
        print("❌ No files found!")
        return

    all_products = []
    seen_ids = set()
    category_counts = {}

    for i, filename in enumerate(files, 1):
        # Map category from filename
        category = map_category_from_filename(filename)
        category_counts[category] = category_counts.get(category, 0) + 0  # Init counter

        print(f"⬇️  [{i}/{len(files)}] {filename[:50]:<50} → {category}")
        products = download_json(filename)

        for product in products:
            product_data = extract_product_fields(product, category)
            prod_id = product_data['product_id']

            if prod_id and prod_id not in seen_ids:
                seen_ids.add(prod_id)
                all_products.append(product_data)
                category_counts[category] = category_counts.get(category, 0) + 1
            elif not prod_id:
                all_products.append(product_data)
                category_counts[category] = category_counts.get(category, 0) + 1

        print(f"   → {len(products)} products")

    print(f"\n📊 Total unique products: {len(all_products)}")
    print(f"\n📂 Category distribution:")
    for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"   {cat}: {count}")

    # Write to CSV
    if all_products:
        fieldnames = ['product_id', 'name', 'brand', 'price_eur', 'url', 'image_url', 'category']

        with open(CSV_OUTPUT, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_products)

        print(f"\n✅ CSV created: {CSV_OUTPUT}")
        print(f"   File size: {os.path.getsize(CSV_OUTPUT):,} bytes")
    else:
        print("❌ No products to write!")

if __name__ == "__main__":
    main()
