#!/bin/bash
# Pinch-to-Post Helper: Fix Affiliate Links
# Bulk fix wrong affiliate domains and add missing affiliate links

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Correct affiliate links (Peter's links)
CORRECT_AFFILIATES=(
  "cybetplay.com/tluy6cbpp"
  "bzstarz1.com/b196c322b"
  "betzrd.com/pyondmfcx"
  "7bit.partners/p4i4w1udu"
  "mirax.partners/p4fp2iusj"
  "trustdice.win/?ref=u_peterp"
  "reffpa.com/L?tag=d_4381452m_97c_"
  "betfury.bet/df1865703"
)

# Wrong domains to replace
WRONG_DOMAINS=(
  "stake.com"
  "bc.game"
  "thunderpick.com"
  "roobet.com"
  "metaspins.com"
  "bitstarz.com"
  "7bitcasino.com"
)

usage() {
  echo "Usage: $0 <site> [post_ids...]"
  echo ""
  echo "If no post_ids provided, will scan recent 100 posts and fix all that need it"
  echo ""
  echo "Examples:"
  echo "  $0 crashcasino           # Fix all recent posts on crashcasino"
  echo "  $0 crashcasino 123 456   # Fix specific posts"
  echo "  $0 crashgame 100-200     # Fix range of posts"
  exit 1
}

# Check arguments
if [[ $# -lt 1 ]]; then
  usage
fi

SITE="$1"
shift

# Site credentials
case "$SITE" in
  crashcasino)
    WP_URL="https://crashcasino.io/wp-json"
    WP_USER="peter"
    WP_PASS="3vRhtTs2khfdLtTiDFqkdeXI"
    ;;
  crashgame)
    WP_URL="https://crashgamegambling.com/wp-json"
    WP_USER="@peter"
    WP_PASS="MioX SygN Xaz6 pK9o RUiK tBMF"
    ;;
  freecrash)
    WP_URL="https://freecrashgames.com/wp-json"
    WP_USER="@peter"
    WP_PASS="F8Mg yZXM qJy4 jQvp BMeZ FoMG"
    ;;
  cryptocrash)
    WP_URL="https://cryptocrashgambling.com/wp-json"
    WP_USER="@peter"
    WP_PASS="R3kQ 6vRA UwYd x7Cn KEtT Pk83"
    ;;
  *)
    echo -e "${RED}Error: Invalid site '${SITE}'${NC}"
    echo "Valid sites: crashcasino, crashgame, freecrash, cryptocrash"
    exit 1
    ;;
esac

# Function to fetch posts
fetch_posts() {
  local limit=$1
  curl -s -u "${WP_USER}:${WP_PASS}" \
    "${WP_URL}/wp/v2/posts?per_page=${limit}&orderby=date&order=desc&_fields=id,title,content,link" \
    2>/dev/null
}

# Function to check if post needs fixing
check_post() {
  local content=$1
  local has_wrong=0
  local has_correct=0

  # Check for wrong domains
  for domain in "${WRONG_DOMAINS[@]}"; do
    if [[ "$content" == *"$domain"* ]]; then
      has_wrong=1
      break
    fi
  done

  # Check for correct affiliate links
  for affiliate in "${CORRECT_AFFILIATES[@]}"; do
    if [[ "$content" == *"$affiliate"* ]]; then
      has_correct=1
      break
    fi
  done

  if [[ $has_wrong -eq 1 ]] || [[ $has_correct -eq 0 ]]; then
    return 0  # Needs fixing
  fi
  return 1  # Already good
}

# Function to fix affiliate links in content
fix_content() {
  local content=$1

  # Replace wrong domains with Cybet (primary affiliate)
  content=$(echo "$content" | sed 's|https://[^/]*stake\.com[^[:space:]"<>]*|https://cybetplay.com/tluy6cbpp|gI')
  content=$(echo "$content" | sed 's|https://[^/]*bc\.game[^[:space:]"<>]*|https://cybetplay.com/tluy6cbpp|gI')
  content=$(echo "$content" | sed 's|https://[^/]*thunderpick\.com[^[:space:]"<>]*|https://cybetplay.com/tluy6cbpp|gI')
  content=$(echo "$content" | sed 's|https://[^/]*roobet\.com[^[:space:]"<>]*|https://cybetplay.com/tluy6cbpp|gI')
  content=$(echo "$content" | sed 's|https://[^/]*metaspins\.com[^[:space:]"<>]*|https://cybetplay.com/tluy6cbpp|gI')
  content=$(echo "$content" | sed 's|https://[^/]*bitstarz\.com[^[:space:]"<>]*|https://bzstarz1.com/b196c322b|gI')
  content=$(echo "$content" | sed 's|https://[^/]*7bitcasino\.com[^[:space:]"<>]*|https://7bit.partners/p4i4w1udu|gI')

  echo "$content"
}

