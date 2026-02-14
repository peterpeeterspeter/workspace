#!/bin/bash
# Pinch-to-Post Helper: Comment Moderation
# Auto-moderate comments (approve good, mark spam)

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
  echo "Usage: $0 <site> <action>"
  echo ""
  echo "Actions:"
  echo "  approve-all   - Approve all pending comments"
  echo "  spam-all      - Mark all pending as spam"
  echo "  show-pending  - Show pending comments"
  echo "  spam-suspicious - Mark suspicious comments as spam"
  echo ""
  echo "Example:"
  echo "  $0 crashcasino approve-all"
  echo "  $0 crashcasino spam-suspicious"
  exit 1
}

# Check arguments
if [[ $# -lt 2 ]]; then
  usage
fi

SITE="$1"
ACTION="$2"

# Validate site
VALID_SITES=("crashcasino" "crashgame" "freecrash" "cryptocrash")
if [[ ! " ${VALID_SITES[@]} " =~ " ${SITE} " ]]; then
  echo -e "${RED}Error: Invalid site '${SITE}'${NC}"
  echo "Valid sites: ${VALID_SITES[*]}"
  exit 1
fi

# Get site URL
SITE_UPPER=$(echo "$SITE" | tr '[:lower:]' '[:upper:]')

# Try both WP_SITE_* and WORDPRESS_* variable names
SITE_URL_VAR="WP_SITE_${SITE_UPPER}_URL"
SITE_URL="${!SITE_URL_VAR}"
if [[ -z "$SITE_URL" ]]; then
  SITE_URL_VAR="WORDPRESS_${SITE_UPPER}_URL"
  SITE_URL="${!SITE_URL_VAR}"
fi

if [[ -z "$SITE_URL" ]]; then
  echo -e "${RED}Error: No URL configured for '${SITE}'${NC}"
  exit 1
fi

# Get credentials - try both variable naming schemes
WP_USER="${WP_USERNAME:-}"
if [[ -z "$WP_USER" ]]; then
  WP_USER_VAR="WORDPRESS_${SITE_UPPER}_USER"
  WP_USER="${!WP_USER_VAR}"
fi
WP_USER="${WP_USER:-peter}"

# Get password
WP_PASS="${WP_PASSWORD:-}"
if [[ -z "$WP_PASS" ]]; then
  WP_PASS_VAR="WP_SITE_${SITE_UPPER}_PASS"
  WP_PASS="${!WP_PASS_VAR}"
fi
if [[ -z "$WP_PASS" ]]; then
  WP_PASS_VAR="WORDPRESS_${SITE_UPPER}_APP_PASSWORD"
  WP_PASS="${!WP_PASS_VAR}"
fi

echo -e "${GREEN}=== Comment Moderation ===${NC}"
echo "Site: ${SITE}"
echo "Action: ${ACTION}"
echo ""

case "$ACTION" in
  show-pending)
    echo -e "${YELLOW}Pending Comments:${NC}"
    echo ""

    PENDING=$(curl -s "${SITE_URL}/wp/v2/comments?status=hold&per_page=100" \
      -u "${WP_USER}:${WP_PASS}")

    COUNT=$(echo "$PENDING" | jq 'length' 2>/dev/null || echo "0")

    if [[ "$COUNT" -eq 0 ]]; then
      echo "  No pending comments"
    else
      echo "$PENDING" | jq -r '.[] |
        "  ID: \(.id)
     Author: \(.author_name // "(no name)")
     URL: \(.author_url // "(no url)")
     Date: \(.date | split("T")[0])
     Content: \(.content.rendered | gsub("<[^>]*>"; "") | if length > 80 then .[0:80] + "..." else . end)
    "'
    fi

    echo ""
    echo "Total pending: ${COUNT}"
    ;;

  approve-all)
    echo -e "${YELLOW}Approving all pending comments...${NC}"

    PENDING=$(curl -s "${SITE_URL}/wp/v2/comments?status=hold&per_page=100" \
      -u "${WP_USER}:${WP_PASS}")

    COUNT=$(echo "$PENDING" | jq 'length' 2>/dev/null || echo "0")

    if [[ "$COUNT" -eq 0 ]]; then
      echo "  No pending comments to approve"
      exit 0
    fi

    APPROVED=0
    FAILED=0

    for id in $(echo "$PENDING" | jq -r '.[].id' 2>/dev/null); do
      if curl -s -X POST "${SITE_URL}/wp/v2/comments/${id}" \
        -u "${WP_USER}:${WP_PASS}" \
        -H "Content-Type: application/json" \
        -d '{"status": "approved"}' | jq -e '.id' > /dev/null 2>&1; then
        ((APPROVED++))
      else
        ((FAILED++))
      fi
    done

    echo -e "${GREEN}✓ Approved: ${APPROVED}${NC}"
    [[ $FAILED -gt 0 ]] && echo -e "${RED}✗ Failed: ${FAILED}${NC}"
    ;;

  spam-all)
    echo -e "${YELLOW}Marking all pending as spam...${NC}"

    PENDING=$(curl -s "${SITE_URL}/wp/v2/comments?status=hold&per_page=100" \
      -u "${WP_USER}:${WP_PASS}")

    COUNT=$(echo "$PENDING" | jq 'length' 2>/dev/null || echo "0")

    if [[ "$COUNT" -eq 0 ]]; then
      echo "  No pending comments"
      exit 0
    fi

    SPAMMED=0
    FAILED=0

    for id in $(echo "$PENDING" | jq -r '.[].id' 2>/dev/null); do
      if curl -s -X POST "${SITE_URL}/wp/v2/comments/${id}" \
        -u "${WP_USER}:${WP_PASS}" \
        -H "Content-Type: application/json" \
        -d '{"status": "spam"}' | jq -e '.id' > /dev/null 2>&1; then
        ((SPAMMED++))
      else
        ((FAILED++))
      fi
    done

    echo -e "${GREEN}✓ Marked as spam: ${SPAMMED}${NC}"
    [[ $FAILED -gt 0 ]] && echo -e "${RED}✗ Failed: ${FAILED}${NC}"
    ;;

  spam-suspicious)
    echo -e "${YELLOW}Checking for suspicious comments...${NC}"

    PENDING=$(curl -s "${SITE_URL}/wp/v2/comments?status=hold&per_page=100" \
      -u "${WP_USER}:${WP_PASS}")

    COUNT=$(echo "$PENDING" | jq 'length' 2>/dev/null || echo "0")

    if [[ "$COUNT" -eq 0 ]]; then
      echo "  No pending comments"
      exit 0
    fi

    SPAMMED=0

    # Suspicious indicators
    SUSPICIOUS_PATTERNS=(
      "casino"
      "viagra"
      "cialis"
      "bitcoin"
      "crypto"
      "loan"
      "porn"
      "xxx"
      ".ru"
      "seo"
      "click here"
      "check this"
      "great post"
      "nice article"
      "very informative"
      "useful information"
    )

    while IFS= read -r comment; do
      COMMENT_ID=$(echo "$comment" | jq -r '.id')
      COMMENT_CONTENT=$(echo "$comment" | jq -r '.content.rendered' | sed 's/<[^>]*>//g')
      COMMENT_AUTHOR=$(echo "$comment" | jq -r '.author_name')
      COMMENT_URL=$(echo "$comment" | jq -r '.author_url')

      # Check for suspicious patterns (in content, author, and URL)
      IS_SPAM=false

      # Check content for patterns
      for pattern in "${SUSPICIOUS_PATTERNS[@]}"; do
        if echo "$COMMENT_CONTENT" | grep -iq "$pattern"; then
          IS_SPAM=true
          break
        fi
      done

      # Check author name for spam patterns (dating, adult, sex, etc.)
      if [[ "$IS_SPAM" == "false" ]]; then
        if echo "$COMMENT_AUTHOR" | grep -iqE "(dating|sex|adult|porn|xxx|casino|viagra|cialis)"; then
          IS_SPAM=true
        fi
      fi

      # Check for generic comments (likely bot spam)
      if echo "$COMMENT_CONTENT" | grep -iqE "^(great|nice|good|very good|excellent|awesome|amazing)"; then
        if [[ ${#COMMENT_CONTENT} -lt 50 ]]; then
          IS_SPAM=true
        fi
      fi

      # Check for URL spam
      if [[ -n "$COMMENT_URL" ]] && [[ "$COMMENT_URL" != "http"* ]]; then
        IS_SPAM=true
      fi

      # Check for suspicious domains (yandex.com poll spam)
      if echo "$COMMENT_URL" | grep -iq "yandex.com/poll"; then
        IS_SPAM=true
      fi

      if [[ "$IS_SPAM" == "true" ]]; then
        echo -e "  ${YELLOW}Marking as spam: ${COMMENT_ID}${NC}"
        echo "    Author: ${COMMENT_AUTHOR}"
        echo "    Content: ${COMMENT_CONTENT:0:80}..."

        if curl -s -X POST "${SITE_URL}/wp/v2/comments/${COMMENT_ID}" \
          -u "${WP_USER}:${WP_PASS}" \
          -H "Content-Type: application/json" \
          -d '{"status": "spam"}' | jq -e '.id' > /dev/null 2>&1; then
          ((SPAMMED++))
        fi
      fi
    done < <(echo "$PENDING" | jq -c '.[]')

    echo ""
    echo -e "${GREEN}✓ Marked as spam: ${SPAMMED}${NC}"
    ;;

  *)
    echo -e "${RED}Error: Unknown action '${ACTION}'${NC}"
    usage
    ;;
esac

exit 0
