#!/usr/bin/env python3
"""
Bathroom Product Data Transformation Pipeline
=============================================

Steps:
1. Flatten: category → brand → product[] into flat rows
2. Dedupe: Pick 1 size per model, keep color variants
3. Map categories: baden→Bathtub, douche→Shower, etc.
4. Classify tiers: based on price + category thresholds
5. Pick best image: [0] for catalog, cleanest product-shot for render
6. Generate ID: brand-model-variant slug
7. Dedupe images: remove duplicate URLs per product

Output: CSV for import + image download list
"""

import json
import csv
import re
import os
from pathlib import Path
from collections import defaultdict
from urllib.parse import urlparse
from typing import List, Dict, Set, Tuple
import hashlib


# ============================================================================
# CONFIGURATION
# ============================================================================

INPUT_DIR = Path("/root/.openclaw/workspace/research/bathroom-products")
OUTPUT_DIR = INPUT_DIR / "processed"
OUTPUT_DIR.mkdir(exist_ok=True)

# Category mapping (Dutch → English)
CATEGORY_MAPPING = {
    "baden": "Bathtub",
    "douche": "Shower",
    "toiletten": "Toilet",
    "wastafels": "Vanity",
    "kranen": "Faucet",
    "spiegels": "Mirror",
    "tegels": "Tile",
    "badkamer-meubelsets": "Vanity Set",
}

# Tier thresholds by category (price in EUR)
TIER_THRESHOLDS = {
    "Bathtub": {"budget": 300, "mid": 600},
    "Shower": {"budget": 200, "mid": 400},
    "Toilet": {"budget": 150, "mid": 300},
    "Vanity": {"budget": 200, "mid": 500},
    "Faucet": {"budget": 80, "mid": 150},
    "Mirror": {"budget": 100, "mid": 200},
    "Tile": {"budget": 50, "mid": 100},
    "Vanity Set": {"budget": 300, "mid": 700},
}


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')


def extract_model_name(name: str) -> str:
    """
    Extract base model name by removing size/color variations.
    Examples:
        "Zeza Oval ligbad 190x90cm" → "zeza-oval-ligbad"
        "Zeza Oval ligbad 170x70cm" → "zeza-oval-ligbad"
    """
    # Remove dimensions (e.g., 190x90cm, 60x46x55cm)
    model = re.sub(r'\d+[xX]\d+(?:[xX]\d+)?(?:cm)?', '', name)
    # Remove extra whitespace
    model = ' '.join(model.split())
    return model


def generate_product_id(brand: str, name: str) -> str:
    """Generate unique product ID: brand-model-variant slug."""
    model = extract_model_name(name)
    return f"{slugify(brand)}-{slugify(model)}"


def classify_tier(category: str, price: float) -> str:
    """Classify product into budget/mid/premium tier."""
    if category not in TIER_THRESHOLDS:
        return "mid"

    thresholds = TIER_THRESHOLDS[category]
    if price < thresholds["budget"]:
        return "budget"
    elif price < thresholds["mid"]:
        return "mid"
    else:
        return "premium"


def dedupe_images(images: List[str]) -> List[str]:
    """Remove duplicate image URLs within a product."""
    seen = set()
    deduped = []
    for img in images:
        if img not in seen:
            seen.add(img)
            deduped.append(img)
    return deduped


def pick_best_images(images: List[str]) -> Tuple[str, str]:
    """
    Pick best images for catalog and render.
    Returns: (catalog_image_url, render_image_url)
    """
    if not images:
        return "", ""

    deduped = dedupe_images(images)

    # Catalog: first image (typically hero shot)
    catalog_image = deduped[0] if deduped else ""

    # Render: pick last image (often detail/angle shot) or second if only 2
    render_image = deduped[-1] if len(deduped) > 1 else catalog_image

    return catalog_image, render_image


# ============================================================================
# MAIN TRANSFORMATION PIPELINE
# ============================================================================

