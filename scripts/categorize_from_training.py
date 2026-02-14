#!/usr/bin/env python3
"""
Categorize bathroom products based on training data from Vision AI analysis
Uses: Brand patterns, Product name patterns, Training confidence scores
"""

import csv
import json
import re
from collections import defaultdict

# Vision AI Training Data (from 175 Rorix products analyzed previously)
TRAINING_PATTERNS = {
    # Bathtub patterns
    'Bathtub': {
        'keywords': ['bad', 'ligbad', 'hoekbad', 'whirlpool', 'whirlpool', 'half vrijstaand', 'vrijstaand', 'inloop'],
        'brands': ['Duravit', 'Villeroy & Boch', 'Riho', 'Ideavit', 'Looox', 'Royal Plaza', 'Wiesbaden', 'Zeza', 'Xenz'],
        'excludes': ['toilet', 'closet', 'urinoir', 'douche wc']
    },
    
    # Shower patterns
    'Shower': {
        'keywords': ['douche', 'shower', 'inloopdouche', 'douchecabine', 'douchewand'],
        'brands': ['Villeroy & Boch', 'Grohe', 'Kaldewei', 'Huppe', 'Duravit'],
        'excludes': ['wc', 'toilet', 'closet']
    },
    
    # Vanity patterns
    'Vanity': {
        'keywords': ['wastafel', 'wasbak', 'waskomen', 'meubel', 'spiegel', 'wastafelkraan'],
        'brands': ['Duravit', 'Villeroy & Boch', 'Geberit', 'Grohe', 'Villeroy & Boch', 'Alape'],
        'excludes': ['led', 'toilet', 'closet', 'douche']
    },
    
    # Toilet patterns
    'Toilet': {
        'keywords': ['toilet', 'closet', 'urinoir', 'bidet', 'wandcloset', 'staand closet', 'diepspoel', 'vlakspoel'],
        'brands': ['Geberit', 'Grohe', 'Villeroy & Boch', 'Jika', 'Adema', 'Ideal Standard', 'Nemo Spring', 'Wisa', 'QeramiQ', 'Sanibroyeur'],
        'excludes': []
    },
    
    # Faucet patterns
    'Faucet': {
        'keywords': ['kraan', 'mengkraan', 'wastafelkraan', 'douchekraan'],
        'brands': ['Grohe', 'Villeroy & Boch', 'Huppe', 'Kaldewei'],
        'excludes': ['toilet', 'bad', 'spiegel']
    },
    
    # Lighting patterns
    'Lighting': {
        'keywords': ['spiegel led', 'lamp', 'licht', 'led spiegel', 'lichtarmatuur'],
        'brands': ['Hotbath', 'INK', 'Wiesbaden'],
        'excludes': ['toilet', 'bad', 'kraan']
    },
    
    # Tile patterns
    'Tile': {
        'keywords': ['tegel', 'mozaiek', 'tile', 'wandtegel'],
        'brands': ['Sanibroyeur', 'Villeroy & Boch'],
        'excludes': []
    }
}

# Brand quality tiers (from training data)
BRAND_TIERS = {
    'premium': ['Villeroy & Boch', 'Duravit', 'Geberit', 'Grohe'],
    'mid_range': ['Riho', 'Ideavit', 'Looox', 'Wiesbaden'],
    'budget': ['Jika', 'Adema', 'Wisa', 'QeramiQ', 'Nemo Spring', 'Xenz', 'Zeza', 'Xellanz', 'Royal Plaza']
}

def score_category(product_name, brand, category):
    """Score a category match based on training patterns"""
    score = 0
    reasons = []
    
    name_lower = product_name.lower()
    
    # Check keyword matches
    patterns = TRAINING_PATTERNS.get(category, {})
    keywords = patterns.get('keywords', [])
    
    for keyword in keywords:
        if keyword in name_lower:
            if keyword in ['bad', 'ligbad', 'hoekbad']:
                score += 30  # Strong indicator for bathtub
            elif keyword in ['toilet', 'closet', 'urinoir']:
                score += 30  # Strong indicator for toilet
            elif keyword in ['spiegel', 'led']:
                score += 25  # Strong indicator for lighting/vanity
            else:
                score += 20  # Good indicator
            reasons.append(f"Keyword match: '{keyword}'")
    
    # Check brand strength
    if brand in BRAND_TIERS.get('premium', []):
        score += 15
        reasons.append(f"Premium brand: '{brand}'")
    elif brand in BRAND_TIERS.get('mid_range', []):
        score += 10
        reasons.append(f"Mid-range brand: '{brand}'")
    elif brand in BRAND_TIERS.get('budget', []):
        score += 5
        reasons.append(f"Budget brand: '{brand}'")
    
    # Check brand-category alignment
    brand_categories = patterns.get('brands', [])
    if brand in brand_categories:
        score += 25
        reasons.append(f"Brand known for '{category}'")
    
    return score, reasons

