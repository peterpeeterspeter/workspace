#!/usr/bin/env python3
"""
Import Sawiday scraper data to Supabase - FIXED VERSION
"""

import json
import os
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# Category mapping (Dutch → English)
CATEGORY_MAP = {
    "Baden": "Bathtub",
    "Douche": "Shower",
    "Kranen": "Faucet",
    "Toiletten": "Toilet",
    "Wastafels": "Vanity",
    "Spiegels": "Lighting"
}

def clean_url(url):
    """Get base URL for deduplication."""
    if not url:
        return ''
    url = url.split('?')[0].split('#')[0].rstrip('/')
    return url

def flatten_products(data, default_category=''):
    """Extract list of products from various nested structures."""
    products = []

    def process_product(product, cat):
        """Process single product with category."""
        if isinstance(product, dict) and 'url' in product:
            product['category_nl'] = cat or default_category
            products.append(product)

    if isinstance(data, dict):
        for key, value in data.items():
            # List of products directly
            if isinstance(value, list):
                for item in value:
                    process_product(item, key)

            # Dict of brands (each with list of products)
            elif isinstance(value, dict):
                for brand, brand_products in value.items():
                    if isinstance(brand_products, list):
                        for product in brand_products:
                            process_product(product, key)

                    # Nested subcategory
                    elif isinstance(brand_products, dict):
                        for subcat, brands in brand_products.items():
                            for brand, prods in brands.items():
                                if isinstance(prods, list):
                                    for product in prods:
                                        process_product(product, key)

    return products

def calculate_price_tiers(products):
    """Calculate price tier cutoffs per category."""
    by_category = defaultdict(list)
    for p in products:
        if p.get('price', 0) > 0:
            by_category[p['category_en']].append(p['price'])

    tier_cutoffs = {}
    for category, prices in by_category.items():
        prices_sorted = sorted(prices)

        if len(prices_sorted) > 3:
            p25 = prices_sorted[int(len(prices_sorted) * 0.25)]
            p50 = prices_sorted[int(len(prices_sorted) * 0.50)]
            p75 = prices_sorted[int(len(prices_sorted) * 0.75)]
            p90 = prices_sorted[int(len(prices_sorted) * 0.90)]

            tier_cutoffs[category] = {
                'budget': p25,
                'economy': p50,
                'premium': p75,
                'luxury': p90
            }
        elif prices_sorted:
            p = prices_sorted[0]
            tier_cutoffs[category] = {
                'budget': p,
                'economy': p,
                'premium': p,
                'luxury': p
            }

    return tier_cutoffs

def get_primary_image(images):
    """Get first/best image as primary."""
    if not images:
        return None

    for img in images:
        if '2000x2000' in img:
            return img
    return images[0] if images else None

def process_json_files(directory):
    """Read all JSON files and process."""
    all_products = []
    seen_urls = set()
    file_count = 0

    for file_path in sorted(Path(directory).glob('*5perbrand*.json')):
        file_count += 1
        print(f"[{file_count}] Processing: {file_path.name}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Extract products
            products = flatten_products(data)

            # Process products
            for product in products:
                # Deduplicate by URL
                url = clean_url(product.get('url', ''))
                if not url or url in seen_urls:
                    continue

                seen_urls.add(url)

                # Map category
                category_nl = product.get('category_nl', '')
                category_en = CATEGORY_MAP.get(category_nl, category_nl)

                # Get primary image
                images = product.get('images', [])
                primary_image = get_primary_image(images)

                # Enrich product data
                enriched_product = {
                    'name': product.get('name', ''),
                    'brand': product.get('brand', ''),
                    'price': product.get('price', 0),
                    'category_en': category_en,
                    'category_nl': category_nl,
                    'subcategory': product.get('subcategory', ''),
                    'url': url,
                    'primary_image_url': primary_image,
                    'images': json.dumps(images),
                    'scraped_at': datetime.now().isoformat()
                }

                all_products.append(enriched_product)

        except Exception as e:
            print(f"  ⚠️  Error: {e}")

    print(f"\nTotal products: {len(all_products)}")
    print(f"Unique URLs: {len(seen_urls)}")
    return all_products

def generate_supabase_inserts(products, tier_cutoffs):
    """Generate Supabase INSERT statements."""
    inserts = []

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
        name_esc = p['name'].replace("'", "''").replace("\\", "\\\\")
        brand_esc = p['brand'].replace("'", "''").replace("\\", "\\\\")
        url_esc = p['url'].replace("'", "''").replace("\\", "\\\\")
        primary_image_esc = p['primary_image_url'].replace("'", "''").replace("\\", "\\\\") if p['primary_image_url'] else 'NULL'
        images_esc = p['images'].replace("'", "''")

        insert = f"""INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  '{name_esc}',
  '{brand_esc}',
  {price},
  '{category}',
  '{price_tier}',
  '{url_esc}',
  {f"'{primary_image_esc}'" if primary_image_esc else 'NULL'},
  '{images_esc}'::jsonb,
  NOW()
);"""

        inserts.append(insert)

    return inserts

def main():
    input_dir = '/root/.openclaw/workspace/research/bathroom-products'

    print("="*70)
    print("📦 SUPABASE IMPORT SCRIPT v3")
    print("="*70)
    print(f"Input directory: {input_dir}")
    print()

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

    for category, cutoffs in tier_cutoffs.items():
        print(f"\n{category}:")
        for tier, price in cutoffs.items():
            print(f"  {tier}: €{price:.2f}")

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
        for nl, en in CATEGORY_MAP.items():
            f.write(f"-- {nl} → {en}\n")
        f.write("\n")

        # Add price tier cutoffs as comment
        f.write("-- Price Tier Cutoffs (per category):\n")
        for category, cutoffs in tier_cutoffs.items():
            f.write(f"-- {category}:\n")
            for tier, price in cutoffs.items():
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
