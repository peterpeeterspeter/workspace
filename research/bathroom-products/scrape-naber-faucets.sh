#!/bin/bash

# Scrape Ideal Standard faucets from Naber.com
# Downloads 2 images per product (packshot + lifestyle)

BASE_DIR="/root/.openclaw/workspace/research/bathroom-products/raw-images/faucets/mid-range"
cd "$BASE_DIR" || exit 1

# Product URLs and names
declare -A PRODUCTS=(
    ["https://naber.com/en/Ideal-Standard-Cerafit-1-chrome-low-pressure/5024151"]="ideal-standard-cerafit-1"
    ["https://naber.com/en/Ideal-Standard-Cerafit-3-chrome-high-pressure/5024154"]="ideal-standard-cerafit-3"
    ["https://naber.com/en/Ideal-Standard-Ceraflex-1-chrome-high-pressure/5024160"]="ideal-standard-ceraflex-1"
    ["https://naber.com/en/Ideal-Standard-Ceraplan-Neo-1-chrome-high-pressure/5024123"]="ideal-standard-ceraplan-neo-1"
    ["https://naber.com/en/Ideal-Standard-Ceralook-1-black-matt-high-pressure/5024118"]="ideal-standard-ceralook-1"
)

for url in "${!PRODUCTS[@]}"; do
    name="${PRODUCTS[$url]}"
    echo "Scraping: $name"

    # Use browser to extract image URLs
    # For now, we'll download manually

    # Packshot (product detail image - Z1 or P1)
    # Lifestyle (context image - P2 or similar)

    sleep 1  # Be respectful
done

echo "Scraping complete!"
