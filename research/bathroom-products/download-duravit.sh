#!/bin/bash

# Download Duravit images from metadata JSON
# Filter by category, download packshot + lifestyle samples

BASE_DIR="/root/.openclaw/workspace/research/bathroom-products/raw-images"
METADATA="/root/.openclaw/workspace/research/bathroom-products/metadata/duravit-image-urls.json"

# Parse JSON and download images by category
# For now, manually select a few examples

# Premium tier - Vanity (already have metadata)
echo "Downloading Duravit vanity (premium)..."

cd "$BASE_DIR/vanity/premium" || exit 1

# Sample vanity images
wget -q "https://wgassets.duravit.cloud/photomanager-duravit/file/8a8a818d4c0f9750014c434cdcc840d4/me_by_starck_furniture_washbasins_06.jpg" -O "duravit-me-by-starck-vanity-lifestyle.jpg" || true
wget -q "https://wgassets.duravit.cloud/photomanager-duravit/file/8a8a818d4588ede6014593a1b55a6054/d-code_wt_00.jpg" -O "duravit-dcode-vanity-packshot.jpg" || true

# Showers
cd "$BASE_DIR/showers/premium" || exit 1
wget -q "https://wgassets.duravit.cloud/photomanager-duravit/file/8a8a818d5ab28eeb015abf6b5e083a5e/veroair_tm_235060_01_1131_.jpg" -O "duravit-veroair-shower-packshot.jpg" || true

# Tiles
cd "$BASE_DIR/tile/premium" || exit 1
wget -q "https://wgassets.duravit.cloud/photomanager-duravit/file/8a8a818d6123d241016131b9e0e15eda/category_washbowles.jpg" -O "duravit-tile-sample-packshot.jpg" || true

echo "Duravit downloads complete!"

# Count total
echo ""
echo "Current image count:"
find "$BASE_DIR" -name "*.jpg" -o -name "*.png" | wc -l
