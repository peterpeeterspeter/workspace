#!/bin/bash
# Pinch-to-Post Helper: Content Statistics
# Generate performance reports across sites

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="/root/.openclaw/workspace"

# Load credentials
source "$WORKSPACE/.env" 2>/dev/null || true

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

usage() {
  echo "Usage: $0 [site]"
  echo ""
  echo "Example:"
  echo "  $0              # All sites"
  echo "  $0 crashcasino  # Specific site"
  exit 1
}

SITE="${1:-all}"

# Sites to query
if [[ "$SITE" == "all" ]]; then
  SITES=("crashcasino" "crashgame" "freecrash" "cryptocrash" "hobbysalon")
else
  SITES=("$SITE")
fi

echo -e "${GREEN}=== Content Statistics ===${NC}"
echo ""

TOTAL_PUBLISHED=0
TOTAL_DRAFTS=0
TOTAL_PENDING=0
TOTAL_SCHEDULED=0

for site in "${SITES[@]}"; do
  # Get site URL from env - try both WP_SITE_* and WORDPRESS_* variable names
  SITE_UPPER=$(echo "$site" | tr '[:lower:]' '[:upper:]')
  SITE_URL_VAR="WP_SITE_${SITE_UPPER}_URL"
  SITE_URL="${!SITE_URL_VAR}"
  if [[ -z "$SITE_URL" ]]; then
    SITE_URL_VAR="WORDPRESS_${SITE_UPPER}_URL"
    SITE_URL="${!SITE_URL_VAR}"
  fi

  if [[ -z "$SITE_URL" ]]; then
    echo -e "${YELLOW}Warning: No URL configured for '${site}'${NC}"
    continue
  fi

  # Get credentials - try both variable naming schemes
  WP_USER="${WP_USERNAME:-}"
  if [[ -z "$WP_USER" ]]; then
    WP_USER_VAR="WORDPRESS_${SITE_UPPER}_USER"
    WP_USER="${!WP_USER_VAR}"
  fi
  WP_USER="${WP_USER:-peter}"

  # Get password - try both variable naming schemes
  WP_PASS="${WP_PASSWORD:-}"
  if [[ -z "$WP_PASS" ]]; then
    WP_PASS_VAR="WP_SITE_${SITE_UPPER}_PASS"
    WP_PASS="${!WP_PASS_VAR}"
  fi
  if [[ -z "$WP_PASS" ]]; then
    WP_PASS_VAR="WORDPRESS_${SITE_UPPER}_APP_PASSWORD"
    WP_PASS="${!WP_PASS_VAR}"
  fi

  echo -e "${BLUE}📊 ${site^^}${NC}"

  # Get counts for each status
  PUBLISHED=$(curl -s "${SITE_URL}/wp-json/wp/v2/posts?per_page=1&status=publish" \
    -u "${WP_USER}:${WP_PASS}" | jq 'length' 2>/dev/null || echo "0")

  DRAFTS=$(curl -s "${SITE_URL}/wp-json/wp/v2/posts?per_page=1&status=draft" \
    -u "${WP_USER}:${WP_PASS}" | jq 'length' 2>/dev/null || echo "0")

  PENDING=$(curl -s "${SITE_URL}/wp-json/wp/v2/posts?per_page=1&status=pending" \
    -u "${WP_USER}:${WP_PASS}" | jq 'length' 2>/dev/null || echo "0")

  SCHEDULED=$(curl -s "${SITE_URL}/wp-json/wp/v2/posts?per_page=1&status=future" \
    -u "${WP_USER}:${WP_PASS}" | jq 'length' 2>/dev/null || echo "0")

  # Media count
  MEDIA=$(curl -s "${SITE_URL}/wp-json/wp/v2/media?per_page=1" \
    -u "${WP_USER}:${WP_PASS}" | jq 'length' 2>/dev/null || echo "0")

  # Comments count
  COMMENTS_APPROVED=$(curl -s "${SITE_URL}/wp-json/wp/v2/comments?per_page=1&status=approved" \
    -u "${WP_USER}:${WP_PASS}" | jq 'length' 2>/dev/null || echo "0")

  COMMENTS_PENDING=$(curl -s "${SITE_URL}/wp-json/wp/v2/comments?per_page=1&status=hold" \
    -u "${WP_USER}:${WP_PASS}" | jq 'length' 2>/dev/null || echo "0")

  echo -e "  Published: ${GREEN}${PUBLISHED}${NC}"
  echo -e "  Drafts: ${YELLOW}${DRAFTS}${NC}"
  echo -e "  Pending Review: ${PENDING}"
  echo -e "  Scheduled: ${SCHEDULED}"
  echo -e "  Media Files: ${MEDIA}"
  echo -e "  Comments (approved): ${COMMENTS_APPROVED}"
  echo -e "  Comments (pending): ${YELLOW}${COMMENTS_PENDING}${NC}"
  echo ""

  # Accumulate totals
  ((TOTAL_PUBLISHED += PUBLISHED))
  ((TOTAL_DRAFTS += DRAFTS))
  ((TOTAL_PENDING += PENDING))
  ((TOTAL_SCHEDULED += SCHEDULED))
done

if [[ "$SITE" == "all" ]]; then
  echo -e "${GREEN}=== Total Across All Sites ===${NC}"
  echo -e "  Published: ${GREEN}${TOTAL_PUBLISHED}${NC}"
  echo -e "  Drafts: ${YELLOW}${TOTAL_DRAFTS}${NC}"
  echo -e "  Pending: ${TOTAL_PENDING}"
  echo -e "  Scheduled: ${TOTAL_SCHEDULED}"
fi

exit 0
