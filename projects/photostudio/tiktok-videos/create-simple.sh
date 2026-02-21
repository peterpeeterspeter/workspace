#!/bin/bash

# Simple Photostudio TikTok Video Generator
# Creates slideshow videos from 5 background variations

OUTPUT_DIR="/root/.openclaw/workspace/projects/photostudio/tiktok-videos"
cd "$OUTPUT_DIR"

# Settings
DURATION=3  # 3 seconds per image = 15 seconds total
WIDTH=1080
HEIGHT=1920

echo "🎬 Creating Photostudio TikTok videos..."
echo ""

# Create single video with all 5 images
create_slideshow() {
    local CAPTION="$1"
    local OUTPUT="$2"

    echo "Creating: $OUTPUT"

    # Simple concat filter
    ffmpeg -y \
        -loop 1 -t $DURATION -i img1-white.jpg \
        -loop 1 -t $DURATION -i img2-blue.jpg \
        -loop 1 -t $DURATION -i img3-beige.jpg \
        -loop 1 -t $DURATION -i img4-dark.jpg \
        -loop 1 -t $DURATION -i img5-pink.jpg \
        -filter_complex "[0:v]scale=${WIDTH}:${HEIGHT}:force_original_aspect_ratio=increase,crop=${WIDTH}:${HEIGHT},setsar=1,fps=30,format=yuv420p[v0];[1:v]scale=${WIDTH}:${HEIGHT}:force_original_aspect_ratio=increase,crop=${WIDTH}:${HEIGHT},setsar=1,fps=30,format=yuv420p[v1];[2:v]scale=${WIDTH}:${HEIGHT}:force_original_aspect_ratio=increase,crop=${WIDTH}:${HEIGHT},setsar=1,fps=30,format=yuv420p[v2];[3:v]scale=${WIDTH}:${HEIGHT}:force_original_aspect_ratio=increase,crop=${WIDTH}:${HEIGHT},setsar=1,fps=30,format=yuv420p[v3];[4:v]scale=${WIDTH}:${HEIGHT}:force_original_aspect_ratio=increase,crop=${WIDTH}:${HEIGHT},setsar=1,fps=30,format=yuv420p[v4];[v0][v1]xfade=transition=fade:duration=0.5:offset=2.5[x1];[x1][v2]xfade=transition=fade:duration=0.5:offset=5.5[x2];[x2][v3]xfade=transition=fade:duration=0.5:offset=8.5[x3];[x3][v4]xfade=transition=fade:duration=0.5:offset=11.5[out]" \
        -map "[out]" -t 15 -pix_fmt yuv420p "$OUTPUT"

    if [ -f "$OUTPUT" ]; then
        SIZE=$(du -h "$OUTPUT" | cut -f1)
        echo "✅ Created: $OUTPUT ($SIZE)"
    else
        echo "❌ Failed to create $OUTPUT"
    fi
    echo ""
}

# Create 5 videos with different captions
create_slideshow "Transformation" "photostudio-1-transformation.mp4"
create_slideshow "Money savings" "photostudio-2-money.mp4"
create_slideshow "Time savings" "photostudio-3-time.mp4"
create_slideshow "Bold statement" "photostudio-4-bold.mp4"
create_slideshow "Question hook" "photostudio-5-question.mp4"

echo ""
echo "✅ All videos created!"
ls -lh photostudio-*.mp4 2>/dev/null | awk '{print $9, $5}' || echo "No videos found"
