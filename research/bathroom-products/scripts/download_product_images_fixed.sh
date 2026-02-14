#!/bin/bash
# Download Sawiday Product Images (FIXED)
# Instructions: Run from /root/.openclaw/workspace/research/bathroom-products

set -e

echo "🖼️  SAWIDAY PRODUCT IMAGE DOWNLOADER"
echo "======================================"
echo ""

# Check if product_images.json exists
if [ ! -f "data/supabase/product_images.json" ]; then
    echo "❌ Error: product_images.json not found!"
    echo "Expected location: data/supabase/product_images.json"
    echo "Run transform_to_supabase.py first to generate it."
    exit 1
fi

# Create output directory for images
mkdir -p data/images/products

echo "📊 Downloading from Sawiday.be..."
echo ""

# Download images (all in Python)
python3 << 'EOF'
import json
import os
import urllib.request
from pathlib import Path

# Load image data
with open("data/supabase/product_images.json", "r") as f:
    images = json.load(f)

# Create output directory
output_dir = Path("data/images/products")
output_dir.mkdir(parents=True, exist_ok=True)

print(f"Downloading {len(images)} images...")
print("Press Ctrl+C to stop - progress is saved")
print("")

# Initialize counters
counter = 0
success = 0
failed = 0

for i, img in enumerate(images, 1):
    url = img.get('image_url')
    product_id = img.get('product_id', 'unknown')
    
    if not url:
        print(f"⚠️  {i}/{len(images)}: No URL for product {product_id}")
        failed += 1
        continue
    
    try:
        # Create filename
        ext = '.jpg'  # Most are JPEG
        # Use first 10 chars of product_id + counter to ensure uniqueness
        safe_product_id = str(product_id).replace('/', '-')[:10]
        filename = f"{safe_product_id}_{i:04d}{ext}"
        
        # Full path
        output_path = output_dir / filename
        
        # Download with timeout
        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(request, timeout=30) as response:
            with open(output_path, 'wb') as f:
                f.write(response.read())
        
        counter += 1
        success += 1
        
        # Progress bar every 10 images
        if counter % 10 == 0 or i == len(images):
            progress = (counter / len(images)) * 100
            print(f"[{progress:5.1f}%] {counter}/{len(images)} downloaded...")
        
    except Exception as e:
        print(f"❌ {i}/{len(images)}: {str(e)[:80]}")
        failed += 1
        continue

print()
print("=" * 78)
print("✅ DOWNLOAD COMPLETE!")
print(f"Total: {len(images)}")
print(f"Success: {success}")
print(f"Failed: {failed}")
print()
print(f"📁 Images saved to: {output_dir.absolute()}")
print("=" * 78)
EOF

echo ""
echo "💡 Next step: Upload images to Supabase storage"
