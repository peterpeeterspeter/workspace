#!/bin/bash
# Pinch-to-Post Helper: Content Calendar
# View publishing schedule across sites

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
  echo "Usage: $0 <year-month> [site]"
  echo ""
  echo "Example:"
  echo "  $0 2026-02              # All sites for February 2026"
  echo "  $0 2026-02 crashcasino  # Specific site"
  exit 1
}

# Check arguments
if [[ $# -lt 1 ]]; then
  usage
fi

MONTH="$1"
SITE="${2:-all}"

# Parse year-month
if [[ ! "$MONTH" =~ ^[0-9]{4}-[0-9]{2}$ ]]; then
  echo -e "${RED}Error: Invalid date format. Use YYYY-MM${NC}"
  exit 1
fi

YEAR="${MONTH%-*}"
MON="${MONTH#*-}"

# First and last day of month
FIRST_DAY="${YEAR}-${MON}-01T00:00:00"
LAST_DAY="${YEAR}-${MON}-31T23:59:59"

# Sites to query
if [[ "$SITE" == "all" ]]; then
  SITES=("crashcasino" "crashgame" "freecrash" "cryptocrash" "hobbysalon")
else
  SITES=("$SITE")
fi

echo -e "${GREEN}=== Content Calendar: ${MONTH} ===${NC}"
echo ""

for site in "${SITES[@]}"; do
  # Get site URL from env
  SITE_UPPER=$(echo "$site" | tr '[:lower:]' '[:upper:]')
  SITE_URL_VAR="WP_SITE_${SITE_UPPER}_URL"
  SITE_URL="${!SITE_URL_VAR}"

  if [[ -z "$SITE_URL" ]]; then
    echo -e "${YELLOW}Warning: No URL configured for '${site}'${NC}"
    continue
  fi

  # Get credentials
  WP_USER="${WP_USERNAME:-peter}"
  WP_PASS_VAR="WP_SITE_${SITE_UPPER}_PASS"
  WP_PASS="${!WP_PASS_VAR}"

  echo -e "${BLUE}📅 ${site^^}${NC}"
  echo ""

  # Published posts
  echo -e "${GREEN}📗 Published:${NC}"
  curl -s "${SITE_URL}/wp-json/wp/v2/posts?per_page=100&status=publish&after=${FIRST_DAY}&before=${LAST_DAY}" \
    -u "${WP_USER}:${WP_PASS}" | \
    jq -r '.[] | "  \(.date | split("T")[0]) - \(.title // "(no title)")"' 2>/dev/null || echo "  None"

  echo ""

  # Scheduled posts
  echo -e "${YELLOW}📅 Scheduled:${NC}"
  curl -s "${SITE_URL}/wp-json/wp/v2/posts?per_page=100&status=future&after=${FIRST_DAY}&before=${LAST_DAY}" \
    -u "${WP_USER}:${WP_PASS}" | \
    jq -r '.[] | "  \(.date | split("T")[0]) - \(.title // "(no title)")"' 2>/dev/null || echo "  None"

  echo ""

  # Draft count
  DRAFT_COUNT=$(curl -s "${SITE_URL}/wp-json/wp/v2/posts?per_page=1&status=draft" \
    -u "${WP_USER}:${WP_PASS}" | jq 'length' 2>/dev/null || echo "0")

  echo -e "${YELLOW}📝 Drafts: ${DRAFT_COUNT}${NC}"
  echo ""
done

exit 0
