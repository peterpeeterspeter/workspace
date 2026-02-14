#!/usr/bin/env python3
"""
Sample products from Supabase database by category
Creates representative samples for Vision AI validation
"""

import json
import random
from collections import defaultdict

def categorize_product_name(product_name, product_description):
    """Categorize product based on name and description"""
    name = product_name.lower()
    description = product_description.lower()
    combined = f"{name} {description}"
    
    # Priority-ordered categorization
    if any(word in combined for word in ['douche', 'shower', 'inloopdouche']):
        if 'douche wc' not in combined and 'douche' in combined:
            return 'Shower'
        elif 'douche wc' in combined or 'wc douche' in combined:
            return 'Toilet'
        else:
            return 'Shower'
    
    if any(word in combined for word in ['spiegel']):
        if 'led' in combined:
            return 'Lighting'
        else:
            if 'toilet' not in combined and 'closet' not in combined:
                return 'Vanity'
            else:
                return 'Toilet'
    
    if any(word in combined for word in ['wastafel', 'wasbak', 'meubel']):
        return 'Vanity'
    
    if any(word in combined for word in ['kraan', 'mengkraan', 'wastafelkraan']):
        if 'toilet' not in combined and 'closet' not in combined:
            return 'Faucet'
        else:
            return 'Toilet'
    
    if 'bad' in name or 'bathtub' in name or 'whirlpool' in name:
        if 'toilet' not in combined and 'closet' not in combined:
            return 'Bathtub'
        else:
            return 'Toilet'
    
    if any(word in combined for word in ['toilet', 'closet', 'urinoir', 'bidet']):
        return 'Toilet'
    
    if any(word in combined for word in ['tegel', 'mozaiek', 'tile']):
        return 'Tile'
    
    return 'Other'

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Gebruik: python3 sample_products.py <input_json> [output_file]")
        print("\nVoorbeeld:")
        print("  python3 sample_products.py data/supabase/products.json sampled_products.json")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace('.json', '_sampled.json')
    
    print("=" * 60)
    print("🎯 Bathroom Product Sampler")
    print("=" * 60)
    print(f"Input: {input_file}")
    print(f"Output: {output_file}")
    print()
    
    # Load products
    with open(input_file, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    print(f"📊 Loaded {len(products):,} products")
    print()
    
    # Categorize all products
    categorized = defaultdict(list)
    for product in products:
        category = categorize_product_name(
            product.get('name', ''),
            product.get('description', '')
        )
        categorized[category].append(product)
    
    print("📊 Category Distribution:")
    for cat in ['Bathtub', 'Shower', 'Vanity', 'Toilet', 'Faucet', 'Lighting', 'Tile', 'Other']:
        count = len(categorized.get(cat, []))
        print(f"  {cat:15s}: {count:6,}")
    
    print()
    
    # Sample from each category
    sample_targets = {
        'Toilet': 50,
        'Bathtub': 50,
        'Shower': 10,
        'Lighting': 5,
        'Faucet': 3,
        'Vanity': 2,
        'Tile': 1
    }
    
    sampled = []
    
    for category, target_count in sample_targets.items():
        available = categorized.get(category, [])
        
        if len(available) == 0:
            print(f"⚠️  Warning: No products available for '{category}'")
            continue
        
        # If not enough products, sample all available
        sample_size = min(target_count, len(available))
        
        # Random sample
        sampled_products = random.sample(available, sample_size)
        
        for product in sampled_products:
            product['sample_category'] = category
            product['sample_reason'] = f"Random sample from {category} ({sample_size}/{len(available)} available)"
        
        sampled.extend(sampled_products)
        
        print(f"✅ {category}: Sampled {sample_size}/{len(available)} products (target: {target_count})")
    
    print()
    print("=" * 60)
    print(f"✅ Total Sampled: {len(sampled)} products")
    print("=" * 60)
    
    # Show sample breakdown
    print()
    print("📋 Sample Breakdown:")
    for category, target_count in sample_targets.items():
        count = sum(1 for p in sampled if p.get('sample_category') == category)
        print(f"  {category:15s}: {count:3d} sampled (target: {target_count})")
    
    print()
    print(f"💾 Output: {output_file}")
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(sampled, f, ensure_ascii=False, indent=2)
    
    print("✅ Saved sampled products to file")
    print()
    print("📝 Next Steps:")
    print("1. Review sampled products for quality")
    print("2. Use for Vision AI validation")
    print("3. Update training rules if needed")

if __name__ == '__main__':
    main()
