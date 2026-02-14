#!/bin/bash

# Convert ALL remaining JPG to WebP in batches
cd /root/.openclaw/workspace/research/bathroom-products/raw-images

converted=0
total_jpg=$(find . -name "*.jpg" -type f | wc -l)
echo "Converting $total_jpg remaining JPG files to WebP..."
echo ""

# Convert all JPG files
find . -name "*.jpg" -type f | while read jpg; do
    webp="${jpg%.jpg}.webp"
    
    # Skip if WebP exists
    [ -f "$webp" ] && continue
    
    # Convert with cwebp
    if cwebp -q 85 "$jpg" -o "$webp" 2>/dev/null; then
        converted=$((converted + 1))
        # Progress every 25 files
        if [ $((converted % 25)) -eq 0 ]; then
            echo "[$converted/$total_jpg] $(basename "$jpg")"
    fi
done

echo ""
echo "✅ All conversions complete!"
echo "   Total converted: $converted"
echo "   Remaining JPG: $(find . -name "*.jpg" | wc -l)"
echo "   Total WebP: $(find . -name "*.webp" | wc -l)"
echo "   Disk usage: $(du -sh . | head -1)"
