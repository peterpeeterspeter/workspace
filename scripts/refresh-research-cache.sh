#!/bin/bash

# 🔄 Refresh Research Cache (Weekly)
# Updates research docs with deltas only
# Usage: refresh-research-cache.sh <site>

set -e

SITE=$1
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESEARCH_DIR="${SCRIPT_DIR}/../research/${SITE}"
VISION_AGENT="agent:seo:main"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}🔄 Refreshing Research Cache${NC}"
echo "Site: $SITE"
echo "Mode: DELTA (incremental updates only)"
echo "Started: $(date)"
echo ""

# Check if research exists
if [ ! -d "$RESEARCH_DIR" ]; then
  echo -e "${YELLOW}⚠️  No existing research found${NC}"
  echo "Run initial build first:"
  echo "  build-research-cache.sh $SITE"
  exit 1
fi

# Send refresh task to Vision
REFRESH_TASK=$(cat <<EOF
@Vision

WEEKLY RESEARCH REFRESH - $SITE

Mode: DELTA UPDATES ONLY (do not rebuild from scratch)

## Task: Update existing research documents

Located in: ${RESEARCH_DIR}/

## What to Update

1. **keyword-clusters.md**
   - Add new keyword clusters discovered this week
   - Update search volume estimates if changed significantly
   - Mark outdated clusters (deprecated terms)

2. **competitor-intel.md**
   - Check top 5 competitors for new content
   - Note any major content changes
   - Update if competitors changed strategy

3. **serp-features.md**
   - Test if SERP features changed
   - Add new features if detected
   - Note feature frequency changes

4. **content-gap-analysis.md**
   - Remove gaps we've filled
   - Add new gaps discovered
   - Update priority rankings

## Method: DELTA (Incremental)

- DO NOT: Re-analyze everything from scratch
- DO: Check for changes since last update
- DO: Update only what changed
- DO: Mark additions with [NEW] tag
- DO: Mark removals with [REMOVED] tag

## Quality Check

After updates, verify:
- All sources still valid (no broken URLs)
- Confidence levels still accurate
- Recommendations still relevant
- No duplicate entries

Update these files:
- ${RESEARCH_DIR}/keyword-clusters.md
- ${RESEARCH_DIR}/competitor-intel.md
- ${RESEARCH_DIR}/serp-features.md
- ${RESEARCH_DIR}/content-gap-analysis.md

Report back with:
- Number of changes made
- New keywords added
- Outdated content removed
- Updated recommendations
EOF
)

# Send to Vision
sessions_send \
  --session "$VISION_AGENT" \
  --message "$REFRESH_TASK"

echo -e "${GREEN}✅ Refresh task sent to Vision${NC}"
echo ""
echo "Vision will update research docs (5-15 min)"
echo "Check: ${RESEARCH_DIR}/"
echo ""
echo "Completed: $(date)"
