#!/bin/bash

# Convert all JPG images to WebP format
cd /root/.openclaw/workspace/research/bathroom-products/raw-images

converted=0
failed=0
skipped=0

total=$(find . -name "*.jpg" | wc -l)
echo "Converting $total JPG images to WebP..."

find . -name "*.jpg" -type f | while read jpg; do
    webp="${jpg%.jpg}.webp"
    
    # Skip if WebP already exists
    if [ -f "$webp" ]; then
        skipped=$((skipped + 1))
        continue
    fi
    
    # Convert using cwebp
    if cwebp -q 85 "$jpg" -o "$webp" 2>/dev/null; then
        converted=$((converted + 1))
        echo "✓ $(basename "$jpg")"
    else
        failed=$((failed + 1))
        echo "✗ $(basename "$jpg")"
    fi
done

echo ""
echo "✅ Conversion complete!"
echo "   Converted: $converted"
echo "   Failed: $failed"
echo "   Skipped: $skipped"
echo "   Total: $((converted + failed + skipped))"
