#!/bin/bash

# 🎯 SEO Optimization with Caching
# Cache-first workflow to minimize API calls
# Usage: seo-optimize-cached.sh <post_id> <site>

set -e

POST_ID=$1
SITE=$2
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CACHE_DIR="${SCRIPT_DIR}/../cache/post-metadata"
CACHE_FILE="${CACHE_DIR}/${POST_ID}.json"
VISION_SCRIPT="${SCRIPT_DIR}/vision-analyze-post.sh"
APPLY_SCRIPT="${SCRIPT_DIR}/apply-seo-enrichment.sh"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🔍 SEO Optimization (Cached)${NC}"
echo "Post: $POST_ID | Site: $SITE"
echo ""

# Step 1: Check cache
if [ -f "$CACHE_FILE" ]; then
  CACHE_AGE=$(($(date +%s) - $(stat -c %Y "$CACHE_FILE")))
  CACHE_AGE_DAYS=$((CACHE_AGE / 86400))

  echo -e "${GREEN}✅ CACHE HIT${NC}"
  echo "Age: $CACHE_AGE_DAYS days"
  echo "Using cached metadata..."
  echo ""

  METADATA=$(cat "$CACHE_FILE")
else
  echo -e "${YELLOW}⚠️  CACHE MISS${NC}"
  echo "Running Vision analysis..."
  echo ""

  # Step 2: Run Vision analysis
  METADATA=$("$VISION_SCRIPT" "$POST_ID" "$SITE")

  if [ -z "$METADATA" ]; then
    echo -e "${RED}❌ Vision analysis failed${NC}"
    exit 1
  fi

  # Validate JSON
  if [ "$(echo "$METADATA" | jq 'empty' 2>/dev/null)" != "" ]; then
    echo -e "${RED}❌ Invalid JSON from Vision${NC}"
    echo "$METADATA"
    exit 1
  fi

  # Step 3: Save to cache
  mkdir -p "$CACHE_DIR"
  echo "$METADATA" | jq '.' > "$CACHE_FILE"

  echo -e "${GREEN}✅ Analysis cached${NC}"
  echo ""
fi

# Step 4: Display metadata
echo "Metadata Preview:"
echo "$METADATA" | jq -r '
  "Primary Keyword: \(.keywords.primary)",
  "Meta Title: \(.meta.title)",
  "Meta Description: \(.meta.description)"
'
echo ""

# Step 5: Apply to WordPress
echo -e "${BLUE}📝 Applying to WordPress...${NC}"

"$APPLY_SCRIPT" "$POST_ID" "$SITE" "$METADATA"

if [ $? -eq 0 ]; then
  echo -e "${GREEN}✅ Optimization complete${NC}"
  echo ""
  echo "Next steps:"
  echo "1. Review changes in WordPress"
  echo "2. Run health check: publish-gateway.sh check $POST_ID $SITE"
  echo "3. Publish if ready: publish-gateway.sh publish $POST_ID $SITE"
else
  echo -e "${RED}❌ Failed to apply metadata${NC}"
  exit 1
fi
