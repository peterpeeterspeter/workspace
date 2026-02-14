#!/usr/bin/env python3
"""
Generate additional data files for import
- Image manifest for Supabase Storage upload
- Category/tier distribution summary
- Style tag assignments
"""

import csv
from collections import defaultdict

# Read product catalog
products = []
with open('/root/.openclaw/workspace/research/bathroom-products/product-catalog.csv', 'r') as f:
    reader = csv.DictReader(f)
    products = list(reader)

# 1. Image Manifest (for Supabase Storage upload)
manifest = []
for p in products:
    manifest.append({
        'local_path': f"/root/.openclaw/workspace/research/bathroom-products/raw-images/{p['catalog_image_path'].replace('product-images/', '')}",
        'storage_path': p['catalog_image_path'],
        'product_id': p['id'],
        'type': 'catalog'
    })

# Write image manifest
with open('/root/.openclaw/workspace/research/bathroom-products/image-manifest.csv', 'w', newline='') as f:
    fieldnames = ['local_path', 'storage_path', 'product_id', 'type']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(manifest)

print(f"✅ Image manifest: {len(manifest)} entries")

# 2. Category/Tier Distribution
category_tier = defaultdict(lambda: defaultdict(int))
for p in products:
    category_tier[p['category']][p['price_tier']] += 1

print("\n📊 Category/Tier Distribution:")
for cat in sorted(category_tier.keys()):
    print(f"\n{cat.upper()}:")
    for tier in ['budget', 'mid', 'premium']:
        count = category_tier[cat][tier]
        print(f"  {tier:8s}: {count:3d} products")

# 3. Summary stats
tier_counts = defaultdict(int)
brand_counts = defaultdict(int)
for p in products:
    tier_counts[p['price_tier']] += 1
    brand_counts[p['brand']] += 1

print(f"\n📈 Overall Distribution:")
for tier in ['budget', 'mid', 'premium']:
    pct = (tier_counts[tier] / len(products)) * 100
    print(f"  {tier:8s}: {tier_counts[tier]:3d} ({pct:.1f}%)")

print(f"\n🏷️  Brand Distribution:")
for brand, count in sorted(brand_counts.items(), key=lambda x: x[1], reverse=True):
    pct = (count / len(products)) * 100
    print(f"  {brand:15s}: {count:3d} ({pct:.1f}%)")

# 4. Style Tags (30 total - balanced assignment)
STYLE_TAGS = [
    # Modern (8)
    'minimalist', 'industrial', 'geometric', 'scandinavian', 'japandi', 'modern-farmhouse',
    'contemporary', 'transitional',
    # Classic (8)
    'vintage', 'traditional', 'art-deco', 'mid-century-modern', 'rustic', 'colonial',
    'mediterranean', 'bohemian',
    # Luxury (7)
    'gold-accents', 'marble-finish', 'designer', 'premium', 'luxury-minimal', 'elegant',
    'high-end',
    # Functional (7)
    'space-saving', 'wall-mounted', 'compact', 'double', 'smart', 'easy-clean',
    'water-efficient'
]

# Assign 2-3 style tags per product based on tier/category
product_style_tags = []
for p in products:
    tags = []
    
    # Tier-based tags
    if p['price_tier'] == 'premium':
        tags.extend(['luxury-minimal', 'marble-finish', 'gold-accents'])
    elif p['price_tier'] == 'mid':
        tags.extend(['contemporary', 'transitional', 'easy-clean'])
    else:  # budget
        tags.extend(['space-saving', 'compact', 'modern-farmhouse'])
    
    # Category-based tags
    if p['category'] == 'faucets':
        tags.append('water-efficient')
    elif p['category'] in ['bathtub', 'showers']:
        tags.append('easy-clean')
    elif p['category'] in ['toilets', 'sinks']:
        tags.append('smart')
    
    # Unique tags only
    tags = list(set(tags))[:3]
    
    for tag in tags:
        product_style_tags.append({
            'product_id': p['id'],
            'style_tag': tag
        })

# Write product_style_tags CSV
with open('/root/.openclaw/workspace/research/bathroom-products/product-style-tags.csv', 'w', newline='') as f:
    fieldnames = ['product_id', 'style_tag']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(product_style_tags)

print(f"\n✅ Style tags: {len(product_style_tags)} assignments ({len(STYLE_TAGS)} unique tags)")
