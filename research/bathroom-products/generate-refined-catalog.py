#!/usr/bin/env python3
"""
Generate refined product catalog (~100 products)
- Exact price ranges from spec
- Realistic brand names
- Dual image system (catalog + render)
- Balanced tier/category distribution
"""

import csv
import random

# Exact price ranges from spec (EUR)
PRICE_RANGES = {
    'faucets': {
        'budget': (60, 120),
        'mid': (120, 350),
        'premium': (350, 1200)
    },
    'toilets': {
        'budget': (150, 300),
        'mid': (300, 600),
        'premium': (600, 2500)
    },
    'showers': {
        'budget': (80, 200),
        'mid': (200, 500),
        'premium': (500, 2000)
    },
    'vanity': {
        'budget': (200, 400),
        'mid': (400, 800),
        'premium': (800, 3500)
    },
    'tile': {
        'budget': (15, 35),
        'mid': (35, 70),
        'premium': (70, 200)
    },
    'lighting': {
        'budget': (40, 100),
        'mid': (100, 300),
        'premium': (300, 1500)
    },
    'bathtub': {
        'budget': (300, 600),
        'mid': (600, 1500),
        'premium': (1500, 5500)
    }
}

# Realistic brand names
BRANDS = {
    'premium': ['Grohe', 'Hansgrohe', 'Duravit', 'Villeroy & Boch', 'Geberit', 'Laufen'],
    'mid': ['Ideal Standard', 'Wisa', 'Tiger', 'Differnz', 'Vitra', 'Keramag'],
    'budget': ['Essential Line', 'Basic', 'Standard', 'Eco', 'Value']
}

# Product name templates
PRODUCT_TEMPLATES = {
    'faucets': {
        'premium': ['Allure', 'Pura', 'K7', 'Metris', 'Wave', 'Edge', 'Plus', 'Grandera'],
        'mid': ['Cerafit', 'Ceralook', 'Ceraplan Neo', 'Cerafine O', 'Mixer', 'Select'],
        'budget': ['Single Lever', 'Standard Mixer', 'Basic Faucet', 'Eco Tap', 'Essential']
    },
    'toilets': {
        'premium': ['Starck 3', 'DuraStyle', 'ME by Starck', 'Architec', 'Happy D.2', 'Vero Air'],
        'mid': ['Omnia Architectura', 'Subway', 'Terra', 'Aqua Circle', 'Basic Round'],
        'budget': ['Compact WC', 'Standard Toilet', 'Eco Toilet', 'Space Saver']
    },
    'showers': {
        'premium': ['Rainshower', 'Euphoria', 'Senses', 'Power & Soul', 'Vernetto'],
        'mid': ['Creshower', 'Thermostat', 'Basic Shower', 'Rail Set', 'Handshower'],
        'budget': ['Standard Shower', 'Eco Shower Head', 'Basic Rail', 'Value Set']
    },
    'vanity': {
        'premium': ['L-Cube', 'ME by Starck', 'DuraSquare', 'Architec', 'Noble'],
        'mid': ['XSquare', 'Connect', 'Basic Vanity', 'Standard Cabinet', 'Compact'],
        'budget': ['Essential Vanity', 'Basic Cabinet', 'Value Unit', 'Eco Sink']
    },
    'tile': {
        'premium': ['Natural Stone', 'Marble Collection', 'Ceramic Luxury', 'Designer Series'],
        'mid': ['Metro Tiles', 'Hexagon Mosaic', 'Standard Ceramic', 'Basic Porcelain'],
        'budget': ['Essential Tile', 'Value Ceramic', 'Basic White', 'Eco Stone']
    },
    'lighting': {
        'premium': ['LED Premium', 'Design Light', 'Luxury Illumination', 'Designer Series'],
        'mid': ['Standard LED', 'Basic Light', 'Compact LED', 'Value Illumination'],
        'budget': ['Essential Light', 'Eco LED', 'Basic Bulb', 'Value Fixture']
    },
    'bathtub': {
        'premium': ['Oval Freestanding', 'Designer Tub', 'Luxury Bath', 'Stone Collection'],
        'mid': ['Standard Tub', 'Basic Bath', 'Acrylic Bath', 'Compact Soaker'],
        'budget': ['Essential Bath', 'Value Tub', 'Eco Bathtub', 'Basic Soaker']
    }
}

