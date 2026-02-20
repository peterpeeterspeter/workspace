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
  # Get site URL from env - use correct variable names
  case "$site" in
    crashcasino)
      SITE_URL="${WORDPRESS_CRASHCASINO_URL:-}"
      WP_USER="${WORDPRESS_CRASHCASINO_USER:-peter}"
      WP_PASS="${WORDPRESS_CRASHCASINO_APP_PASSWORD:-}"
      ;;
    crashgame)
      SITE_URL="${WORDPRESS_CRASHGAMEGAMBLING_URL:-}"
      WP_USER="${WORDPRESS_CRASHGAMEGAMBLING_USER:-@peter}"
      WP_PASS="${WORDPRESS_CRASHGAMEGAMBLING_APP_PASSWORD:-}"
      ;;
    freecrash)
      SITE_URL="${WORDPRESS_FREECRASH_URL:-}"
      WP_USER="${WORDPRESS_FREECRASH_USER:-@peter}"
      WP_PASS="${WORDPRESS_FREECRASH_APP_PASSWORD:-}"
      ;;
    cryptocrash)
      SITE_URL="${WORDPRESS_CRYPTOCRASH_URL:-}"
      WP_USER="${WORDPRESS_CRYPTOCRASH_USER:-@peter}"
      WP_PASS="${WORDPRESS_CRYPTOCRASH_APP_PASSWORD:-}"
      ;;
    hobbysalon)
      SITE_URL="${WORDPRESS_HOBBSALON_URL:-}"
      WP_USER="${WORDPRESS_HOBBSALON_USER:-peter}"
      WP_PASS="${WORDPRESS_HOBBSALON_APP_PASSWORD:-}"
      ;;
    *)
      echo -e "${YELLOW}Warning: Unknown site '${site}'${NC}"
      continue
      ;;
  esac

  if [[ -z "$SITE_URL" ]]; then
    echo -e "${YELLOW}Warning: No URL configured for '${site}'${NC}"
    continue
  fi

  # Remove /wp-json suffix if present (we'll add it in the API calls)
  SITE_URL="${SITE_URL%/wp-json}"

  # Debug: show what URL we're using
  if [[ "${DEBUG:-0}" == "1" ]]; then
    echo "  [DEBUG] URL: ${SITE_URL}" >&2
    echo "  [DEBUG] User: ${WP_USER}" >&2
  fi

  echo -e "${BLUE}📊 ${site^^}${NC}"

  # Test connectivity first (with -k for SSL issues)
  HTTP_CODE=$(curl -s -k -o /dev/null -w "%{http_code}" "${SITE_URL}/wp-json/wp/v2/posts?per_page=1" \
    -u "${WP_USER}:${WP_PASS}" 2>/dev/null || echo "000")

  if [[ "$HTTP_CODE" == "000" ]]; then
    echo -e "  ${YELLOW}Site niet bereikbaar (connectie fout)${NC}"
    echo ""
    continue
  fi

  # Get counts for each status (with -k for SSL issues and better error handling)
  PUBLISHED=$(curl -s -k "${SITE_URL}/wp-json/wp/v2/posts?per_page=1&status=publish" \
    -u "${WP_USER}:${WP_PASS}" | jq 'length' 2>/dev/null || echo "0")

  DRAFTS=$(curl -s -k "${SITE_URL}/wp-json/wp/v2/posts?per_page=1&status=draft" \
    -u "${WP_USER}:${WP_PASS}" | jq 'length' 2>/dev/null || echo "0")

  PENDING=$(curl -s -k "${SITE_URL}/wp-json/wp/v2/posts?per_page=1&status=pending" \
    -u "${WP_USER}:${WP_PASS}" | jq 'length' 2>/dev/null || echo "0")

  SCHEDULED=$(curl -s -k "${SITE_URL}/wp-json/wp/v2/posts?per_page=1&status=future" \
    -u "${WP_USER}:${WP_PASS}" | jq 'length' 2>/dev/null || echo "0")

  # Media count
  MEDIA=$(curl -s -k "${SITE_URL}/wp-json/wp/v2/media?per_page=1" \
    -u "${WP_USER}:${WP_PASS}" | jq 'length' 2>/dev/null || echo "0")

  # Comments count
  COMMENTS_APPROVED=$(curl -s -k "${SITE_URL}/wp-json/wp/v2/comments?per_page=1&status=approved" \
    -u "${WP_USER}:${WP_PASS}" | jq 'length' 2>/dev/null || echo "0")

  COMMENTS_PENDING=$(curl -s -k "${SITE_URL}/wp-json/wp/v2/comments?per_page=1&status=hold" \
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
