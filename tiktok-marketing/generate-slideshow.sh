#!/bin/bash
# Photostudio.io TikTok Slideshow Generator
# Creates 9:16 TikTok slideshows from before/after images

PROJECT="$1"
HOOK="${2:-We replaced our \$5,000/month photographer with AI. Here's what happened.}"
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
echo "📸 Found $TOTAL_IMAGES images:"
echo "   ✓ before.jpg"
for i in "${!AFTER_IMAGES[@]}"; do
    echo "   ✓ after-$((i+1)).jpg"
done

echo ""
echo "🎬 Creating slideshow:"
echo "   Total duration: ${DURATION}s"
echo "   Per image: ${PER_IMAGE}s (last: ${LAST_IMAGE}s)"
echo "   Resolution: 1080x1920 (9:16)"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Build ffmpeg command
FFMPEG_CMD="ffmpeg -y"

# Add before image
FFMPEG_CMD="$FFMPEG_CMD -loop 1 -t $PER_IMAGE -i \"$BEFORE\""

# Add after images
INDEX=0
for img in "${AFTER_IMAGES[@]}"; do
    INDEX=$((INDEX + 1))
    if [ $INDEX -eq ${#AFTER_IMAGES[@]} ]; then
        FFMPEG_CMD="$FFMPEG_CMD -loop 1 -t $LAST_IMAGE -i \"$img\""
    else
        FFMPEG_CMD="$FFMPEG_CMD -loop 1 -t $PER_IMAGE -i \"$img\""
    fi
done

# Build filter complex
FILTER_COMPLEX=""
for i in $(seq 0 $((TOTAL_IMAGES - 1))); do
    FILTER_COMPLEX="${FILTER_COMPLETE}[${i}:v]scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2[v${i}];"
done

# Build concat part
CONCAT_PARTS=""
for i in $(seq 0 $((TOTAL_IMAGES - 1))); do
    CONCAT_PARTS="${CONCAT_PARTS}[v${i}]"
done
FILTER_COMPLEX="${FILTER_COMPLEX}${CONCAT_PARTS}concat=n=${TOTAL_IMAGES}:v=1:a=0[outv]"

FFMPEG_CMD="$FFMPEG_CMD -filter_complex \"$FILTER_COMPLEX\" -map \"[outv]\" \"$OUTPUT_FILE\""

echo ""
echo "⚙️  Executing ffmpeg..."
eval $FFMPEG_CMD 2>&1 | grep -v "Stream #" | grep -v "Press \[q\]" | grep -v "frame=" | grep -v "^$"

if [ -f "$OUTPUT_FILE" ]; then
    SIZE=$(du -h "$OUTPUT_FILE" | cut -f1)
    echo ""
    echo "✅ Slideshow created successfully!"
    echo "   📁 Output: $OUTPUT_FILE"
    echo "   📊 File size: $SIZE"
    echo ""
    echo "📝 Suggested Caption:"
    echo "   $HOOK"
    echo "   "
    echo "   One photo → Ghost mannequin + flatlay + on-model + video in seconds."
    echo "   "
    echo "   Link in bio ↗️"
    echo "   "
    echo "   #fashion #ecommerce #ai #productphotography #smallbusiness"
    echo ""
    echo "🎵 Music Recommendation:"
    echo "   Open TikTok → Check For You page → Find trending upbeat track"
    echo "   Look for ↑ rising badge → Use in your video"
else
    echo ""
    echo "❌ ERROR: Failed to create slideshow"
    exit 1
fi
