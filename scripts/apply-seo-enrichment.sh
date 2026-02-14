#!/bin/bash

# 🎯 Apply SEO Enrichment to WordPress
# Updates RankMath fields via REST API
# Usage: apply-seo-enrichment.sh <post_id> <site> <metadata_json>

set -e

POST_ID=$1
SITE=$2
METADATA=$3
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source credentials
source "${SCRIPT_DIR}/get-site-creds.sh"

CREDS=$(get_site_creds "$SITE")
read -r SITE_URL USERNAME PASSWORD <<< "$CREDS"

# Parse metadata
PRIMARY_KEYWORD=$(echo "$METADATA" | jq -r '.keywords.primary')
META_TITLE=$(echo "$METADATA" | jq -r '.meta.title')
META_DESCRIPTION=$(echo "$METADATA" | jq -r '.meta.description')

# Validate required fields
if [ -z "$PRIMARY_KEYWORD" ] || [ "$PRIMARY_KEYWORD" = "null" ]; then
  echo "ERROR: Missing primary keyword" >&2
  exit 1
fi

if [ -z "$META_DESCRIPTION" ] || [ "$META_DESCRIPTION" = "null" ]; then
  echo "ERROR: Missing meta description" >&2
  exit 1
fi

# Build update payload
# Note: RankMath uses these meta fields
UPDATE_PAYLOAD=$(jq -n \
  --arg title "$META_TITLE" \
  --arg desc "$META_DESCRIPTION" \
  --arg kw "$PRIMARY_KEYWORD" \
  '{
    title: $title,
    meta: {
      rank_math_description: $desc,
      rank_math_focus_keyword: $kw
    }
  }')

echo "Updating post $POST_ID..."
echo "  Title: $META_TITLE"
echo "  Keyword: $PRIMARY_KEYWORD"
echo "  Description: ${META_DESCRIPTION:0:80}..."
echo ""

# Update via WordPress REST API
RESULT=$(curl -s -L -X POST \
  "${SITE_URL}/wp/v2/posts/${POST_ID}" \
  -u "${USERNAME}:${PASSWORD}" \
  -H "Content-Type: application/json" \
  -d "$UPDATE_PAYLOAD")

# Validate response
if [ -z "$RESULT" ] || [ "$(echo "$RESULT" | jq 'empty' 2>/dev/null)" != "" ]; then
  echo "ERROR: Invalid response from WordPress API" >&2
  echo "$RESULT" >&2
  exit 1
fi

# Check for errors
if [ "$(echo "$RESULT" | jq -r '.code // empty')" != "" ]; then
  echo "ERROR: WordPress API returned error" >&2
  echo "$RESULT" | jq -r '.' >&2
  exit 1
fi

NEW_TITLE=$(echo "$RESULT" | jq -r '.title.rendered // ""' | sed 's/<[^>]*>//g')
NEW_DESC=$(echo "$RESULT" | jq -r '.meta.rank_math_description // ""')

echo "✅ Updated successfully"
echo "  New title: $NEW_TITLE"
echo "  New description: ${NEW_DESC:0:80}..."
