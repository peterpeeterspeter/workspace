#!/bin/bash
#
# Midnight Surprise - Daily autonomous value creation for Peter
# Runs every night at 2 AM CET
# Creates surprise + value across his portfolio
#
# File: /root/.openclaw/workspace/scripts/midnight-surprise.sh
#

set -e

# Configuration
WORKSPACE="/root/.openclaw/workspace"
OUTPUT_DIR="$WORKSPACE/midnight-surprises"
LOG_DIR="$OUTPUT_DIR/logs"
DATE=$(date +%Y-%m-%d)
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
LOG_FILE="$LOG_DIR/midnight-surprise-$DATE.log"

# Create directories
mkdir -p "$OUTPUT_DIR"
mkdir -p "$LOG_DIR"

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "🌙 MIDNIGHT SURPRISE STARTED"

# Day of week (0=Sunday, 6=Saturday)
DAY_OF_WEEK=$(date +%u)
WEEK_NUMBER=$(date +%U)

# Pick a surprise type based on day rotation
# We'll cycle through different value categories
SURPRISE_TYPES=(
    "competitive-intelligence"    # Mon: Spy on competitors
    "content-creation"             # Tue: Create content assets
    "technical-discovery"          # Wed: Find technical opportunities
    "business-intelligence"        # Thu: Analytics & insights
    "playbook-creation"            # Fri: Document & systematize
    "trend-research"               # Sat: Find emerging trends
    "portfolio-review"             # Sun: Review & optimize portfolio
)

# Select based on day of week (1-7)
SURPRISE_TYPE="${SURPRISE_TYPES[$((DAY_OF_WEEK - 1))]}"

log "📅 Selected surprise type: $SURPRISE_TYPE"

# Execute the surprise
case "$SURPRISE_TYPE" in
    competitive-intelligence)
        log "🔍 Running competitive intelligence..."
        /root/.openclaw/workspace/scripts/surprises/competitive-intelligence.sh "$DATE" "$OUTPUT_DIR"
        ;;
    content-creation)
        log "✍️  Running content creation..."
        /root/.openclaw/workspace/scripts/surprises/content-creation.sh "$DATE" "$OUTPUT_DIR"
        ;;
    technical-discovery)
        log "🔧 Running technical discovery..."
        /root/.openclaw/workspace/scripts/surprises/technical-discovery.sh "$DATE" "$OUTPUT_DIR"
        ;;
    business-intelligence)
        log "📊 Running business intelligence..."
        /root/.openclaw/workspace/scripts/surprises/business-intelligence.sh "$DATE" "$OUTPUT_DIR"
        ;;
    playbook-creation)
        log "📖 Running playbook creation..."
        /root/.openclaw/workspace/scripts/surprises/playbook-creation.sh "$DATE" "$OUTPUT_DIR"
        ;;
    trend-research)
        log "🔥 Running trend research..."
        /root/.openclaw/workspace/scripts/surprises/trend-research.sh "$DATE" "$OUTPUT_DIR"
        ;;
    portfolio-review)
        log "💼 Running portfolio review..."
        /root/.openclaw/workspace/scripts/surprises/portfolio-review.sh "$DATE" "$OUTPUT_DIR"
        ;;
esac

log "✅ MIDNIGHT SURPRISE COMPLETED"
log "📦 Output directory: $OUTPUT_DIR"

# Return success
exit 0
