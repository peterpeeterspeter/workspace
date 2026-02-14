#!/bin/bash

# 🎯 Vision Post Analysis (Cacheable)
# Vision analyzes single post, returns structured metadata
# Usage: vision-analyze-post.sh <post_id> <site>

set -e

POST_ID=$1
SITE=$2
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CACHE_DIR="${SCRIPT_DIR}/../cache/post-metadata"
RESEARCH_DIR="${SCRIPT_DIR}/../research/${SITE}"
VISION_AGENT="agent:seo:main"

# Get post content via WordPress API
source "${SCRIPT_DIR}/get-site-creds.sh"

CREDS=$(get_site_creds "$SITE")
read -r SITE_URL USERNAME PASSWORD <<< "$CREDS"

# Fetch post data
POST_DATA=$(curl -s -L "${SITE_URL}/wp/v2/posts/${POST_ID}" -u "${USERNAME}:${PASSWORD}")

# Validate
if [ -z "$POST_DATA" ] || [ "$(echo "$POST_DATA" | jq 'empty' 2>/dev/null)" != "" ]; then
  echo "ERROR: Invalid post data for $POST_ID" >&2
  exit 1
fi

TITLE=$(echo "$POST_DATA" | jq -r '.title.rendered // ""' | sed 's/<[^>]*>//g' | sed 's/&amp;/\&/g')
CONTENT=$(echo "$POST_DATA" | jq -r '.content.rendered // ""' | sed 's/<[^>]*>//g' | sed 's/&nbsp;/ /g' | tr -s ' ')
EXCERPT=$(echo "$CONTENT" | head -c 500)

# Check if research cache exists
RESEARCH_EXISTS=0
if [ -f "${RESEARCH_DIR}/keyword-clusters.md" ]; then
  RESEARCH_EXISTS=1
fi

# Build Vision prompt
if [ $RESEARCH_EXISTS -eq 1 ]; then
  MODE="CACHE_HIT"
  CONTEXT=$(cat "${RESEARCH_DIR}/keyword-clusters.md")
else
  MODE="CACHE_MISS"
  CONTEXT="No cached research available. Perform fresh analysis."
fi

VISION_PROMPT=$(cat <<EOF
@Vision

POST ANALYSIS REQUEST - Mode: $MODE

## Post Details
- Site: $SITE
- Post ID: $POST_ID
- Title: $TITLE

## Content Excerpt
$EXCERPT

## Research Context
$CONTEXT

## Task: Generate SEO Metadata (DEEP MODE)

Provide this JSON output only:

{
  "keywords": {
    "primary": "main keyword phrase",
    "secondary": ["keyword1", "keyword2"],
    "lsi": ["related1", "related2"]
  },
  "meta": {
    "title": "Optimized title (50-60 chars)",
    "description": "Meta description (155-160 chars, includes primary keyword)"
  },
  "suggestions": {
    "content_gaps": ["missing topic 1", "missing topic 2"],
    "internal_links": ["suggested post 1", "suggested post 2"],
    "serp_features": ["images", "faq", "video"]
  },
  "confidence": "high|medium|low",
  "sources": ["source1", "source2"]
}

## Optimization Rules

Title:
- 50-60 characters
- Include primary keyword near start
- Use power words (Ultimate, Complete, Best, Guide)
- Remove filler words

Description:
- 155-160 characters
- Include primary keyword naturally
- Promise value/benefit
- Include CTA if appropriate

Keywords:
- Primary: main search term this post targets
- Secondary: variations and related terms
- LSI: latent semantic indexing terms (contextual)

## Research Sources
- web_search: keyword volume/difficulty
- web_fetch: competitor SERP analysis
- Cache: keyword-clusters.md if available

Return ONLY the JSON. No explanation.
EOF
)

# Send to Vision and capture response
RESPONSE=$(sessions_send \
  --session "$VISION_AGENT" \
  --message "$VISION_PROMPT" \
  --timeout-seconds 120)

# Extract JSON from response
echo "$RESPONSE" | grep -A 100 '{' | head -n -1
