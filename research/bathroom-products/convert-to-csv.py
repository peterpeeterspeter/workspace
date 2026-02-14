#!/usr/bin/env python3
"""
Convert Sawiday product JSON files to CSV
Downloads all sawiday JSON files from the HTTP server and creates a single CSV
"""
import json
import csv
import urllib.request
from urllib.parse import urljoin
from typing import List, Dict
import os

BASE_URL = "http://23.95.148.204:8081/"
OUTPUT_DIR = "/root/.openclaw/workspace/research/bathroom-products"
CSV_OUTPUT = os.path.join(OUTPUT_DIR, "sawiday-products.csv")

def list_sawiday_files() -> List[str]:
    """List all sawiday JSON files on the server"""
    try:
        with urllib.request.urlopen(BASE_URL) as response:
            html = response.read().decode('utf-8')
        # Extract sawiday JSON filenames
        files = []
        for line in html.split('\n'):
            if 'sawiday' in line and '.json' in line:
                # Extract filename from href
                start = line.find('href="') + 6
                end = line.find('.json"', start)
                if start > 5 and end > start:
                    filename = line[start:end+5]  # Include .json
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

def extract_product_fields(product: Dict) -> Dict:
    """Extract and normalize product fields"""
    return {
        'name': product.get('name', ''),
        'brand': product.get('brand', ''),
        'product_id': product.get('product_id', ''),
        'price_eur': product.get('price_eur', ''),
        'url': product.get('url', ''),
        'image_url': product.get('image_url', ''),
        'category': filename_to_category(product.get('url', ''))
    }

def filename_to_category(url: str) -> str:
    """Extract category from URL or filename"""
    # Try to infer category from URL path
    if '/baden/' in url or 'baden' in url.lower():
        return 'bathtubs'
    elif '/wastafels/' in url or 'wastafel' in url.lower():
        return 'sinks'
    elif '/douche/' in url or 'douche' in url.lower():
        return 'showers'
    elif '/kranen/' in url or 'kraan' in url.lower():
        return 'faucets'
    return 'other'

def main():
    print("🔍 Listing Sawiday JSON files...")
    files = list_sawiday_files()
    print(f"   Found {len(files)} files\n")
    
    if not files:
        print("❌ No files found!")
        return
    
    all_products = []
    seen_ids = set()
    
    for i, filename in enumerate(files, 1):
        print(f"⬇️  [{i}/{len(files)}] Downloading {filename}...")
        products = download_json(filename)
        
        # Extract fields and track unique products
        for product in products:
            product_data = extract_product_fields(product)
            prod_id = product_data['product_id']
            
            # Skip duplicates by product_id
            if prod_id and prod_id not in seen_ids:
                seen_ids.add(prod_id)
                all_products.append(product_data)
            elif not prod_id:  # Include products without ID
                all_products.append(product_data)
        
        print(f"   → {len(products)} products")
    
    print(f"\n📊 Total unique products: {len(all_products)}")
    
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
