#!/bin/bash

cd /root/.openclaw/workspace/research/bathroom-products/raw-images

converted=0
failed=0

echo "Converting remaining JPG to WebP..."

for jpg in $(find . -name "*.jpg" -type f | head -100); do
    webp="${jpg%.jpg}.webp"
    
    # Skip if WebP already exists
    if [ -f "$webp" ]; then
        continue
    fi
    
    # Convert
    if cwebp -q 85 "$jpg" -o "$webp" >/dev/null 2>&1; then
        converted=$((converted + 1))
        # Only print every 5 to reduce output
        if [ $((converted % 5)) -eq 0 ]; then
            echo "Progress: $converted converted..."
        fi
    else
        failed=$((failed + 1))
    fi
done

echo ""
echo "✅ Conversion complete!"
echo "   Converted: $converted"
echo "   Failed: $failed"
echo ""
echo "Total WebP files: $(find . -name "*.webp" | wc -l)"
echo "Remaining JPG: $(find . -name "*.jpg" | wc -l)"
