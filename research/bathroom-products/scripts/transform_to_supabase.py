#!/usr/bin/env python3
"""
Transform Sawiday scraped data to Supabase-ready format
Splits data into: products, product_images, lifestyle_images
"""

import json
import sys
from pathlib import Path

def load_scraped_data():
    """Load all scraped Sawiday data"""
    raw_dir = Path("/root/.openclaw/workspace/research/bathroom-products/products/raw")
    
    products_data = []
    
    # Load all JSON files
    for json_file in raw_dir.glob("sawiday-*.json"):
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
                
                # Handle different formats
                if 'products' in data:
                    # New universal scraper format
                    products_data.extend(data.get('products', []))
                elif isinstance(data, list):
                    # Old scraper format (simple list)
                    products_data.extend(data)
        except Exception as e:
            print(f"Warning: Could not load {json_file.name}: {e}")
    
    print(f"✓ Loaded {len(products_data)} products from {len(list(raw_dir.glob('sawiday-*.json')))} files")
    return products_data

def transform_products(products):
    """Transform products to Supabase schema"""
    transformed = []
    
    for p in products:
        product = {}
        
        # Required fields
        product['name'] = p.get('name', '')
        product['price'] = p.get('price_eur', 0)
        product['url'] = p.get('url', '')
        product['brand'] = p.get('brand', 'Unknown')
        product['category'] = p.get('category', '')
        
        # Optional fields
        product['product_id'] = p.get('product_id', '')
        product['image_url'] = p.get('image_url', '')
        product['description'] = p.get('name', '')  # Full name as description
        
        transformed.append(product)
    
    return transformed

def create_product_images_table(products):
    """Create product_images table"""
    images = []
    
    for p in products:
        if p.get('image_url'):
            img = {
                'product_id': p.get('product_id', ''),
                'image_url': p.get('image_url', ''),
                'image_type': 'product',
                'alt_text': p.get('name', '')[:100]  # First 100 chars as alt text
            }
            images.append(img)
    
    return images

def create_lifestyle_images_table(products):
    """Create lifestyle_images table"""
    # For now, leave empty - will be populated separately
    return []

def create_supabase_schema():
    """Return Supabase table schemas"""
    return {
        'products': """-- SQL for products table
CREATE TABLE products (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    price DECIMAL NOT NULL,
    url TEXT,
    brand TEXT,
    category TEXT,
    product_id TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- SQL for product_images table
CREATE TABLE product_images (
    id TEXT PRIMARY KEY,
    product_id TEXT NOT NULL,
    image_url TEXT NOT NULL,
    image_type TEXT NOT NULL,  -- 'product' or 'lifestyle'
    alt_text TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- SQL for lifestyle_images table  
CREATE TABLE lifestyle_images (
    id TEXT PRIMARY KEY,
    product_id TEXT NOT NULL,
    image_url TEXT NOT NULL,
    alt_text TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
"""
    }

def main():
    print("=" * 60)
    print("🔄 SAWIDAY → SUPABASE TRANSFORMER")
    print("=" * 60)
    print()
    
    # Load all scraped data
    print("📂 Loading scraped data...")
    products = load_scraped_data()
    
    # Remove duplicates by product_id
    unique_products = {}
    for p in products:
        pid = p.get('product_id')
        if pid and pid not in unique_products:
            unique_products[pid] = p
    
    unique_products = list(unique_products.values())
    print(f"✓ Deduped to {len(unique_products)} unique products")
    
    # Transform to Supabase schema
    print("\n📦 Transforming to Supabase schema...")
    products_table = transform_products(unique_products)
    product_images = create_product_images_table(unique_products)
    lifestyle_images = create_lifestyle_images_table(unique_products)
    
    # Statistics
    total_images = len(product_images)
    with_images = len([p for p in unique_products if p.get('image_url')])
    
    print(f"\n📊 Statistics:")
    print(f"  Total products: {len(unique_products)}")
    print(f"  Products with images: {with_images} ({with_images/len(unique_products)*100:.1f}%)")
    print(f"  Product images to upload: {total_images}")
    print(f"  Lifestyle images: {len(lifestyle_images)} (to be added)")
    print()
    
    # Save tables
    output_dir = Path("/root/.openclaw/workspace/research/bathroom-products/data/supabase")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save products
    products_file = output_dir / "products.json"
    with open(products_file, 'w') as f:
        json.dump(products_table, f, ensure_ascii=False, indent=2)
    print(f"✓ Saved: {products_file}")
    
    # Save product_images
    images_file = output_dir / "product_images.json"
    with open(images_file, 'w') as f:
        json.dump(product_images, f, ensure_ascii=False, indent=2)
    print(f"✓ Saved: {images_file}")
    
    # Save lifestyle_images (empty for now)
    lifestyle_file = output_dir / "lifestyle_images.json"
    with open(lifestyle_file, 'w') as f:
        json.dump(lifestyle_images, f, ensure_ascii=False, indent=2)
    print(f"✓ Saved: {lifestyle_file}")
    
    # Save Supabase schema
    schema_file = output_dir / "supabase_schema.sql"
    with open(schema_file, 'w') as f:
        schema = create_supabase_schema()
        f.write(str(schema))  # Convert to string
    print(f"✓ Saved: {schema_file}")
    
    # Generate Supabase import script
    import_script = output_dir / "import_to_supabase.sh"
    with open(import_script, 'w') as f:
        f.write('#!/bin/bash\n')
        f.write('set -e\n\n')
        f.write('# Supabase connection details\n')
        f.write('# Get these from: https://app.supabase.com/project/_/settings/api\n')
        f.write('\n')
        f.write('# Load environment variables (optional)\n')
        f.write('# SUPABASE_URL="https://xyzproject.supabase.co"\n')
        f.write('SUPABASE_KEY="your-anon-key"\n')
        f.write('\n')
        f.write('# Import products\n')
        f.write(f'echo "Importing {len(products_table)} products..."\n')
        f.write(f'supabase db insert --db-url "$SUPABASE_URL" --db-key "$SUPABASE_KEY" \\\n')
        f.write('  --table=products \\\n')
        f.write('  --file=format=values \\\n')
        f.write(f'  --data={products_file}\n')
        f.write('\n')
        f.write('# Import product images\n')
        f.write(f'echo "Importing {total_images} product images..."\n')
        f.write(f'supabase db insert --db-url "$SUPABASE_URL" --db-key "$SUPABASE_KEY" \\\n')
        f.write('  --table=product_images \\\n')
        f.write('  --file=format=values \\\n')
        f.write(f'  --data={images_file}\n')
        f.write('\n')
        f.write('echo "✓ Import complete!"\n')
    
    print(f"✓ Saved: {import_script}")
    
    print()
    print("=" * 60)
    print("✅ TRANSFORMATION COMPLETE!")
    print()
    print("📁 Output Files:")
    print(f"   {products_file}")
    print(f"   {images_file}")
    print(f"   {lifestyle_file}")
    print(f"   {schema_file}")
    print(f"   {import_script}")
    print()
    print("🚀 Next Steps:")
    print("   1. Set SUPABASE_URL and SUPABASE_KEY in import script")
    print("   2. Run: bash import_to_supabase.sh")
    print("   3. Download product images from URLs")
    print("   4. Upload images to Supabase storage")
    print("   5. Add lifestyle images (use separate script)")
    print()
    print("💡 Tip: Use `supabase gen typescript` to generate TypeScript types from schema")

if __name__ == "__main__":
    main()
