#!/bin/bash
# Download Sawiday Product Images
# Instructions: Run from /root/.openclaw/workspace/research/bathroom-products/scripts

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

# Count total images
TOTAL=$(python3 << 'EOF'
import json
with open("data/supabase/product_images.json", "r") as f:
    data = json.load(f)
    print(f"Total images to download: {len(data)}")
EOF
)

echo ""
echo "📊 Found $TOTAL images to download"
echo ""

# Counter for progress
COUNTER=0
SUCCESS=0
FAILED=0

# Download images
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

for i, img in enumerate(images, 1):
    url = img.get('image_url')
    product_id = img.get('product_id')
    
    if not url:
        print(f"⚠️  {i}/{len(images)}: No URL for product {product_id}")
        FAILED += 1
        continue
    
    try:
        # Create filename
        ext = '.jpg'  # Most are JPEG
        # Use first 10 chars of product_id + counter to ensure uniqueness
        safe_product_id = product_id.replace('/', '-')[:10]
        filename = f"{safe_product_id}_{i:03d}{ext}"
        
        # Full path
        output_path = output_dir / filename
        
        # Download
        urllib.request.urlretrieve(url, output_path)
        
        COUNTER += 1
        SUCCESS += 1
        
        # Progress bar every 10 images
        if COUNTER % 10 == 0 or i == len(images):
            progress = (COUNTER / len(images)) * 100
            print(f"[{progress:5.0f}%] {COUNTER}/{len(images)} downloaded...")
        
    except Exception as e:
        print(f"❌ {i}/{len(images)}: {e}")
        FAILED += 1
        continue

print()
print("=" * 60)
print("✅ DOWNLOAD COMPLETE!")
print(f"Total: {len(images)}")
print(f"Success: {SUCCESS}")
print(f"Failed: {FAILED}")
print()
print(f"📁 Images saved to: {output_dir.absolute}")
print("=" * 60)
EOF

echo ""
echo "✅ Download complete!"
echo ""
echo "📁 Images location: data/images/products/"
echo ""
echo "📊 Statistics:"
echo "   Total processed: $TOTAL"
echo "   Successful: $SUCCESS"
echo "   Failed: $FAILED"
echo ""
echo "💡 Next step: Upload images to Supabase storage"
