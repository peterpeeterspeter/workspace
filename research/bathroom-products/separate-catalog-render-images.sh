#!/bin/bash

# Separate catalog images from render images
# Catalog: Lifestyle shots for UI (product-images-catalog/)
# Render: Product shots for AI (product-images-render/)

cd /root/.openclaw/workspace/research/bathroom-products/raw-images

echo "Separating catalog vs render images..."
echo ""

catalog_dir="product-images-catalog"
render_dir="product-images-render"
mkdir -p "$render_dir"

separated=0
skipped=0

# Find render-optimized images (clean, white background)
# Criteria: solid/light background, centered product, neutral colors
find . -name "*.jpg" -o -name "*.webp" -type f | while read img; do
    fname=$(basename "$img")
    
    # Skip if already has "catalog" or "render" in path
    [[ "$fname" == *"catalog"* ]] && continue
    [[ "$fname" == *"render"* ]] && continue
    
    # Use heuristics to detect render images (simplified)
    # Render images: cleaner, product-focused
    if [[ "$fname" == *"grohe"* ]] || \
       [[ "$fname" == *"duravit-starck"* ]] || \
       [[ "$fname" == *"architec"* ]] || \
       [[ "$fname" == *"happy"* ]]; then
        # This is likely a render image
        target_dir="$render_dir"
        prefix="render"
    else
        # This is a catalog image
        target_dir="$catalog_dir"
        prefix="catalog"
    
    # Ensure target directory exists
    mkdir -p "$target_dir"
    
    # Get category from path
    category=$(echo "$img" | cut -d'/' -f1 | cut -d'/' -f1)
    
    # Move file
    mv "$img" "$target_dir/${category}-${prefix}-$(basename "$fname")"
    separated=$((separated + 1))
    
    # Progress every 25
    if [ $((separated % 25)) -eq 0 ]; then
        echo "[$separated] $(basename "$img")"
    fi
done

echo ""
echo "✅ Separation complete!"
echo "   Separated: $separated files"
echo "   Catalog images: $(find product-images-catalog -name '*.jpg' -o -name '*.webp' | wc -l)"
echo "   Render images: $(find product-images-render -name '*.jpg' -o -name '*.webp' | wc -l)"
echo ""
echo "Next: Upload these folders to Supabase Storage bucket 'product-images'"
