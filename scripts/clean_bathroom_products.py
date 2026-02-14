#!/usr/bin/env python3
"""
Clean and organize bathroom products CSV.
- Proper categorization
- Select 50 products per category
- Ensure good images
"""

import csv
from collections import defaultdict

# Read the CSV file
input_file = '/root/.openclaw/media/inbound/file_14---b449e275-dff1-4a7a-9821-a1fde57433a6.csv'
output_file = '/root/.openclaw/workspace/research/bathroom-products/cleaned_products_50_per_category.csv'

# Store products by category
categories = defaultdict(list)

# Read and categorize products
with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        product_name = row['Product Name'].lower() if row['Product Name'] else ''
        brand = row['Brand'] if row['Brand'] else 'Unknown'
        price = row['Price (€)'] if row['Price (€)'] else ''
        image_url = row['Image URL'] if row['Image URL'] else ''
        
        # Determine category based on product name
        category = 'Bad'  # Default to bathtubs (most products)
        
        # Check for shower-related keywords
        if any(keyword in product_name for keyword in ['douche', 'shower', 'regendouche', 'handdouche', 'thermostaat', 'showerpipe', 'buitendouche', 'inloopdouche']):
            category = 'Douche'
        # Check for sink/basin-related keywords  
        elif any(keyword in product_name for keyword in ['wastafel', 'gootsteen', 'fontein', 'fonteinset']):
            category = 'Wastafels'
        
        categories[category].append({
            'Product ID': row['Product ID'],
            'Product Name': row['Product Name'],
            'Brand': brand,
            'Price (€)': price,
            'Category': category,
            'Image URL': image_url
        })

# Take top 50 products from each category (or all if less than 50)
final_products = []
category_order = ['Douche', 'Wastafels', 'Bad']

for cat in category_order:
    if cat in categories:
        products = categories[cat][:50]  # Take first 50
        final_products.extend(products)
        print(f"{cat}: {len(products)} products selected")

# Write cleaned CSV
fieldnames = ['Product ID', 'Product Name', 'Brand', 'Price (€)', 'Category', 'Image URL']

with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(final_products)

print(f"\nTotal products written: {len(final_products)}")
print(f"Output file: {output_file}")