# Generate ~100 products matching exact distribution
products = []
product_id = 1

# Distribution targets from spec
DISTRIBUTION = {
    'faucets': {'budget': 3, 'mid': 4, 'premium': 5},
    'toilets': {'budget': 3, 'mid': 4, 'premium': 3},
    'showers': {'budget': 3, 'mid': 4, 'premium': 4},
    'vanity': {'budget': 3, 'mid': 4, 'premium': 3},
    'tile': {'budget': 4, 'mid': 5, 'premium': 4},
    'lighting': {'budget': 3, 'mid': 4, 'premium': 3},
    'bathtub': {'budget': 3, 'mid': 4, 'premium': 3}
}

for category, tiers in DISTRIBUTION.items():
    for tier, count in tiers.items():
        brands = BRANDS[tier]
        templates = PRODUCT_TEMPLATES[category][tier]
        
        for i in range(count):
            brand = random.choice(brands)
            template = random.choice(templates)
            
            # Generate unique product name
            if tier == 'budget' and 'Essential' in brand:
                name = f"{template} {i+1}"
            else:
                name = f"{brand} {template}"
            
            # Get exact price range
            price_low, price_high = PRICE_RANGES[category][tier]
            
            # Generate storage paths
            product_slug = name.lower().replace(' ', '-').replace('/', '-')
            catalog_path = f"product-images/{category}/{product_slug}-catalog.webp"
            render_path = f"product-images/{category}/{product_slug}-render.webp"
            
            # Description
            descriptions = {
                'premium': f"Premium {category} from {brand}. High-quality design and materials for luxury bathrooms. Part of the {tier} collection.",
                'mid': f"{brand} {category} - Reliable quality and contemporary design. Ideal for modern renovation projects.",
                'budget': f"Essential {category} - Practical and affordable. Perfect for budget-conscious renovations without compromising quality."
            }
            
            product = {
                'id': product_id,
                'brand': brand,
                'name': name,
                'category': category,
                'price_tier': tier,
                'price_low': price_low,
                'price_high': price_high,
                'currency': 'EUR',
                'image_url': f'https://cdn.example.com/products/{product_slug}.jpg',
                'catalog_image_path': catalog_path,
                'render_image_path': render_path,
                'origin': 'catalog-2026',
                'is_active': True,
                'display_order': product_id,
                'description': descriptions[tier]
            }
            
            products.append(product)
            product_id += 1

# Write CSV
output_file = '/root/.openclaw/workspace/research/bathroom-products/product-catalog-refined.csv'
fieldnames = ['id', 'brand', 'name', 'category', 'price_tier', 'price_low', 'price_high', 
              'currency', 'image_url', 'catalog_image_path', 'render_image_path', 'origin', 'is_active', 'display_order', 'description']

with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(products)

print(f"✅ Refined Product Catalog Generated")
print(f"   File: {output_file}")
print(f"   Total Products: {len(products)}")

# Distribution summary
from collections import defaultdict
tier_counts = defaultdict(int)
category_counts = defaultdict(int)

for p in products:
    tier_counts[p['price_tier']] += 1
    category_counts[p['category']] += 1

print(f"\n📊 Tier Distribution:")
for tier in ['budget', 'mid', 'premium']:
    count = tier_counts[tier]
    pct = (count / len(products)) * 100
    print(f"   {tier:8s}: {count:2d} ({pct:.1f}%)")

print(f"\n📁 Category Distribution:")
for cat in sorted(category_counts.keys()):
    count = category_counts[cat]
    print(f"   {cat:10s}: {count:2d}")

print(f"\n💰 Price Range Examples:")
for tier in ['budget', 'mid', 'premium']:
    samples = [p for p in products if p['price_tier'] == tier][:2]
    print(f"   {tier.upper()}:")
    for p in samples:
        print(f"      {p['brand']} {p['category']}: €{p['price_low']}–€{p['price_high']}")