def categorize_product(product_name_raw, brand, old_category=None):
    """Categorize a single product using training data"""
    name_lower = product_name_raw.lower()
    
    scores = {}
    all_reasons = {}
    
    # Score each category
    for category in TRAINING_PATTERNS.keys():
        score, reasons = score_category(product_name_raw, brand, category)
        
        # Apply exclusion rules
        patterns = TRAINING_PATTERNS[category]
        for exclude in patterns.get('excludes', []):
            if exclude in name_lower:
                score = 0
                reasons = [f"Excluded: '{exclude}' in name"]
                break
        
        scores[category] = score
        all_reasons[category] = reasons
    
    # Find winning category
    if not scores or max(scores.values()) == 0:
        return 'Toilet', ['Uncategorized - defaulted to toilet'], 0
    
    winning_category = max(scores, key=scores.get)
    winning_score = scores[winning_category]
    winning_reasons = all_reasons[winning_category]
    
    # Calculate confidence
    total_score = sum(scores.values())
    confidence = (winning_score / total_score * 100) if total_score > 0 else 0
    
    # Special handling for mirrors
    if 'spiegel' in name_lower:
        if 'led' in name_lower:
            winning_category = 'Lighting'
            winning_reasons = ["LED mirror detected"]
            confidence = 95
        else:
            # Check if it's a mirror-only product (vanity) or part of toilet set
            if 'toilet' in name_lower or 'closet' in name_lower:
                winning_category = 'Toilet'
                winning_reasons = ["Mirror part of toilet set"]
                confidence = 85
            else:
                winning_category = 'Vanity'
                winning_reasons = ["Non-LED mirror"]
                confidence = 80
    
    # Special handling for "douche wc" (shower toilet = TOILET, not shower)
    if 'douche wc' in name_lower or 'wc douche' in name_lower:
        winning_category = 'Toilet'
        winning_reasons = ["Shower toilet = toilet category"]
        confidence = 90
    
    # Special handling for bathtubs with fixtures
    if 'bad' in name_lower and any(w in name_lower for w in ['kraan', 'waste', 'sifon']):
        winning_category = 'Bathtub'
        winning_reasons = ["Bathtub with fixture accessory"]
        confidence = 85
    
    return winning_category, winning_reasons, confidence

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Gebruik: python3 categorize_from_training.py <input_csv>")
        sys.exit(1)
    
    input_csv = sys.argv[1]
    output_csv = input_csv.replace('.csv', '_categorized.csv')
    
    print(f"🏷️ Bathroom Product Categorizer")
    print(f"=" * 50)
    print(f"Input: {input_csv}")
    print(f"Output: {output_csv}")
    print()
    
    # Read products
    products = []
    with open(input_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        
        for row in reader:
            products.append(row)
    
    print(f"📊 Found {len(products)} products to categorize")
    print()
    
    # Categorize each product
    results = []
    category_counts = defaultdict(int)
    confidence_distribution = defaultdict(int)
    
    for i, product in enumerate(products, 1):
        name_raw = product.get('name_raw', product.get('name', ''))
        brand = product.get('brand', 'Unknown')
        old_category = product.get('category', '')
        
        # Categorize using training data
        category, reasons, confidence = categorize_product(name_raw, brand, old_category)
        
        # Update product
        product['category'] = category
        product['old_category'] = old_category
        product['confidence'] = confidence
        product['reasons'] = '; '.join(reasons)
        
        results.append(product)
        category_counts[category] += 1
        confidence_distribution[confidence // 10 * 10] += 1
        
        # Progress indicator
        if i % 100 == 0 or i == len(products):
            print(f"[{i:4d}/{len(products):4d}] {name_raw[:60]:60} → {category} ({confidence: .0f}% confidence)")
    
    print()
    print("=" * 50)
    print("✅ CATEGORIZATION COMPLETE")
    print("=" * 50)
    print()
    
    # Summary statistics
    print("📊 Category Distribution:")
    for cat in ['Bathtub', 'Shower', 'Vanity', 'Toilet', 'Faucet', 'Lighting', 'Tile']:
        count = category_counts.get(cat, 0)
        percentage = (count / len(products) * 100) if products else 0
        print(f"  {cat:15s}: {count:4d} ({percentage:5.1f}%)")
    
    print()
    print("🎯 Confidence Distribution:")
    for conf_range in [(90, 100), (80, 89), (70, 79), (60, 69), (0, 59)]:
        count = confidence_distribution[conf_range]
        pct = (count / len(products) * 100) if products else 0
        print(f"  {conf_range[0]}-{conf_range[1]}%: {count:4d} ({pct:5.1f}%)")
    
    print()
    print(f"💾 Output: {output_csv}")
    print()
    
    # Write to CSV
    with open(output_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    
    print(f"✅ Saved {len(results)} categorized products to {output_csv}")
    print()
    print("📝 Next Steps:")
    print("1. Review products with confidence <80%")
    print("2. Spot-check 10-20 random products")
    print("3. Import to Supabase/DeBadkamer.com")

if __name__ == '__main__':
    main()
