#!/bin/bash
#
# Content Creation - Create ready-to-use content assets
# Tuesdays - TikTok scripts, blog posts, social media content
#

set -e

DATE=$1
OUTPUT_DIR=$2
OUTPUT_FILE="$OUTPUT_DIR/content-creation-$DATE.md"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log "✍️  CONTENT CREATION - $DATE"

# Content calendar for rotation
WEEK_NUMBER=$(date +%U)
CONTENT_TYPES=(
    "photostudio-tiktok"
    "debadkamer-blog"
    "hobbysalon-social"
    "domain-research"
)

# Rotate based on week number
CONTENT_TYPE="${CONTENT_TYPES[$((WEEK_NUMBER % 4))]}"

log "  📝 Content type: $CONTENT_TYPE"

case "$CONTENT_TYPE" in
    photostudio-tiktok)
        log "    📸 Creating Photostudio TikTok content..."
        /root/.openclaw/workspace/scripts/surprises/content/photostudio-tiktok.sh "$DATE" "$OUTPUT_DIR"
        ;;
    debadkamer-blog)
        log "    🚽 Creating DeBadkamer blog post..."
        /root/.openclaw/workspace/scripts/surprises/content/debadkamer-blog.sh "$DATE" "$OUTPUT_DIR"
        ;;
    hobbysalon-social)
        log "    🎨 Creating Hobbysalon social content..."
        /root/.openclaw/workspace/scripts/surprises/content/hobbysalon-social.sh "$DATE" "$OUTPUT_DIR"
        ;;
    domain-research)
        log "    🔗 Creating domain research brief..."
        /root/.openclaw/workspace/scripts/surprises/content/domain-research.sh "$DATE" "$OUTPUT_DIR"
        ;;
esac

log "✅ Content creation completed"

echo "$OUTPUT_FILE"
