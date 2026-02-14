#!/usr/bin/env python3
"""
Generate product catalog CSV from scraped images
"""

import os
import json
import csv
from collections import defaultdict

BASE_DIR = "/root/.openclaw/workspace/research/bathroom-products/raw-images"

# Price ranges by tier for NL/BE market
PRICE_RANGES = {
    'budget': {'low': 50, 'high': 150},
    'mid': {'low': 150, 'high': 500},
    'premium': {'low': 500, 'high': 5500}
}

# Category mapping from filenames
CATEGORY_MAP = {
    'faucet': 'faucets',
    'toilet': 'toilets',
    'shower': 'showers',
    'vanity': 'vanity',
    'sink': 'sinks',
    'tile': 'tile',
    'light': 'lighting',
    'bathtub': 'bathtub',
    'bath': 'bathtub'
}

# Tier detection from path
def detect_tier(path):
    if '/budget/' in path:
        return 'budget'
    elif '/mid-range/' in path:
        return 'mid'
    elif '/premium/' in path:
        return 'premium'
    return 'premium'

# Category from path
def detect_category(path):
    for keyword, cat in CATEGORY_MAP.items():
        if keyword in path.lower():
            return cat
    return 'other'

# Brand detection from filename
def detect_brand(filename):
    fname = filename.lower()
    if 'duravit' in fname:
        return 'Duravit'
    elif 'ideal' in fname or 'cera' in fname or 'ceraplan' in fname or 'ceratherm' in fname:
        return 'Ideal Standard'
    elif 'naber' in fname or 'lumica' in fname:
        return 'Naber'
    elif 'grohe' in fname or 'hansgrohe' in fname:
        return 'Grohe'
    elif 'essential-line' in fname:
        return 'Essential Line'
    else:
        return 'Generic'

# Generate product name from filename
def generate_product_name(filename):
    """Generate clean product name from filename"""
    fname = filename.replace('.jpg', '').replace('.webp', '')
    
    # Remove tier prefixes
    for prefix in ['duravit-', 'ideal-standard-', 'essential-line-', 'naber-']:
        fname = fname.replace(prefix, '', 1)
    
    # Clean up
    fname = fname.replace('_', ' ').replace('-', ' ').strip()
    
    # Remove technical suffixes
    for suffix in ['packshot', 'lifestyle', 'chrome', 'matt', 'white', 'black', 'high', 'low', 'pressure']:
        fname = fname.replace(suffix, '').strip()
    
    return fname.title() if fname else 'Unnamed Product'

products = []
product_id = 1

# Walk through all images (both JPG and WebP)
for root, dirs, files in os.walk(BASE_DIR):
    for file in files:
        if not (file.lower().endswith('.jpg') or file.lower().endswith('.webp')):
            continue
        
        file_path = os.path.join(root, file)
        
        # Skip - already processed if we have WebP
        if file.lower().endswith('.jpg'):
            webp_path = file_path.replace('.jpg', '.webp')
            if os.path.exists(webp_path):
                continue
        
        category = detect_category(file_path)
        tier = detect_tier(file_path)
        brand = detect_brand(file)
        name = generate_product_name(file)
        
        # Get prices
        prices = PRICE_RANGES[tier]
        price_low = prices['low']
        price_high = prices['high']
        
        # Generate storage path
        rel_path = file_path.replace(BASE_DIR + '/', '')
        storage_path = f"product-images/{rel_path}"
        
        # Render path (use WebP if exists)
        render_path = storage_path.replace('.jpg', '.webp')
        if not os.path.exists(file_path.replace('.jpg', '.webp')):
            render_path = storage_path
        
        product = {
            'id': product_id,
            'brand': brand,
            'name': name,
            'category': category,
            'price_tier': tier,
            'price_low': price_low,
            'price_high': price_high,
            'currency': 'EUR',
            'image_url': f'https://cdn.yoursite.com/bathroom/{category}/{os.path.basename(file)}',
            'catalog_image_path': storage_path,
            'render_image_path': render_path,
            'origin': 'scraped',
            'is_active': True,
            'display_order': product_id,
            'description': f"{brand} {name} - High-quality {category} for modern bathrooms. Part of the {tier} collection."
        }
        
        products.append(product)
        product_id += 1

print(f"Generated {len(products)} products from image files")

# Write CSV
output_file = '/root/.openclaw/workspace/research/bathroom-products/product-catalog.csv'
fieldnames = ['id', 'brand', 'name', 'category', 'price_tier', 'price_low', 'price_high', 
              'currency', 'image_url', 'catalog_image_path', 'render_image_path', 'origin', 'is_active', 'display_order', 'description']

with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(products)

print(f"✅ Product catalog written to: {output_file}")
print(f"   Total products: {len(products)}")
print(f"   Categories: {set(p['category'] for p in products)}")
print(f"   Tiers: {set(p['price_tier'] for p in products)}")
print(f"   Brands: {set(p['brand'] for p in products)}")
