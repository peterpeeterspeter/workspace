#!/usr/bin/env python3
"""
Categorize bathroom products using keyword matching from Dutch product names.
"""

import csv
import sys
from pathlib import Path

# Target categories
VALID_CATEGORIES = ["Bathtub", "Shower", "Vanity", "Toilet", "Faucet"]

# Dutch keywords for each category
CATEGORY_KEYWORDS = {
    "Bathtub": [
        "bad", "ligbad", "hoekbad", "vrijstaand bad", "halfvrijstaand bad", 
        "whirlpoolbad", "zitbad", "inbouw bad", "freestanding", "badkuip"
    ],
    "Toilet": [
        "toilet", "closet", "urinoir", "wandcloset", "wc", "douche wc", 
        "douchewc", "spoelrand", "spoelrandloos", "rimless", "zitting"
    ],
    "Vanity": [
        "spiegel", "wasbak", "wastafel", "badmeubel", "wasunit", 
        "badkamermeubel", "led spiegel", "spiegelverwarming"
    ],
    "Faucet": [
        "kraan", "mengkraan", "thermostaatkraan", "bidet", "wastafelkraan"
    ],
    "Shower": [
        "douche", "shower", "regendouche", "handdoek", "douchecabine",
        "douchegoot", "doucheset"
    ]
}

def categorize_by_name(product_name):
    """Categorize product based on Dutch product name keywords."""
    if not product_name:
        return None
    
    product_lower = product_name.lower()
    
    # Priority: check specific terms first
    # Toilets have priority over other categories (e.g., "douche wc" is Toilet)
    for keyword in CATEGORY_KEYWORDS["Toilet"]:
        if keyword in product_lower:
            return "Toilet"
    
    for category, keywords in CATEGORY_KEYWORDS.items():
        if category == "Toilet":
            continue  # Already checked
        for keyword in keywords:
            if keyword in product_lower:
                return category
    
    return None

def main():
    input_file = Path("/root/.openclaw/media/inbound/file_19---0e0d6ca0-74ac-4ebf-ba3d-75ec786aaf1d.csv")
    output_file = Path("/root/.openclaw/workspace/output/categorized_products_batch1.csv")
    needs_vision_file = Path("/root/.openclaw/workspace/output/needs_vision_analysis.txt")
    
    if not input_file.exists():
        print(f"Error: {input_file} not found")
        sys.exit(1)
    
    # Read input CSV
    products = []
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        
        for row in reader:
            products.append(row)
    
    print(f"Processing {len(products)} products...")
    
    # Process products
    stats = {
        'total': len(products),
        'categorized': 0,
        'unchanged': 0,
        'uncertain': 0
    }
    
    updated = []
    needs_vision = []
    
    for product in products:
        name = product.get('name_raw', '')
        old_category = product.get('category', '')
        
        # Try keyword-based categorization
        new_category = categorize_by_name(name)
        
        # Track old category
        product['old_category'] = old_category
        
        # Update category if we found a better one
        if new_category:
            if new_category != old_category:
                product['category'] = new_category
                stats['categorized'] += 1
            else:
                stats['unchanged'] += 1
        else:
            stats['uncertain'] += 1
            needs_vision.append({
                'name': name,
                'old_category': old_category,
                'image_url': product.get('image_url', '')
            })
        
        updated.append(product)
    
    # Write output CSV
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        fieldnames = list(updated[0].keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated)
    
    # Write list of products needing vision analysis
    with open(needs_vision_file, 'w', encoding='utf-8') as f:
        f.write(f"# Products needing vision analysis ({len(needs_vision)})\n\n")
        for item in needs_vision:
            f.write(f"Name: {item['name']}\n")
            f.write(f"Old Category: {item['old_category']}\n")
            f.write(f"Image: {item['image_url']}\n\n")
    
    print(f"\n=== Processing Complete ===")
    print(f"Total products: {stats['total']}")
    print(f"Categorized (changed): {stats['categorized']}")
    print(f"Already correct: {stats['unchanged']}")
    print(f"Needs vision analysis: {stats['uncertain']}")
    print(f"\nOutput CSV: {output_file}")
    print(f"Vision analysis list: {needs_vision_file}")

if __name__ == "__main__":
    main()
