#!/usr/bin/env python3
"""
Convert Sawiday product JSON files to CSV with proper category mapping
Handles multiple JSON formats and uses embedded category when available
"""
import json
import csv
import urllib.request
from urllib.parse import urljoin
from typing import List, Dict, Any
import os

BASE_URL = "http://23.95.148.204:8081/"
OUTPUT_DIR = "/root/.openclaw/workspace/research/bathroom-products"
CSV_OUTPUT = os.path.join(OUTPUT_DIR, "sawiday-products.csv")

# Granular category mapping from Sawiday categories
SAWIDAY_CATEGORY_MAP = {
    # BATHTUBS - Granular
    'vrijstaande': 'baden-vrijstaande',
    'inbouw': 'baden-inbouw',
    'hoek': 'baden-hoek',

    # TOILETS - Granular (as-is since files are -alle)
    # Note: Current scraped data doesn't separate toilets granularly
}

def map_sawiday_category(sawiday_cat: str, filename_category: str) -> str:
    """Map Sawiday category to our granular category schema"""
    if not sawiday_cat:
        return filename_category  # Fallback to filename-based category

    sawiday_cat = sawiday_cat.lower()

    # Map Sawiday categories to granular categories
    if sawiday_cat in SAWIDAY_CATEGORY_MAP:
        return SAWIDAY_CATEGORY_MAP[sawiday_cat]

    # For standard categories, add -alle suffix if not already granular
    if sawiday_cat in ['douche', 'wastafels', 'kranen', 'spiegels', 'tegels']:
        return f"{sawiday_cat}-alle"

    # For baden/bathtubs without granular info
    if sawiday_cat in ['baden', 'bathtubs', 'bad']:
        return 'baden-alle'

    # For toilets
    if sawiday_cat in ['toiletten', 'toilet', 'toilets']:
        return 'toiletten-alle'

    # Fallback
    return filename_category

def map_category_from_filename(filename: str) -> str:
    """Map JSON filename to granular category (fallback)"""
    filename_lower = filename.lower()

    # Granular patterns
    if 'baden-vrijstaande' in filename_lower or 'bathtubs-vrijstaande' in filename_lower:
        return 'baden-vrijstaande'
    elif 'baden-inbouw' in filename_lower or 'bathtubs-inbouw' in filename_lower:
        return 'baden-inbouw'
    elif 'baden-hoek' in filename_lower or 'bathtubs-hoek' in filename_lower:
        return 'baden-hoek'

    # Broad patterns
    elif 'baden' in filename_lower or 'bathtubs' in filename_lower:
        return 'baden-alle'
    elif 'toiletten' in filename_lower:
        return 'toiletten-alle'
    elif 'douche' in filename_lower:
        return 'douche-alle'
    elif 'wastafels' in filename_lower:
        return 'wastafels-alle'
    elif 'kranen' in filename_lower:
        return 'kranen-alle'
    elif 'spiegels' in filename_lower:
        return 'spiegels-alle'
    elif 'tegels' in filename_lower:
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
                'sawiday_category': data.get('category', '')
            }

        # Handle format: array of products
        elif isinstance(data, list):
            return {
                'products': data,
                'sawiday_category': ''
            }

        return {'products': [], 'sawiday_category': ''}
    except Exception as e:
        print(f"Error downloading {filename}: {e}")
        return {'products': [], 'sawiday_category': ''}

def extract_product_fields(product: Dict, filename_category: str, sawiday_category: str) -> Dict:
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
            'category': map_sawiday_category(sawiday_category, filename_category)
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
            'category': map_sawiday_category(sawiday_category, filename_category)
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
        # Get filename-based category as fallback
        filename_category = map_category_from_filename(filename)

        print(f"⬇️  [{i:3d}/{len(files)}] {filename[:55]:<55}", end='')

        # Download and parse
        result = download_json(filename)
        products = result['products']
        sawiday_cat = result['sawiday_category']

        print(f" → {filename_category} (sawiday: '{sawiday_cat}')")

        for product in products:
            product_data = extract_product_fields(product, filename_category, sawiday_cat)
            prod_id = product_data['product_id']
            cat = product_data['category']

            if prod_id and prod_id not in seen_ids:
                seen_ids.add(prod_id)
                all_products.append(product_data)
                category_counts[cat] = category_counts.get(cat, 0) + 1
            elif not prod_id:
                all_products.append(product_data)
                category_counts[cat] = category_counts.get(cat, 0) + 1

        print(f"   → {len(products)} products")

    print(f"\n📊 Total unique products: {len(all_products)}")
    print(f"\n📂 Final category distribution:")
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
