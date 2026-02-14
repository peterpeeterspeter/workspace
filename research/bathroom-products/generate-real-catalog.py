#!/usr/bin/env python3
"""
Generate real product catalog from actual downloaded images
Matches images to Duravit metadata and creates accurate CSV
"""

import json
import csv
import re
from pathlib import Path
from urllib.parse import quote

# Paths
BASE_DIR = Path("/root/.openclaw/workspace/research/bathroom-products")
RAW_IMAGES_DIR = BASE_DIR / "raw-images"
METADATA_DIR = BASE_DIR / "metadata"

# Load Duravit metadata
duravit_toilets = json.loads((METADATA_DIR / "duravit-toilets.json").read_text()) if (METADATA_DIR / "duravit-toilets.json").exists() else {"products": []}
duravit_sinks = json.loads((METADATA_DIR / "duravit-sinks.json").read_text()) if (METADATA_DIR / "duravit-sinks.json").exists() else {"products": []}
duravit_faucets = json.loads((METADATA_DIR / "duravit-faucets.json").read_text()) if (METADATA_DIR / "duravit-faucets.json").exists() else {"products": []}

# Map category to metadata
CATEGORY_METADATA = {
    "toilets": duravit_toilets,
    "sinks": duravit_sinks,
    "faucets": duravit_faucets,
}

# Price ranges by tier and category
PRICE_RANGES = {
    "toilets": {"budget": (150, 300), "mid-range": (300, 600), "premium": (600, 2500)},
    "sinks": {"budget": (200, 400), "mid-range": (400, 800), "premium": (800, 3500)},
    "faucets": {"budget": (60, 120), "mid-range": (120, 350), "premium": (350, 1200)},
    "showers": {"budget": (80, 200), "mid-range": (200, 500), "premium": (500, 2000)},
    "bathtub": {"budget": (300, 600), "mid-range": (600, 1500), "premium": (1500, 5500)},
    "vanity": {"budget": (200, 400), "mid-range": (400, 800), "premium": (800, 3500)},
    "lighting": {"budget": (40, 100), "mid-range": (100, 300), "premium": (300, 1500)},
    "tile": {"budget": (15, 35), "mid-range": (35, 70), "premium": (70, 200)},
}

# Brand mapping from filename patterns
BRAND_PATTERNS = {
    r"lumica": "Lumica",
    r"essential": "Essential Line",
    r"dura": "Duravit",
    r"vero": "Duravit",
    r"starck": "Duravit",
    r"happy": "Duravit",
    r"me.by": "Duravit",
    r"d-code": "Duravit",
    r"durasquare": "Duravit",
    r"lu": "Duravit",
    r"neo": "Duravit",
    r"architectura": "Differnz",
    r"terra": "Tiger",
    r"cerafit": "Vitra",
    r"xsquare": "Vitra",
    r"compact": "Keramag",
    r"basic": "Basic",
    r"eco": "Eco",
    r"value": "Value",
    r"standard": "Standard",
}

def extract_product_name(filename):
    """Extract readable product name from filename"""
    # Remove extension and path
    name = filename.stem
    # Replace dashes/hyphens with spaces
    name = re.sub(r'[-_]', ' ', name)
    # Remove numbers at end
    name = re.sub(r'\s*\d+$', '', name)
    # Capitalize words
    name = ' '.join(word.capitalize() for word in name.split())
    return name

def detect_brand(filename):
    """Detect brand from filename patterns"""
    name_lower = filename.stem.lower()
    for pattern, brand in BRAND_PATTERNS.items():
        if pattern in name_lower:
            return brand
    return "Standard"  # Default fallback

def find_matching_metadata(category, filename):
    """Try to find matching Duravit product"""
    if category not in CATEGORY_METADATA:
        return None

    metadata = CATEGORY_METADATA[category]
    if not metadata.get("products"):
        return None

    # Try to match by series or product_id
    name_lower = filename.stem.lower()

    for product in metadata["products"]:
        series = product.get("series", "").lower().replace("_", "")
        if series and series in name_lower:
            return product

    return None

