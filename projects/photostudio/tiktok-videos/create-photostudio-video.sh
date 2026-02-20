#!/bin/bash

# Photostudio.io TikTok Video Generator
# Creates slideshow videos from background variations

OUTPUT_DIR="/root/.openclaw/workspace/projects/photostudio/tiktok-videos"
cd "$OUTPUT_DIR"

# Video settings
DURATION=3  # 3 seconds per image
FPS=30
ASPECT="9:16"
WIDTH=1080
HEIGHT=1920

# Input images (in order)
IMAGES=(
    "img1-white.jpg"
    "img2-blue.jpg"
    "img3-beige.jpg"
    "img4-dark.jpg"
    "img5-pink.jpg"
)

# Create video for each caption variant
create_video() {
    local CAPTION="$1"
    local VARIANT="$2"
    local OUTPUT="photostudio-${VARIANT}.mp4"

    echo "Creating $OUTPUT..."

    # Build ffmpeg filter chain for slideshow
    FILTER_COMPLEX=""

    for i in "${!IMAGES[@]}"; do
        IMG="${IMAGES[$i]}"
        IDX=$((i))

        # Scale and pad to 9:16 (1080x1920)
        FILTER_COMPLEX="[${IDX}:v]scale=${WIDTH}:${HEIGHT}:force_original_aspect_ratio=decrease,pad=${WIDTH}:${HEIGHT}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=${FPS},format=yuv420p[vid${IDX}];"

        if [[ $i -eq 0 ]]; then
            # First image - no fade in
            FILTER_COMPLEX="${FILTER_COMPLEX}[vid${IDX}]trim=0:${DURATION},setpts=PTS-STARTPTS[part${IDX}];"
        else
            # Subsequent images - fade transition
            FILTER_COMPLEX="${FILTER_COMPLEX}[vid${IDX}]trim=0:${DURATION},setpts=PTS-STARTPTS[part${IDX}];"
        fi
    done

    # Concat all parts
    FILTER_COMPLEX="${FILTER_COMPLEX}"
    for i in "${!IMAGES[@]}"; do
        if [[ $i -eq $((${#IMAGES[@]} - 1)) ]]; then
            FILTER_COMPLEX="${FILTER_COMPLEX}[part${i}]concat=n=${#IMAGES[@]}:v=1:a=0[out]"
        else
            FILTER_COMPLEX="${FILTER_COMPLEX}[part${i}]"
        fi
    done

    # Simple fade transitions between images
    FADE_FILTER=""
    for i in "${!IMAGES[@]}"; do
        if [[ $i -eq 0 ]]; then
            continue
        fi
        PREV=$((i - 1))
        FADE_FILTER="[${PREV}][${i}]xfade=transition=fade:duration=0.5:offset=$(echo "$PREV * $DURATION - 0.5" | bc)[v${i}];"
    done

    # Build final command
    FILTER=""

    for i in "${!IMAGES[@]}"; do
        FILTER="-loop 1 -t ${DURATION} -i ${IMAGES[$i]} "
    done

    # Use xfade for smooth transitions
    INPUT_COUNT=${#IMAGES[@]}
    FILTER_COMPLEX=""

    for i in $(seq 0 $((INPUT_COUNT - 1))); do
        FILTER_COMPLEX="${FILTER_COMPLEX}[${i}:v]scale=${WIDTH}:${HEIGHT}:force_original_aspect_ratio=increase,crop=${WIDTH}:${HEIGHT},setsar=1[f${i}];"
    done

    # Create fade transitions
    for i in $(seq 1 $((INPUT_COUNT - 1))); do
        PREV=$((i - 1))
        FILTER_COMPLEX="${FILTER_COMPLEX}[f${PREV}][f${i}]xfade=transition=fade:duration=0.5:offset=$(echo "$PREV * $DURATION - 0.5" | bc)[v${i}];"
    done

    FILTER_COMPLEX="${FILTER_COMPLEX}[v$((INPUT_COUNT - 1))]"

    # Calculate total duration
    TOTAL_DURATION=$((DURATION * INPUT_COUNT))

    # Build ffmpeg command
    CMD="ffmpeg -y"

    for i in $(seq 0 $((INPUT_COUNT - 1))); do
        CMD="$CMD -loop 1 -t $DURATION -i ${IMAGES[$i]}"
    done

    CMD="$CMD -filter_complex \"${FILTER_COMPLEX}\" -map \"[v$((INPUT_COUNT - 1))]\" -t ${TOTAL_DURATION} -pix_fmt yuv420p \"$OUTPUT\""

    # Execute
    eval $CMD

    if [ -f "$OUTPUT" ]; then
        SIZE=$(du -h "$OUTPUT" | cut -f1)
        echo "✅ Created: $OUTPUT ($SIZE)"
    else
        echo "❌ Failed to create $OUTPUT"
    fi

    echo ""
}

# Create video variants with different captions
echo "🎬 Creating Photostudio TikTok videos..."
echo ""

# Variant 1: Transformation focus
create_video "Watch me transform one product photo into 5 backgrounds in seconds" "transformation"

# Variant 2: Money savings
create_video "This one mistake is costing brands $10K/year on photoshoots" "money"

# Variant 3: Time savings
create_video "How I create 5 product variations in 15 seconds" "time"

# Variant 4: Bold statement
create_video "Everything you know about product photography is about to change" "bold"

# Variant 5: Question hook
create_video "Ever wonder why some brands photos look so expensive?" "question"

echo "✅ All videos created!"
echo ""
echo "📁 Location: $OUTPUT_DIR"
echo ""
ls -lh photostudio-*.mp4 | awk '{print $9, $5}'
