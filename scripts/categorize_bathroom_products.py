#!/usr/bin/env python3
"""
Categorize bathroom products using vision analysis and keyword matching.
"""

import csv
import re
import subprocess
import json

# Target categories
VALID_CATEGORIES = ["Bathtub", "Showers", "Vanity", "Toilet", "Faucet"]

# Keyword-based categorization (Dutch product names)
CATEGORY_KEYWORDS = {
    "Bathtub": ["bad", "ligbad", "hoekbad", "vrijstaand bad", "whirlpoolbad", "zitbad", "inbouw bad"],
    "Toilet": ["toilet", "closet", "urinoir", "wandcloset", "wc", "douche wc", "douchewc"],
    "Vanity": ["spiegel", "wasbak", "wastafel", "badmeubel", "wasunit"],
    "Faucet": ["kraan", "mengkraan", "thermostaatkraan"],
    "Showers": ["douche", "shower", "regendouche", "handdoek", "douchecabine"]
}

def categorize_by_name(product_name):
    """Categorize product based on Dutch product name keywords."""
    product_lower = product_name.lower()
    
    # Check for each category's keywords
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in product_lower:
                return category
    
    return None

def categorize_by_vision(image_url):
    """Use vision API to categorize product from image."""
    try:
        result = subprocess.run(
            ["openclaw", "image", "analyze",
             "--image", image_url,
             "--prompt", "What is this product? Is it a Bathtub, Shower, Vanity, Toilet, or Faucet? Answer with just the category name."],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            response = result.stdout.strip()
            # Extract category from response
            for category in VALID_CATEGORIES:
                if category.lower() in response.lower():
                    return category
    except Exception as e:
        print(f"Vision analysis failed for {image_url}: {e}")
    
    return None

def main():
    input_file = "/root/.openclaw/media/inbound/file_19---0e0d6ca0-74ac-4ebf-ba3d-75ec786aaf1d.csv"
    output_file = "/root/.openclaw/workspace/output/categorized_products.csv"
    
    # Read input CSV
    products = []
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=',')
        header = reader.fieldnames
        
        for row in reader:
            products.append(row)
    
    print(f"Processing {len(products)} products...")
    
    # Process products
    categorized = 0
    vision_analyzed = 0
    updated = []
    
    for i, product in enumerate(products):
        name = product.get('name_raw', '')
        old_category = product.get('category', '')
        image_url = product.get('image_url', '')
        
        # Try keyword-based categorization first
        new_category = categorize_by_name(name)
        
        # If keywords don't work, use vision (but limit to avoid rate issues)
        if not new_category and image_url and vision_analyzed < 50:
            print(f"Vision analyzing product {i+1}/{len(products)}: {name[:50]}...")
            new_category = categorize_by_vision(image_url)
            vision_analyzed += 1
        
        # Update category if we found a better one
        if new_category and new_category != old_category:
            product['old_category'] = old_category
            product['category'] = new_category
            categorized += 1
            print(f"  {old_category} -> {new_category}: {name[:60]}...")
        
        updated.append(product)
    
    # Write output CSV
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        # Add old_category to header if it exists
        fieldnames = list(updated[0].keys()) if updated else header
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated)
    
    print(f"\nDone! Categorized {categorized} products.")
    print(f"Used vision analysis for {vision_analyzed} products.")
    print(f"Output: {output_file}")

if __name__ == "__main__":
    main()
