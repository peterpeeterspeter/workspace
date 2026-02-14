#!/bin/bash

# Fast batch convert ALL JPG to WebP
cd /root/.openclaw/workspace/research/bathroom-products/raw-images

total_jpg=$(find . -name "*.jpg" -type f | wc -l)
echo "Converting all $total_jpg JPG files to WebP..."
echo ""

converted=0

# Convert using find -exec
find . -name "*.jpg" -type f -exec bash -c '
    jpg="$1"
    webp="${jpg%.jpg}.webp"
    if [ ! -f "$webp" ]; then
        cwebp -q 85 "$jpg" -o "$webp" 2>/dev/null && echo "✓ $(basename "$jpg")"
    fi
' {} \;

echo ""
echo "✅ Conversion complete!"
echo "   JPG files: $(find . -name "*.jpg" | wc -l)"
echo "   WebP files: $(find . -name "*.webp" | wc -l)"
