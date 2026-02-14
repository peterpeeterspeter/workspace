#!/bin/bash

# 🎯 Build Master Research Cache for Site
# One-time analysis, reusable across all posts
# Usage: build-research-cache.sh <site>

set -e

SITE=$1
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESEARCH_DIR="${SCRIPT_DIR}/../research/${SITE}"
VISON_AGENT="agent:seo:main"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}🔍 Building Master Research Cache${NC}"
echo "Site: $SITE"
echo "Mode: DEEP"
echo ""

# Create research directory
mkdir -p "$RESEARCH_DIR"

# Step 1: Analyze Top Posts (Vision)
echo -e "${YELLOW}[1/4] Analyzing top 20 posts...${NC}"

VISION_ANALYSIS=$(cat <<EOF
@Vision

DEEP MODE RESEARCH TASK for $SITE

Analyze the top 20 published posts on $SITE and create comprehensive research documentation.

For each post:
1. Extract primary keywords
2. Identify keyword clusters
3. Map content types (guides, reviews, lists)
4. Note SERP features (images, videos, FAQs)
5. Identify search intent

Create 4 master research documents:

## 1. keyword-clusters.md
- Group related keywords by topic
- Note search volume estimates
- Map to content type (guide/review/list)
- Identify content gaps (missing topics)

## 2. competitor-intel.md
- Top 5 competitors in this niche
- Their top-performing content
- Content formats they use
- Topics we can outrank

## 3. serp-features.md
- Common SERP features (images, videos, FAQs, People Also Ask)
- How often each appears
- What content triggers them
- Optimization opportunities

## 4. content-gap-analysis.md
- Topics competitors cover that we don't
- Questions people ask that we don't answer
- Content formats we're missing
- Priority topics to create

Research methodology:
- Use web_search for keyword discovery
- Use web_fetch to analyze competitor content
- Track all sources
- Provide confidence levels (high/medium/low)

Write each document to: ${RESEARCH_DIR}/

Quality standards:
- Data-driven (all claims have sources)
- Specific (not "good content" but "list-based guides with 15+ items")
- Actionable (clear "what to create next" recommendations)
- Comprehensive (cover major topics, not edge cases)

DEEP MODE: Take your time. This is one-time cost for permanent reuse.

Report back when complete with:
- Number of posts analyzed
- Keyword clusters found
- Competitors identified
- SERP features mapped
- Content gaps found
EOF
)

# Send to Vision agent
# sessions_send removed - using direct analysis \
  --session "$VISION_AGENT" \
  --message "$VISION_ANALYSIS"

echo -e "${GREEN}✅ Vision analysis started${NC}"
echo "Check: ${RESEARCH_DIR}/"
echo ""
echo "Next steps:"
echo "1. Vision will create research docs (5-10 min)"
echo "2. Run: seo-optimize-cached.sh <post_id> $SITE"
echo "3. Cache will auto-build from research docs"

# Fallback direct analyzer
analyze_post_direct() {
  local post_id=$1
  local site=$2

  ~/.openclaw/workspace/scripts/publish-gateway.sh check "$post_id" "$site" \
    > "/root/.openclaw/workspace/cache/post-metadata/${post_id}.json"
}