def load_json_files() -> Dict[str, Dict]:
    """Load all JSON files from input directory."""
    all_data = {}
    json_files = list(INPUT_DIR.glob("*.json"))

    print(f"📂 Loading {len(json_files)} JSON files...")

    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

                # Handle different JSON formats
                # Format 1: {"category": {brand: [products]}}
                if isinstance(data, dict):
                    # Check if nested {"baden": {brand: [...]}}
                    first_val = next(iter(data.values())) if data else None
                    if first_val and isinstance(first_val, dict):
                        # Multi-category format
                        for category, brands in data.items():
                            if category not in all_data:
                                all_data[category] = {}
                            all_data[category].update(brands)
                    elif first_val and isinstance(first_val, list):
                        # Already flattened to brand level: {brand: [products]}
                        # These are pre-processed, skip for now
                        pass

                # Format 2: [{products}] - skip, already processed
                elif isinstance(data, list):
                    # List of products - skip, already processed
                    pass

                print(f"  ✓ {json_file.name}")
        except Exception as e:
            print(f"  ✗ {json_file.name}: {e}")

    return all_data


def flatten_data(raw_data: Dict[str, Dict]) -> List[Dict]:
    """Step 1: Flatten category → brand → products[] into flat rows."""
    flat_products = []

    for category_dutch, brands_or_nested in raw_data.items():
        category_english = CATEGORY_MAPPING.get(category_dutch.lower(), category_dutch)

        # Handle nested structure: {"baden": {"Zeza": [products]}}
        # vs flat structure: {"Zeza": [products]}
        
        # Check if values are nested (dict of dicts) or flat (dict of lists)
        first_val = next(iter(brands_or_nested.values())) if brands_or_nested else None
        
        if first_val and isinstance(first_val, dict):
            # Nested structure - need to go one level deeper
            for nested_key, brands in brands_or_nested.items():
                if not isinstance(brands, dict):
                    continue
                for brand, products in brands.items():
                    if not isinstance(products, list):
                        continue
                    for product in products:
                        flat_products.append({
                            "category_original": category_dutch,
                            "category": category_english,
                            "brand": brand,
                            "name": product.get("name", ""),
                            "url": product.get("url", ""),
                            "price": product.get("price", 0),
                            "images": product.get("images", []),
                        })
        elif first_val and isinstance(first_val, list):
            # Flat structure - brands directly map to product lists
            for brand, products in brands_or_nested.items():
                if not isinstance(products, list):
                    continue
                for product in products:
                    flat_products.append({
                        "category_original": category_dutch,
                        "category": category_english,
                        "brand": brand,
                        "name": product.get("name", ""),
                        "url": product.get("url", ""),
                        "price": product.get("price", 0),
                        "images": product.get("images", []),
                    })

    print(f"\n📊 Flattened {len(flat_products)} products")
    return flat_products


def dedupe_by_model(products: List[Dict]) -> List[Dict]:
    """
    Step 2: Dedupe - pick 1 size per model, keep color variants.

    Strategy:
    - Group by base model name
    - Keep first size variant encountered
    - Keep all color/material variants (different model names)
    """
    model_groups = defaultdict(list)

    # Group by base model
    for product in products:
        model_base = extract_model_name(product["name"])
        model_groups[model_base].append(product)

    deduped = []
    skipped = 0

    for model_base, variants in model_groups.items():
        # Keep first variant (one size per model)
        # Color/material variants will have different base names
        deduped.append(variants[0])
        skipped += len(variants) - 1

    print(f"\n🔄 Deduped products:")
    print(f"  - Kept: {len(deduped)} unique models")
    print(f"  - Skipped: {skipped} size variants")

    return deduped


def transform_products(products: List[Dict]) -> List[Dict]:
    """Apply transformations: tier classification, image selection, ID generation."""
    transformed = []

    for p in products:
        # Step 4: Classify tier
        tier = classify_tier(p["category"], p["price"])

        # Step 5 & 7: Pick best images + dedupe images
        images = dedupe_images(p["images"])
        catalog_image, render_image = pick_best_images(images)

        # Step 6: Generate product ID
        product_id = generate_product_id(p["brand"], p["name"])

        transformed.append({
            "product_id": product_id,
            "category": p["category"],
            "brand": p["brand"],
            "name": p["name"],
            "model_name": extract_model_name(p["name"]),
            "price": p["price"],
            "tier": tier,
            "url": p["url"],
            "catalog_image": catalog_image,
            "render_image": render_image,
            "total_images": len(images),
        })

    return transformed


