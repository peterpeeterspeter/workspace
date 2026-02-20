#!/bin/bash
#
# Capture Learning - Helper script for self-improvement skill
# Usage: ./capture-learning.sh "Title" "Category" "Description"
#

set -e

TITLE=$1
CATEGORY=${2:-general}
DESCRIPTION=$3
DATE=$(date +%Y-%m-%d\ %H:%M)
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

# Files
SELF_REVIEW="/root/.openclaw/workspace/self-review.md"
MEMORY="/root/.openclaw/workspace/MEMORY.md"
DAILY_LOG="/root/.openclaw/workspace/memory/$(date +%Y-%m-%d).md"

# Create daily log if doesn't exist
touch "$DAILY_LOG"

# Add to daily log
cat >> "$DAILY_LOG" << EOF

## Learning: $TITLE

**Date:** $DATE
**Category:** $CATEGORY

**What Happened:**
$DESCRIPTION

**Tags:** #$CATEGORY #learning

EOF

# Add to self-review
cat >> "$SELF_REVIEW" << EOF

## $TITLE

**Date:** $DATE
**Category:** $CATEGORY

**Context:** [To be filled]
**Issue:** [To be filled]
**Root Cause:** [To be filled]
**Solution:** [To be filled]
**Prevention:** [To be filled]
**Impact:** [To be filled]
**Tags:** #$CATEGORY #learning

EOF

echo "✅ Learning captured: $TITLE"
echo "📁 Daily log: $DAILY_LOG"
echo "📁 Self-review: $SELF_REVIEW"
echo ""
echo "📝 Please fill in the details in:"
echo "   - $SELF_REVIEW"
