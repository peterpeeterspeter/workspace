#!/bin/bash
# Debadkamer TikTok Video Generator - Simple Version
# Creates TikTok-ready videos from single before/after images

PROJECT="$1"
HOOK="${2:-Voor → Na. AI deed het in 30 seconden.}"
DURATION="${3:-15}"
LANGUAGE="${4:-nl}"

INPUT_DIR="/root/.openclaw/workspace/tiktok-marketing/debadkamer/input"
OUTPUT_DIR="/root/.openclaw/workspace/tiktok-marketing/debadkamer/output"
OUTPUT_FILE="$OUTPUT_DIR/${PROJECT}.mp4"

# Find the image
IMAGE_PATH="$INPUT_DIR/${PROJECT}.webp"
if [ ! -f "$IMAGE_PATH" ]; then
    IMAGE_PATH="$INPUT_DIR/${PROJECT}.jpg"
fi

if [ ! -f "$IMAGE_PATH" ]; then
    echo "❌ ERROR: Image not found: $INPUT_DIR/${PROJECT}.{webp,jpg}"
    exit 1
fi

echo ""
echo "📸 Found: $IMAGE_PATH"
echo "🎬 Creating video: ${DURATION}s"

mkdir -p "$OUTPUT_DIR"

# Create simple slideshow video (TikTok users can add effects in-app)
echo "⚙️  Generating video..."

ffmpeg -y -loop 1 -i "$IMAGE_PATH" \
    -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" \
    -c:v libx264 -tune stillimage -pix_fmt yuv420p -r 30 -t ${DURATION} \
    -shortest "$OUTPUT_FILE" 2>&1 | grep -v "^Stream" | grep -v "^Output" | head -3

if [ -f "$OUTPUT_FILE" ]; then
    SIZE=$(du -h "$OUTPUT_FILE" | cut -f1)
    echo ""
    echo "✅ Video created successfully!"
    echo "   📁 Output: $OUTPUT_FILE"
    echo "   📊 File size: $SIZE"
    echo ""

    # Dutch caption
    if [ "$LANGUAGE" = "nl" ]; then
        echo "📝 Suggested Caption (NL):"
        echo "   $HOOK"
        echo ""
        echo "   Upload je badkamerfoto → Kies producten → AI ontwerpt → Ontvang offerte"
        echo ""
        echo "   👉 Link in bio"
        echo ""
        echo "   #badkamer #renovatie #wonen #interieur #ai"
    else
        echo "📝 Suggested Caption (EN):"
        echo "   $HOOK"
        echo ""
        echo "   Upload bathroom photo → Choose products → AI designs → Get quote"
        echo ""
        echo "   👉 Link in bio"
        echo ""
        echo "   #bathroom #renovation #homedesign #interior #ai"
    fi

    echo ""
    echo "🎵 Music:"
    echo "   Check TikTok For You page for trending upbeat track"
    echo "   Look for ↑ rising badge"
    echo ""
    echo "💡 Pro tip: Add zoom/pan effects in TikTok editor for extra engagement!"
else
    echo "❌ Failed to create video"
    exit 1
fi