def export_csv(products: List[Dict]) -> Path:
    """Export products to CSV for database import."""
    csv_path = OUTPUT_DIR / "bathroom_products_import.csv"

    fieldnames = [
        "product_id",
        "category",
        "brand",
        "name",
        "model_name",
        "price",
        "tier",
        "url",
        "catalog_image",
        "render_image",
        "total_images",
    ]

    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)

    print(f"\n💾 Exported CSV: {csv_path}")
    print(f"   ({len(products)} products)")

    return csv_path


def export_image_list(products: List[Dict]) -> Tuple[Path, int]:
    """Export list of all images for download."""
    images_path = OUTPUT_DIR / "image_download_list.txt"
    total_images = 0

    with open(images_path, 'w', encoding='utf-8') as f:
        for p in products:
            # Write catalog images
            if p["catalog_image"]:
                f.write(f"{p['product_id']}|catalog|{p['catalog_image']}\n")
                total_images += 1

            # Write render images (if different)
            if p["render_image"] and p["render_image"] != p["catalog_image"]:
                f.write(f"{p['product_id']}|render|{p['render_image']}\n")
                total_images += 1

    print(f"\n🖼️  Image download list: {images_path}")
    print(f"   ({total_images} unique images to download)")

    return images_path, total_images


def print_summary(products: List[Dict]):
    """Print transformation summary."""
    print("\n" + "="*60)
    print("📈 TRANSFORMATION SUMMARY")
    print("="*60)

    # Count by category
    category_counts = defaultdict(int)
    tier_counts = defaultdict(int)
    brand_counts = defaultdict(int)

    for p in products:
        category_counts[p["category"]] += 1
        tier_counts[p["tier"]] += 1
        brand_counts[p["brand"]] += 1

    print("\n📦 Products by Category:")
    for cat, count in sorted(category_counts.items()):
        print(f"  - {cat}: {count}")

    print("\n💰 Products by Tier:")
    for tier in ["budget", "mid", "premium"]:
        count = tier_counts.get(tier, 0)
        if count:
            print(f"  - {tier.capitalize()}: {count}")

    print("\n🏭 Top 10 Brands:")
    for brand, count in sorted(brand_counts.items(), key=lambda x: -x[1])[:10]:
        print(f"  - {brand}: {count}")

    price_range = [p["price"] for p in products]
    if price_range:
        print(f"\n💵 Price Range:")
        print(f"  - Min: €{min(price_range):.2f}")
        print(f"  - Max: €{max(price_range):.2f}")
        print(f"  - Avg: €{sum(price_range)/len(price_range):.2f}")

    print("\n" + "="*60)


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    print("\n" + "="*60)
    print("🔧 BATHROOM PRODUCT DATA TRANSFORMATION PIPELINE")
    print("="*60 + "\n")

    # Step 1: Load JSON files
    raw_data = load_json_files()
    if not raw_data:
        print("\n❌ No data found! Check input directory.")
        return

    # Step 1: Flatten data
    flat_products = flatten_data(raw_data)

    # Step 2: Dedupe by model
    deduped_products = dedupe_by_model(flat_products)

    # Steps 3-6: Transform products
    final_products = transform_products(deduped_products)

    # Export CSV
    csv_path = export_csv(final_products)

    # Export image list
    images_path, total_images = export_image_list(final_products)

    # Print summary
    print_summary(final_products)

    print(f"\n✅ Pipeline complete!")
    print(f"\nNext steps:")
    print(f"1. Review CSV: {csv_path}")
    print(f"2. Download images using: {images_path}")
    print(f"3. Import CSV into database")


if __name__ == "__main__":
    main()
