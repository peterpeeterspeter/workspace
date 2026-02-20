#!/bin/bash
# Photostudio.io TikTok Slideshow Generator - Simplified
# Creates 9:16 TikTok slideshows from before/after images

PROJECT="$1"
HOOK="${2:-AI creates your entire product catalog in seconds.}"
DURATION="${3:-30}"

INPUT_DIR="/root/.openclaw/workspace/tiktok-marketing/slideshows/input/$PROJECT"
OUTPUT_DIR="/root/.openclaw/workspace/tiktok-marketing/slideshows/output"
OUTPUT_FILE="$OUTPUT_DIR/$PROJECT.mp4"

# Check input directory
if [ ! -d "$INPUT_DIR" ]; then
    echo "❌ ERROR: Input directory not found: $INPUT_DIR"
    exit 1
fi

# Count images
BEFORE="$INPUT_DIR/before.jpg"
if [ ! -f "$BEFORE" ]; then
    echo "❌ ERROR: before.jpg not found"
    exit 1
fi

# Find all after images
AFTER_IMAGES=()
for i in {1..10}; do
    IMG="$INPUT_DIR/after-$i.jpg"
    if [ -f "$IMG" ]; then
        AFTER_IMAGES+=("$IMG")
    fi
done

if [ ${#AFTER_IMAGES[@]} -eq 0 ]; then
    echo "❌ ERROR: No after images found"
    exit 1
fi

TOTAL_IMAGES=$((${#AFTER_IMAGES[@]} + 1))
PER_IMAGE=$((DURATION / TOTAL_IMAGES))
LAST_IMAGE=$((DURATION - (PER_IMAGE * (TOTAL_IMAGES - 1))))

echo ""
echo "📸 Found $TOTAL_IMAGES images"
echo "🎬 Creating slideshow: ${DURATION}s total"

# Create temp directory for scaled images
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

# Scale all images to 1080x1920 first
echo "⚙️  Scaling images..."
INDEX=0
ffmpeg -y -i "$BEFORE" -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" -frames:v 1 "$TEMP_DIR/slide0.jpg" 2>&1 | grep -v "^$" | head -5

for img in "${AFTER_IMAGES[@]}"; do
    INDEX=$((INDEX + 1))
    ffmpeg -y -i "$img" -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" -frames:v 1 "$TEMP_DIR/slide${INDEX}.jpg" 2>&1 | grep -v "^$" | head -5
done

# Create slideshow using simple concat
echo "🎬 Creating slideshow..."

# Build concat file
CONCAT_FILE="$TEMP_DIR/concat.txt"
for i in $(seq 0 $((TOTAL_IMAGES - 1))); do
    if [ $i -eq $((TOTAL_IMAGES - 1)) ]; then
        DUR=$LAST_IMAGE
    else
        DUR=$PER_IMAGE
    fi
    echo "file '$TEMP_DIR/slide${i}.jpg'"
    echo "duration $DUR"
done > "$CONCAT_FILE"

# Create video
ffmpeg -y -f concat -safe 0 -i "$CONCAT_FILE" -vf "fps=30" -vsync vfr "$OUTPUT_FILE" 2>&1 | grep -E "(Duration|Stream|frame=)" | head -10

if [ -f "$OUTPUT_FILE" ]; then
    SIZE=$(du -h "$OUTPUT_FILE" | cut -f1)
    echo ""
    echo "✅ Slideshow created successfully!"
    echo "   📁 Output: $OUTPUT_FILE"
    echo "   📊 File size: $SIZE"
    echo ""
    echo "📝 Suggested Caption:"
    echo "   $HOOK"
    echo ""
    echo "   One photo → Ghost mannequin + flatlay + on-model + video in seconds."
    echo ""
    echo "   Link in bio ↗️"
    echo ""
    echo "   #fashion #ecommerce #ai #productphotography #smallbusiness"
    echo ""
    echo "🎵 Music:"
    echo "   Check TikTok For You page for trending upbeat tracks"
    echo "   Look for ↑ rising badge"
else
    echo "❌ Failed to create slideshow"
    exit 1
fi
