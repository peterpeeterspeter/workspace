#!/bin/bash
# Pinch-to-Post Helper: Cross-Site Publishing
# Publish same article to multiple sites

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="/root/.openclaw/workspace"

# Load credentials
source "$WORKSPACE/.env" 2>/dev/null || true

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

usage() {
  echo "Usage: $0 <title> <content_file> <sites>"
  echo ""
  echo "Example:"
  echo '  $0 "My Article" content.md "crashgame,freecrash,cryptocrash"'
  echo '  $0 "My Article" content.html "crashcasino"'
  exit 1
}

# Check arguments
if [[ $# -lt 3 ]]; then
  usage
fi

TITLE="$1"
CONTENT_FILE="$2"
SITES_CSV="$3"

# Check content file exists
if [[ ! -f "$CONTENT_FILE" ]]; then
  echo -e "${RED}Error: File not found: ${CONTENT_FILE}${NC}"
  exit 1
fi

# Read content
CONTENT=$(cat "$CONTENT_FILE")

# Detect content type
if [[ "$CONTENT_FILE" =~ \.md$ ]]; then
  CONTENT_TYPE="markdown"
elif [[ "$CONTENT_FILE" =~ \.html$ ]]; then
  CONTENT_TYPE="html"
else
  CONTENT_TYPE="text"
fi

# Parse sites
IFS=',' read -ra SITES <<< "$SITES_CSV"

# Validate sites
VALID_SITES=("crashcasino" "crashgame" "freecrash" "cryptocrash" "hobbysalon")
for site in "${SITES[@]}"; do
  site=$(echo "$site" | xargs)  # trim whitespace
  if [[ ! " ${VALID_SITES[@]} " =~ " ${site} " ]]; then
    echo -e "${RED}Error: Invalid site '${site}'${NC}"
    echo "Valid sites: ${VALID_SITES[*]}"
    exit 1
  fi
done

echo -e "${GREEN}=== Cross-Site Publishing ===${NC}"
echo "Title: ${TITLE}"
echo "Content: ${CONTENT_FILE} (${CONTENT_TYPE})"
echo "Sites: ${SITES[*]}"
echo ""

# Convert markdown to HTML if needed
if [[ "$CONTENT_TYPE" == "markdown" ]]; then
  # Simple markdown to HTML conversion (basic)
  HTML=$(echo "$CONTENT" | sed -e 's/^# \(.*\)$/<h1>\1<\/h1>/' \
    -e 's/^## \(.*\)$/<h2>\1<\/h2>/' \
    -e 's/^### \(.*\)$/<h3>\1<\/h3>/' \
    -e 's/\*\*\(.*\)\*\*/<strong>\1<\/strong>/g' \
    -e 's/\*\([^*]*\)\*/<em>\1<\/em>/g' \
    -e 's/^\- \(.*\)$/<li>\1<\/li>/' \
    -e 's/^> \(.*\)$/<blockquote>\1<\/blockquote>/' \
    -e 's/^$/<p>/' \
    -e 's/$/<\/>/')

  # Wrap remaining text in paragraphs
  CONTENT="$HTML"
fi

PUBLISHED=0
FAILED=0

for site in "${SITES[@]}"; do
  site=$(echo "$site" | xargs)  # trim whitespace

  echo -e "${YELLOW}[${site}]${NC} Publishing..."

  # Get site URL
  SITE_UPPER=$(echo "$site" | tr '[:lower:]' '[:upper:]')
  SITE_URL_VAR="WP_SITE_${SITE_UPPER}_URL"
  SITE_URL="${!SITE_URL_VAR}"

  if [[ -z "$SITE_URL" ]]; then
    echo -e "  ${RED}✗ No URL configured${NC}"
    ((FAILED++))
    continue
  fi

  # Get credentials
  WP_USER="${WP_USERNAME:-peter}"
  WP_PASS_VAR="WP_SITE_${SITE_UPPER}_PASS"
  WP_PASS="${!WP_PASS_VAR}"

  # Create post
  RESPONSE=$(curl -s -X POST "${SITE_URL}/wp-json/wp/v2/posts" \
    -u "${WP_USER}:${WP_PASS}" \
    -H "Content-Type: application/json" \
    -d "{
      \"title\": \"${TITLE}\",
      \"content\": $(echo "$CONTENT" | jq -Rs .),
      \"status\": \"draft\"
    }")

  POST_ID=$(echo "$RESPONSE" | jq -r '.id' 2>/dev/null)

  if [[ -z "$POST_ID" ]] || [[ "$POST_ID" == "null" ]]; then
    echo -e "  ${RED}✗ Failed to create draft${NC}"
    echo "  Response: $RESPONSE"
    ((FAILED++))
    continue
  fi

  echo -e "  ${GREEN}✓ Draft created (ID: ${POST_ID})${NC}"
  ((PUBLISHED++))
done

echo ""
echo -e "${GREEN}=== Results ===${NC}"
echo -e "Published: ${GREEN}${PUBLISHED}${NC}"
echo -e "Failed: ${RED}${FAILED}${NC}"
echo ""
echo -e "${YELLOW}Note: Articles created as drafts. Use publish-gateway.sh to publish after review.${NC}"

exit 0
