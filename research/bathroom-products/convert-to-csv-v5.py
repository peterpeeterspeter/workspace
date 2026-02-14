#!/usr/bin/env python3
"""
Convert Sawiday product JSON files to CSV with proper granular category mapping
Handles multiple JSON formats and prioritizes granular categories
"""
import json
import csv
import urllib.request
from urllib.parse import urljoin
from typing import List, Dict, Any
import os
import re

BASE_URL = "http://23.95.148.204:8081/"
OUTPUT_DIR = "/root/.openclaw/workspace/research/bathroom-products"
CSV_OUTPUT = os.path.join(OUTPUT_DIR, "sawiday-products.csv")

# Priority-based category mapping (higher priority = more specific)
CATEGORY_PRIORITY = {
    # Highest priority: Granular bathtubs
    'baden-inbouw': 100,
    'bathtubs-inbouw': 100,
    'baden-hoek': 100,
    'bathtubs-hoek': 100,
    'baden-vrijstaande': 100,
    'bathtubs-vrijstaande': 100,
    'bathtubs-half-vrijstaande': 95,  # Map to vrijstaande
    'bathtubs-whirlpool': 90,  # Map to baden-alle

    # Broad categories (lower priority)
    'baden-alle': 50,
    'bathtubs-alle': 50,
    'baden': 50,
    'bathtubs': 50,
    'toiletten-alle': 50,
    'toiletten': 50,
    'douche-alle': 50,
    'douche': 50,
    'wastafels-alle': 50,
    'wastafels': 50,
    'kranen-alle': 50,
    'kranen': 50,
    'spiegels-alle': 50,
    'spiegels': 50,
    'tegels-alle': 50,
    'tegels': 50,
}

def map_category_from_filename(filename: str) -> tuple[str, int]:
    """Map JSON filename to (category, priority)"""
    filename_lower = filename.lower()

    # Check all patterns, return highest priority match
    best_match = ('other', 0)

    for pattern, priority in CATEGORY_PRIORITY.items():
        if pattern in filename_lower:
            if priority > best_match[1]:
                best_match = (pattern, priority)

    return best_match

def normalize_category(category: str) -> str:
    """Normalize category name to final schema"""
    category = category.lower()

    # Granular bathtubs
    if 'bathtubs-inbouw' in category or 'baden-inbouw' in category:
        return 'baden-inbouw'
    elif 'bathtubs-hoek' in category or 'baden-hoek' in category:
        return 'baden-hoek'
    elif 'bathtubs-half-vrijstaande' in category or 'baden-half-vrijstaande' in category:
        return 'baden-vrijstaande'
    elif 'bathtubs-vrijstaande' in category or 'baden-vrijstaande' in category:
        return 'baden-vrijstaande'
    elif 'bathtubs-whirlpool' in category or 'baden-whirlpool' in category:
        return 'baden-alle'

    # Broad categories
    elif 'baden-alle' in category or 'bathtubs-alle' in category:
        return 'baden-alle'
    elif 'baden' in category or 'bathtubs' in category:
        return 'baden-alle'
    elif 'toiletten-alle' in category or 'toiletten' in category:
        return 'toiletten-alle'
    elif 'douche-alle' in category or 'douche' in category:
        return 'douche-alle'
    elif 'wastafels-alle' in category or 'wastafels' in category:
        return 'wastafels-alle'
    elif 'kranen-alle' in category or 'kranen' in category:
        return 'kranen-alle'
    elif 'spiegels' in category:
        return 'spiegels-alle'
    elif 'tegels' in category:
        return 'tegels-alle'

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

def download_json(filename: str) -> Any:
    """Download and parse a JSON file (handles multiple formats)"""
    url = urljoin(BASE_URL, filename)
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode('utf-8'))

        # Handle format: {category: "...", products: [...]}
        if isinstance(data, dict) and 'products' in data:
            return {
                'products': data.get('products', []),
                'sawiday_category': data.get('category', ''),
                'total_products': data.get('total_products', len(data.get('products', [])))
            }

        # Handle format: array of products
        elif isinstance(data, list):
            return {
                'products': data,
                'sawiday_category': '',
                'total_products': len(data)
            }

        return {'products': [], 'sawiday_category': '', 'total_products': 0}
    except Exception as e:
        print(f"Error downloading {filename}: {e}")
        return {'products': [], 'sawiday_category': '', 'total_products': 0}

def extract_product_fields(product: Dict, category: str) -> Dict:
    """Extract and normalize product fields (handles multiple formats)"""

    # Format 1: Standard sawiday-all-* format
    if 'product_url' in product:
        return {
            'name': product.get('name', ''),
            'brand': product.get('brand', ''),
            'product_id': product.get('sawiday_id', ''),
            'price_eur': product.get('price', ''),
            'url': product.get('product_url', ''),
            'image_url': product.get('image_url', ''),
            'category': category
        }

    # Format 2: Standard sawiday-{category}-* format
    else:
        return {
            'name': product.get('name', ''),
            'brand': product.get('brand', ''),
            'product_id': product.get('product_id', ''),
            'price_eur': product.get('price_eur', ''),
            'url': product.get('url', ''),
            'image_url': product.get('image_url', ''),
            'category': category
        }

def main():
    print("🔍 Listing Sawiday JSON files...")
    files = list_sawiday_files()
    print(f"   Found {len(files)} files\n")

    if not files:
        print("❌ No files found!")
        return

    # Track categories and their file sources
    category_files = {}  # category -> [(filename, product_count)]

    all_products = []
    seen_ids = {}  # product_id -> priority (highest wins)

    for i, filename in enumerate(files, 1):
        # Get filename-based category
        file_category_raw, priority = map_category_from_filename(filename)
        category = normalize_category(file_category_raw)

        result = download_json(filename)
        products = result['products']
        total = result['total_products']

        # Track category sources
        if total > 0:
            if category not in category_files:
                category_files[category] = []
            category_files[category].append((filename, total))

        print(f"⬇️  [{i:3d}/{len(files)}] {filename[:55]:<55} → {category} (prio:{priority}) ({total} products)")

        for product in products:
            product_data = extract_product_fields(product, category)
            prod_id = product_data['product_id']

            if prod_id:
                # Only add if not seen, or if this is higher priority
                if prod_id not in seen_ids:
                    seen_ids[prod_id] = priority
                    all_products.append(product_data)
                elif priority > seen_ids.get(prod_id, 0):
                    # Replace with higher priority product
                    # Find and remove existing
                    for idx, p in enumerate(all_products):
                        if p.get('product_id') == prod_id:
                            all_products[idx] = product_data
                            seen_ids[prod_id] = priority
                            break
            else:
                # No ID, just add
                all_products.append(product_data)

    print(f"\n📊 Total unique products: {len(all_products)}")

    print(f"\n📂 Category breakdown by source files:")
    for cat in sorted(category_files.keys()):
        files_list = category_files[cat]
        total_products = sum(f[1] for f in files_list)
        print(f"\n   {cat}: {total_products} products from {len(files_list)} file(s)")
        for fname, count in files_list:
            print(f"      - {fname}: {count}")

    # Final category counts
    category_counts = {}
    for p in all_products:
        cat = p['category']
        category_counts[cat] = category_counts.get(cat, 0) + 1

    print(f"\n📂 Final category distribution in CSV:")
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
