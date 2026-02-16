#!/bin/bash
# Pinch-to-Post Helper: Bulk Publish
# Publish multiple articles at once with quality checks

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GATEWAY_SCRIPT="/root/.openclaw/workspace/scripts/publish-gateway.sh"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

usage() {
  echo "Usage: $0 <site> <post_ids...>"
  echo ""
  echo "Example:"
  echo "  $0 crashcasino 123 456 789"
  echo "  $0 crashgame 100-110  # Publish range"
  exit 1
}

# Check arguments
if [[ $# -lt 2 ]]; then
  usage
fi

SITE="$1"
shift
POST_IDS="$@"

# Validate site
VALID_SITES=("crashcasino" "crashgame" "freecrash" "cryptocrash" "hobbysalon")
if [[ ! " ${VALID_SITES[@]} " =~ " ${SITE} " ]]; then
  echo -e "${RED}Error: Invalid site '${SITE}'${NC}"
  echo "Valid sites: ${VALID_SITES[*]}"
  exit 1
fi

# Expand ranges if any
EXPANDED_IDS=()
for id in $POST_IDS; do
  if [[ "$id" =~ ^([0-9]+)-([0-9]+)$ ]]; then
    start=${BASH_REMATCH[1]}
    end=${BASH_REMATCH[2]}
    for ((i=start; i<=end; i++)); do
      EXPANDED_IDS+=($i)
    done
  else
    EXPANDED_IDS+=($id)
  fi
done

echo -e "${GREEN}=== Bulk Publish Operation ===${NC}"
echo "Site: ${SITE}"
echo "Posts: ${EXPANDED_IDS[*]} (${#EXPANDED_IDS[@]} articles)"
echo ""

# Results tracking
PUBLISHED=0
FAILED=0
SKIPPED=0

for post_id in "${EXPANDED_IDS[@]}"; do
  echo -e "${YELLOW}[${post_id}]${NC} Checking..."

  # Run health check
  if ! SCORE=$("$GATEWAY_SCRIPT" check "$post_id" "$SITE" 2>&1); then
    echo -e "  ${RED}✗ Failed to check post${NC}"
    ((FAILED++))
    continue
  fi

  # Extract score from output (format: "Score: XX/100")
  if [[ "$SCORE" =~ ([0-9]+)/100 ]]; then
    SCORE_VALUE=${BASH_REMATCH[1]}
  else
    echo -e "  ${RED}✗ Could not parse score${NC}"
    ((FAILED++))
    continue
  fi

  if [[ $SCORE_VALUE -lt 80 ]]; then
    echo -e "  ${YELLOW}⊘ Skipped (score: ${SCORE_VALUE}/100, needs 80+)${NC}"
    ((SKIPPED++))
    continue
  fi

  # Publish
  echo -e "  ${GREEN}✓ Publishing (score: ${SCORE_VALUE}/100)...${NC}"
  if "$GATEWAY_SCRIPT" publish "$post_id" "$SITE" > /dev/null 2>&1; then
    echo -e "  ${GREEN}✓ Published${NC}"
    ((PUBLISHED++))
  else
    echo -e "  ${RED}✗ Failed to publish${NC}"
    ((FAILED++))
  fi
done

echo ""
echo -e "${GREEN}=== Results ===${NC}"
echo -e "Published: ${GREEN}${PUBLISHED}${NC}"
echo -e "Skipped: ${YELLOW}${SKIPPED}${NC}"
echo -e "Failed: ${RED}${FAILED}${NC}"
echo "Total: ${#EXPANDED_IDS[@]}"

exit 0
