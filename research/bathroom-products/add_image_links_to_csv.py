#!/usr/bin/env python3
"""
Add image links from product.json files to the CSV.
Matches products by name and adds local image paths.
"""

import csv
import json
import os
from pathlib import Path
from urllib.parse import urlparse
import re

def normalize_name(name):
    """Normalize product name for matching."""
    if not name:
        return ""
    # Remove extra whitespace, convert to lowercase
    name = name.strip().lower()
    # Remove common variations
    name = re.sub(r'\s+', ' ', name)
    return name

def extract_image_filename(url):
    """Extract filename from image URL."""
    parsed = urlparse(url)
    path = parsed.path
    # Get the filename part after last slash
    filename = path.split('/')[-1]
    return filename

def load_product_images(bathroom_products_dir):
    """Scan all product.json files and build name -> images mapping."""
    products = {}

    # Scan both single-products and batch-browser-scrape
    for base_dir in ['single-products', 'batch-browser-scrape']:
        base_path = Path(bathroom_products_dir) / base_dir
        if not base_path.exists():
            continue

        # Find all product.json files
        for product_json in base_path.rglob('product.json'):
            try:
                with open(product_json, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                name = data.get('name', '').strip()
                if not name:
                    continue

                # Get images
                images = data.get('images', [])
                if not images:
                    continue

                # Store both URLs and would-be local paths
                image_data = []
                for img in images:
                    img_url = img.get('url', '')
                    if img_url:
                        filename = extract_image_filename(img_url)
                        # Would-be local path (assuming organized by product name)
                        safe_name = re.sub(r'[^\w\s-]', '', name).strip().replace(' ', '-').lower()
                        local_path = f"images/{safe_name}/{filename}"

                        image_data.append({
                            'url': img_url,
                            'local_path': local_path,
                            'alt': img.get('alt', '')
                        })

                if image_data:
                    norm_name = normalize_name(name)
                    # Handle duplicates - keep the one with most images
                    if norm_name not in products or len(products[norm_name]) < len(image_data):
                        products[norm_name] = {
                            'name': name,
                            'images': image_data
                        }

            except Exception as e:
                print(f"Error loading {product_json}: {e}")
                continue

    return products

def match_csv_to_images(csv_path, products):
    """Match CSV products to their images."""
    updated_rows = []

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames

        # Add new columns
        if 'local_images' not in fieldnames:
            fieldnames.append('local_images')
        if 'image_count' not in fieldnames:
            fieldnames.append('image_count')
        if 'all_image_urls' not in fieldnames:
            fieldnames.append('all_image_urls')

        matched = 0
        unmatched = 0

        for row in reader:
            name = row.get('name', '').strip()
            norm_name = normalize_name(name)

            # Try to match
            if norm_name in products:
                product = products[norm_name]
                images = product['images']

                # Add image data
                row['local_images'] = ';'.join([img['local_path'] for img in images])
                row['all_image_urls'] = ';'.join([img['url'] for img in images])
                row['image_count'] = len(images)
                matched += 1
            else:
                # Try fuzzy match
                matched_product = None
                for prod_name, prod_data in products.items():
                    # Check if key words match
                    csv_words = set(norm_name.split())
                    prod_words = set(prod_name.split())
                    overlap = csv_words & prod_words

                    if len(overlap) >= 3:  # At least 3 matching words
                        matched_product = prod_data
                        break

                if matched_product:
                    images = matched_product['images']
                    row['local_images'] = ';'.join([img['local_path'] for img in images])
                    row['all_image_urls'] = ';'.join([img['url'] for img in images])
                    row['image_count'] = len(images)
                    matched += 1
                else:
                    row['local_images'] = ''
                    row['all_image_urls'] = row.get('image_url', '')
                    row['image_count'] = 1 if row.get('image_url') else 0
                    unmatched += 1

            updated_rows.append(row)

    return updated_rows, matched, unmatched

def main():
    bathroom_products_dir = '/root/.openclaw/workspace/research/bathroom-products'
    csv_path = os.path.join(bathroom_products_dir, 'optimized_products_with_subcategories.csv')
    output_path = os.path.join(bathroom_products_dir, 'products_with_image_links.csv')

    print("Loading product images from product.json files...")
    products = load_product_images(bathroom_products_dir)
    print(f"Found {len(products)} products with images")

    print("Matching CSV products to images...")
    updated_rows, matched, unmatched = match_csv_to_images(csv_path, products)

    print(f"Matched: {matched}")
    print(f"Unmatched: {unmatched}")

    # Write updated CSV
    print(f"Writing to {output_path}...")
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        if updated_rows:
            writer = csv.DictWriter(f, fieldnames=updated_rows[0].keys())
            writer.writeheader()
            writer.writerows(updated_rows)

    print("Done!")
    print(f"Output: {output_path}")

    # Show some examples
    print("\n=== Sample products with images ===")
    with open(output_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i >= 5:
                break
            if int(row.get('image_count', 0)) > 1:
                print(f"\n{row['name']}")
                print(f"  Images: {row['image_count']}")
                print(f"  Local: {row['local_images'][:100]}...")

if __name__ == '__main__':
    main()