# Function to update post
update_post() {
  local post_id=$1
  local new_content=$2

  curl -s -X POST \
    -u "${WP_USER}:${WP_PASS}" \
    -H "Content-Type: application/json" \
    -d "{\"content\": $(echo "$new_content" | jq -Rs .)}" \
    "${WP_URL}/wp/v2/posts/${post_id}" \
    2>/dev/null
}

# Main operation
echo -e "${BLUE}=== Affiliate Link Fix ===${NC}"
echo "Site: ${SITE}"
echo ""

# Get post IDs to process
if [[ $# -eq 0 ]]; then
  echo -e "${YELLOW}Scanning recent posts...${NC}"
  POSTS_JSON=$(fetch_posts 100)

  if [[ -z "$POSTS_JSON" ]] || [[ "$POSTS_JSON" == "[]" ]]; then
    echo -e "${RED}No posts found${NC}"
    exit 1
  fi

  # Extract post IDs that need fixing
  POST_IDS=()
  TOTAL=0

  while IFS= read -r line; do
    ((TOTAL++))
    post_id=$(echo "$line" | jq -r '.id')
    title=$(echo "$line" | jq -r '.title.rendered')
    content=$(echo "$line" -r '.content.rendered')

    if check_post "$content"; then
      POST_IDS+=("$post_id")
    fi
  done < <(echo "$POSTS_JSON" | jq -c '.[]')

  echo -e "Scanned ${TOTAL} posts, found ${#POST_IDS[@]} needing fixes"
  echo ""
else
  # Expand ranges if any
  POST_IDS=()
  for id in "$@"; do
    if [[ "$id" =~ ^([0-9]+)-([0-9]+)$ ]]; then
      start=${BASH_REMATCH[1]}
      end=${BASH_REMATCH[2]}
      for ((i=start; i<=end; i++)); do
        POST_IDS+=("$i")
      done
    else
      POST_IDS+=("$id")
    fi
  done
fi

if [[ ${#POST_IDS[@]} -eq 0 ]]; then
  echo -e "${GREEN}✓ All posts already have correct affiliate links!${NC}"
  exit 0
fi

echo -e "${BLUE}Processing ${#POST_IDS[@]} posts...${NC}"
echo ""

# Track results
FIXED=0
FAILED=0
ALREADY_GOOD=0

for post_id in "${POST_IDS[@]}"; do
  echo -ne "${YELLOW}[${post_id}]${NC} Checking..."

  # Fetch post content
  POST_JSON=$(curl -s -u "${WP_USER}:${WP_PASS}" \
    "${WP_URL}/wp/v2/posts/${post_id}?_fields=id,title,content" \
    2>/dev/null)

  if [[ -z "$POST_JSON" ]] || [[ "$POST_JSON" == *"code"* ]]; then
    echo -e " ${RED}✗ Failed to fetch${NC}"
    ((FAILED++))
    continue
  fi

  content=$(echo "$POST_JSON" | jq -r '.content.rendered // ""')
  title=$(echo "$POST_JSON" | jq -r '.title.rendered // ""')

  # Check if fixing needed
  if ! check_post "$content"; then
    echo -e " ${GREEN}✓ Already good${NC}"
    ((ALREADY_GOOD++))
    continue
  fi

  # Fix content
  fixed_content=$(fix_content "$content")

  # Update post
  result=$(update_post "$post_id" "$fixed_content")

  if [[ -z "$result" ]] || [[ "$result" == *"code"* ]]; then
    echo -e " ${RED}✗ Failed to update${NC}"
    ((FAILED++))
  else
    echo -e " ${GREEN}✓ Fixed${NC}"
    ((FIXED++))
  fi
done

echo ""
echo -e "${BLUE}=== Results ===${NC}"
echo -e "Fixed: ${GREEN}${FIXED}${NC}"
echo -e "Already good: ${GREEN}${ALREADY_GOOD}${NC}"
echo -e "Failed: ${RED}${FAILED}${NC}"
echo -e "Total processed: ${#POST_IDS[@]}"

exit 0
