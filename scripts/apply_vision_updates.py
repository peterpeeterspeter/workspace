#!/usr/bin/env python3
"""
Final categorization updates after vision analysis.
"""

import csv
from pathlib import Path

# Vision analysis results for uncertain products
VISION_CATEGORIES = {
    "Sanibroyeur Saniwall Pro UP - Grohe inbouwreservoir - tegelbaar - Sanibroyeur vermaler - bedieningspaneel glans chroom": "Toilet",
    "Villeroy & Boch Omnia Architectura DirectFlush combipack - ceramic+ wit": "Toilet",
    "Nemo Spring Cascata jachtbak 38x14.5x40cm met Geberit spoelmechanisme porselein wit TWEEDEKANS": "Toilet",
    "Wisa afdekplaat 34.5x16.5cm kunststof wit": "Toilet"
}

def main():
    input_file = Path("/root/.openclaw/workspace/output/categorized_products_batch1.csv")
    output_file = Path("/root/.openclaw/workspace/output/categorized_products_final.csv")
    
    # Read CSV
    products = []
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            products.append(row)
    
    print(f"Updating {len(products)} products with vision analysis results...")
    
    # Update categories based on vision analysis
    updated = 0
    for product in products:
        name = product.get('name_raw', '')
        
        # Check if this product needs vision-based update
        for key, category in VISION_CATEGORIES.items():
            if key in name:
                old_cat = product.get('category', '')
                if old_cat != category:
                    product['category'] = category
                    updated += 1
                    print(f"Updated: {name[:60]}... -> {category}")
    
    # Write final CSV
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        fieldnames = list(products[0].keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)
    
    print(f"\nComplete! Updated {updated} products with vision analysis.")
    print(f"Final output: {output_file}")

if __name__ == "__main__":
    main()