def get_category_from_path(path_obj):
    """Extract category from path"""
    parts = path_obj.parts
    if "raw-images" in parts:
        idx = parts.index("raw-images")
        if idx + 1 < len(parts):
            return parts[idx + 1]
    return None

def get_tier_from_path(path_obj):
    """Extract price tier from path"""
    parts = path_obj.parts
    tier = parts[-2] if len(parts) >= 2 else "premium"
    return tier

def generate_description(brand, name, category, tier):
    """Generate product description"""
    tier_desc = {
        "budget": "Essential products - Practical and affordable. Perfect for budget-conscious renovations without compromising quality.",
        "mid-range": "Reliable quality and contemporary design. Ideal for modern renovation projects.",
        "premium": f"Premium {category} from {brand}. High-quality design and materials for luxury bathrooms. Part of the premium collection.",
    }
    return tier_desc.get(tier, tier_desc["premium"])

# Scan all images and build product catalog
products = {}
product_id = 1

print("🔍 Scanning images...")
image_files = list(RAW_IMAGES_DIR.rglob("*.jpg")) + list(RAW_IMAGES_DIR.rglob("*.webp"))

for image_path in image_files:
    # Skip WebP copies (we'll use the JPG as reference)
    if image_path.suffix == ".webp":
        continue

    category = get_category_from_path(image_path)
    if not category:
        continue

    tier = get_tier_from_path(image_path)
    tier_key = tier.replace("-", "")  # mid-range -> midrange

    # Extract product info
    brand = detect_brand(image_path)
    product_name = extract_product_name(image_path)

    # Create unique key for product (brand + name + category + tier)
    product_key = f"{brand}_{product_name}_{category}_{tier}".lower().replace(" ", "_")

    if product_key not in products:
        # Get price range
        price_low, price_high = PRICE_RANGES.get(category, {}).get(tier_key, (100, 500))

        # Try to find matching metadata
        metadata = find_matching_metadata(category, image_path)

        # Use metadata values if available
        if metadata:
            sku = metadata.get("sku", f"{brand.upper()}-{product_id}")
            dimensions = metadata.get("dimensions", "")
        else:
            sku = f"{brand.upper()}-{product_id:04d}"
            dimensions = ""

        # Build image paths
        relative_path = image_path.relative_to(RAW_IMAGES_DIR)
        webp_path = str(relative_path).replace(".jpg", ".webp")

        products[product_key] = {
            "id": product_id,
            "brand": brand,
            "name": product_name,
            "category": category,
            "price_tier": tier,
            "price_low": price_low,
            "price_high": price_high,
            "currency": "EUR",
            "image_url": f"https://wgassets.duravit.cloud/photomanager-duravit/{quote(str(relative_path))}",
            "catalog_image_path": webp_path,
            "render_image_path": webp_path,
            "origin": "catalog-2026",
            "is_active": True,
            "display_order": product_id,
            "description": generate_description(brand, product_name, category, tier),
            "sku": sku,
            "dimensions": dimensions,
        }
        product_id += 1

# Write to CSV
output_file = BASE_DIR / "product-catalog-REAL.csv"
fieldnames = [
    "id", "brand", "name", "category", "price_tier", "price_low", "price_high",
    "currency", "image_url", "catalog_image_path", "render_image_path",
    "origin", "is_active", "display_order", "description"
]

print(f"📝 Writing {len(products)} products to {output_file}...")
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for product in sorted(products.values(), key=lambda x: x["id"]):
        row = {k: v for k, v in product.items() if k in fieldnames}
        writer.writerow(row)

print(f"✅ Done! Generated {len(products)} real products")
print(f"\n📊 Summary:")
for category in sorted(set(p["category"] for p in products.values())):
    count = sum(1 for p in products.values() if p["category"] == category)
    print(f"  {category}: {count} products")

print(f"\n📁 Output: {output_file}")
