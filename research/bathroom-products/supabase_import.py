#!/usr/bin/env python3
"""
Supabase Import Script for Sawiday Bathroom Products
Features:
- Reads all JSON files from scraper
- Deduplicates by URL
- Maps categories (Baden → Bathtub, Douche → Shower, etc.)
- Generates Supabase INSERT statements with JSONB images
- Uses first image as primary_image_url
- Auto-calculates price tiers per category
"""

import json
import os
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# Category mapping (Dutch → English)
CATEGORY_MAP = {
    "Baden": "Bathtub",
    "baden": "Bathtub",
    "Douche": "Shower",
    "douche": "Shower",
    "Kranen": "Faucet",
    "kranen": "Faucet",
    "Toiletten": "Toilet",
    "toiletten": "Toilet",
    "Wastafels": "Vanity",
    "wastafels": "Vanity",
    "Spiegels": "Lighting",
    "spiegels": "Lighting"
}

def map_category(category_nl):
    """Map Dutch category to English."""
    category_nl = category_nl.lower()
    
    # Direct mappings
    if category_nl in CATEGORY_MAP:
        return CATEGORY_MAP[category_nl]
    
    # Handle common variations
    if "baden" in category_nl:
        return "Bathtub"
    if "douche" in category_nl:
        return "Shower"
    if "kranen" in category_nl or "kraan" in category_nl:
        return "Faucet"
    if "toiletten" in category_nl or "toilet" in category_nl:
        return "Toilet"
    if "wastafels" in category_nl or "wastafel" in category_nl:
        return "Vanity"
    if "spiegels" in category_nl or "spiegel" in category_nl:
        return "Lighting"
    
    # Default: return as-is if no mapping found
    print(f"  ⚠️  Unknown category: {category_nl} → using as-is")
    return category_nl.title()

def clean_url(url):
    """Get base URL for deduplication."""
    if not url:
        return ''
    url = url.split('?')[0].split('#')[0]
    url = url.rstrip('/')
    return url

def get_primary_image(images):
    """Get best image as primary."""
    if not images:
        return None
    
    # Prefer high-res images (2000x2000)
    for img in images:
        if '2000x2000' in img or '1920' in img:
            return img
    
    # Fallback: first image
    return images[0]

def process_json_files(directory):
    """Read all JSON files and process."""
    all_products = []
    seen_urls = set()
    file_count = 0
    
    print("="*70)
    print("📦 PROCESSING SCRAPER OUTPUT FILES")
    print("="*70)
    
    # Find all JSON files
    for file_path in sorted(Path(directory).glob('*5perbrand*.json')):
        file_count += 1
        print(f"\n[{file_count}] Processing: {file_path.name}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Process each product
            for product in flatten_products(data):
                # Deduplicate by URL
                clean_url = clean_url(product.get('url', ''))
                if not clean_url or clean_url in seen_urls:
                    continue
                
                seen_urls.add(clean_url)
                
                # Map category
                category_nl = product.get('category_nl', product.get('category', ''))
                category_en = map_category(category_nl)
                
                # Get primary image
                images = product.get('images', [])
                primary_image = get_primary_image(images)
                
                # Enrich product data
                enriched_product = {
                    'name': product.get('name', ''),
                    'brand': product.get('brand', ''),
                    'price': product.get('price', 0),
                    'category_nl': category_nl,
                    'category_en': category_en,
                    'subcategory': product.get('subcategory', ''),
                    'url': clean_url,
                    'primary_image_url': primary_image,
                    'images': json.dumps(images),  # Store all as JSONB
                    'scraped_at': datetime.now().isoformat()
                }
                
                all_products.append(enriched_product)
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print(f"\n✅ Processed {file_count} files")
    print(f"📊 Total products: {len(all_products)}")
    print(f"🔒 Unique URLs: {len(seen_urls)}")
    return all_products

def flatten_products(data, parent_category=''):
    """Extract list of products from various nested structures."""
    products = []
    
    if isinstance(data, dict):
        for key, value in data.items():
            # Value is list of products
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, dict) and 'url' in item:
                        item['category_nl'] = parent_category or key
                        products.append(item)
            
            # Value is dict of brands
            elif isinstance(value, dict):
                for brand, brand_products in value.items():
                    if isinstance(brand_products, list):
                        for product in brand_products:
                            if isinstance(product, dict) and 'url' in product:
                                product['category_nl'] = parent_category or key
                                products.append(product)
    
    return products

