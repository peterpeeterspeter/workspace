#!/bin/bash

cd /root/.openclaw/workspace/research/bathroom-products/raw-images

converted=0
total_jpg=$(find . -name "*.jpg" -type f | wc -l)
echo "Converting $total_jpg remaining JPG files to WebP..."
echo ""

find . -name "*.jpg" -type f | while read jpg; do
    webp="${jpg%.jpg}.webp"
    [ -f "$webp" ] && continue
    
    if cwebp -q 85 "$jpg" -o "$webp" 2>/dev/null; then
        converted=$((converted + 1))
        if [ $((converted % 25)) -eq 0 ]; then
            echo "[$converted/$total_jpg] $(basename "$jpg")"
        fi
    fi
done

echo ""
echo "✅ Conversion complete!"
echo "   Total WebP: $(find . -name "*.webp" | wc -l)"
echo "   Remaining JPG: $(find . -name "*.jpg" | wc -l)"
