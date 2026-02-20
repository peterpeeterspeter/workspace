#!/bin/bash

# Before/After Slideshow for Photostudio
# Sequence: BEFORE (3s) → 5 AFTER images (2.5s each) = 15.5 seconds total

cd /root/.openclaw/workspace/projects/photostudio/tiktok-videos

WIDTH=1080
HEIGHT=1920

echo "🎬 Creating Before/After transformation video..."
echo ""

# Create the video
ffmpeg -y \
    -loop 1 -t 3.0 -i before-raw.jpg \
    -loop 1 -t 2.5 -i img1-white.jpg \
    -loop 1 -t 2.5 -i img2-blue.jpg \
    -loop 1 -t 2.5 -i img3-beige.jpg \
    -loop 1 -t 2.5 -i img4-dark.jpg \
    -loop 1 -t 2.5 -i img5-pink.jpg \
    -filter_complex "[0:v]scale=${WIDTH}:${HEIGHT}:force_original_aspect_ratio=increase,crop=${WIDTH}:${HEIGHT},setsar=1,fps=30,format=yuv420p[v0];[1:v]scale=${WIDTH}:${HEIGHT}:force_original_aspect_ratio=increase,crop=${WIDTH}:${HEIGHT},setsar=1,fps=30,format=yuv420p[v1];[2:v]scale=${WIDTH}:${HEIGHT}:force_original_aspect_ratio=increase,crop=${WIDTH}:${HEIGHT},setsar=1,fps=30,format=yuv420p[v2];[3:v]scale=${WIDTH}:${HEIGHT}:force_original_aspect_ratio=increase,crop=${WIDTH}:${HEIGHT},setsar=1,fps=30,format=yuv420p[v3];[4:v]scale=${WIDTH}:${HEIGHT}:force_original_aspect_ratio=increase,crop=${WIDTH}:${HEIGHT},setsar=1,fps=30,format=yuv420p[v4];[5:v]scale=${WIDTH}:${HEIGHT}:force_original_aspect_ratio=increase,crop=${WIDTH}:${HEIGHT},setsar=1,fps=30,format=yuv420p[v5];[v0][v1]xfade=transition=fade:duration=0.5:offset=2.5[x1];[x1][v2]xfade=transition=fade:duration=0.5:offset=4.5[x2];[x2][v3]xfade=transition=fade:duration=0.5:offset=6.5[x3];[x3][v4]xfade=transition=fade:duration=0.5:offset=8.5[x4];[x4][v5]xfade=transition=fade:duration=0.5:offset=10.5[out]" \
    -map "[out]" -t 15.5 -pix_fmt yuv420p photostudio-before-after.mp4

if [ -f "photostudio-before-after.mp4" ]; then
    SIZE=$(du -h "photostudio-before-after.mp4" | cut -f1)
    echo "✅ Created: photostudio-before-after.mp4 ($SIZE)"
    echo ""
    echo "📊 Video specs:"
    ffprobe -v error -show_entries format=duration,size -show_entries stream=width,height -of default=noprint_wrappers=1 photostudio-before-after.mp4 2>/dev/null | head -4
else
    echo "❌ Failed to create video"
fi