def calculate_price_tiers(products):
    """Calculate price tier cutoffs per category."""
    by_category = defaultdict(list)
    for p in products:
        if p.get('price', 0) > 0:
            by_category[p['category_en']].append(p['price'])
    
    tier_cutoffs = {}
    
    for category, prices in by_category.items():
        if not prices:
            print(f"\n{category}: No prices found")
            continue
            
        prices_sorted = sorted(prices)
        n = len(prices_sorted)
        
        # Define percentile cutoffs
        p25 = prices_sorted[int(n * 0.25)] if n > 3 else prices_sorted[0]
        p50 = prices_sorted[int(n * 0.50)] if n > 1 else prices_sorted[0]
        p75 = prices_sorted[int(n * 0.75)] if n > 1 else prices_sorted[0]
        p90 = prices_sorted[int(n * 0.90)] if n > 1 else prices_sorted[0]
        
        tier_cutoffs[category] = {
            'budget': p25,
            'economy': p50,
            'premium': p75,
            'luxury': p90
        }
        
        print(f"\n{category} price tiers:")
        for tier, price in tier_cutoffs[category].items():
            print(f"  {tier}: €{price:.2f}")
    
    return tier_cutoffs

def generate_supabase_inserts(products, tier_cutoffs):
    """Generate Supabase INSERT statements."""
    inserts = []
    
    print("\n" + "="*70)
    print("📝 GENERATING SUPABASE INSERTS")
    print("="*70)
    
    for p in products:
        # Calculate price tier
        category = p['category_en']
        price = p['price']
        price_tier = 'budget'
        
        if category in tier_cutoffs:
            for tier, cutoff in tier_cutoffs[category].items():
                if price <= cutoff:
                    price_tier = tier
                    break
        
        # Properly escape strings for SQL
        name_escaped = p['name'].replace("'", "''").replace("\\", "\\\\")
        brand_escaped = p['brand'].replace("'", "''").replace("\\", "\\\\")
        url_escaped = p['url'].replace("'", "''").replace("\\", "\\\\")
        images_escaped = p['images'].replace("'", "''").replace("\\", "\\\\")
        
        # Handle primary image with proper escaping
        if p['primary_image_url']:
            primary_image_sql = f"'{p['primary_image_url'].replace(\"'\", \"''\")}'"
        else:
            primary_image_sql = 'NULL'
        
        category_en = p['category_en']
        subcategory = p.get('subcategory', '')
        
        insert = f"""INSERT INTO products (
  name, brand, price, category, subcategory, price_tier, url, primary_image_url, images, created_at
) VALUES (
  '{name_escaped}',
  '{brand_escaped}',
  {price},
  '{category_en}',
  '{subcategory}',
  '{price_tier}',
  '{url_escaped}',
  {primary_image_sql},
  '{images_escaped}'::jsonb,
  NOW()
);"""
        
        inserts.append(insert)
    
    return inserts

def main():
    input_dir = '/root/.openclaw/workspace/research/bathroom-products'
    
    print("="*70)
    print("📋 SUPABASE IMPORT SCRIPT")
    print("="*70)
    print(f"Input directory: {input_dir}\n")
    
    # Process all JSON files
    products = process_json_files(input_dir)
    
    if not products:
        print("\n❌ No products found!")
        return
    
    # Calculate price tiers per category
    print("\n" + "="*70)
    print("💰 CALCULATING PRICE TIERS")
    print("="*70)
    tier_cutoffs = calculate_price_tiers(products)
    
    # Generate INSERT statements
    print("\n" + "="*70)
    print("📝 GENERATING SUPABASE INSERTS")
    print("="*70)
    
    inserts = generate_supabase_inserts(products, tier_cutoffs)
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{input_dir}/supabase_import_{timestamp}.sql"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("-- Supabase Import for Sawiday Products\n")
        f.write(f"-- Generated: {datetime.now().isoformat()}\n")
        f.write(f"-- Total products: {len(products)}\n")
        f.write(f"-- Source: Sawiday scraper\n\n")
        
        # Add category mappings as comment
        f.write("-- Category Mappings (Dutch → English):\n")
        for nl, en in sorted(CATEGORY_MAP.items()):
            f.write(f"-- {nl} → {en}\n")
        f.write("\n")
        
        # Add price tier cutoffs as comment
        f.write("-- Price Tier Cutoffs (per category):\n")
        for category, cutoffs in sorted(tier_cutoffs.items()):
            f.write(f"\n-- {category}:\n")
            for tier, price in sorted(cutoffs.items(), key=lambda x: x[1]):
                f.write(f"--   {tier}: €{price:.2f}\n")
        f.write("\n")
        
        # Write INSERT statements
        f.write("BEGIN;\n\n")
        for insert in inserts:
            f.write(insert + "\n")
        f.write("\nCOMMIT;\n")
    
    print(f"\n✅ SQL file created: {output_file}")
    print(f"   Size: {os.path.getsize(output_file)} bytes")
    print(f"   Statements: {len(inserts)}")
    
    # Summary
    print("\n" + "="*70)
    print("📊 SUMMARY")
    print("="*70)
    
    by_category = defaultdict(int)
    for p in products:
        by_category[p['category_en']] += 1
    
    print("\nProducts by category:")
    for cat, count in sorted(by_category.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat}: {count}")
    
    print(f"\nTotal: {sum(by_category.values())} products")
    print(f"File: {output_file}")

if __name__ == '__main__':
    main()
