#!/bin/bash
# Pinch-to-Post Helper: Media Management
# Upload images with alt text and set as featured

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
  echo "Usage: $0 <site> <image_path> [alt_text] [caption] [post_id]"
  echo ""
  echo "Example:"
  echo "  $0 crashcasino /path/to/image.jpg \"Crash game screenshot\""
  echo "  $0 crashcasino /path/to/image.jpg \"Screenshot\" \"How to play\" 123"
  echo ""
  echo "If post_id is provided, image will be set as featured image for that post."
  exit 1
}

# Check arguments
if [[ $# -lt 2 ]]; then
  usage
fi

SITE="$1"
IMAGE_PATH="$2"
ALT_TEXT="${3:-}"
CAPTION="${4:-}"
POST_ID="${5:-}"

# Validate site
VALID_SITES=("crashcasino" "crashgame" "freecrash" "cryptocrash")
if [[ ! " ${VALID_SITES[@]} " =~ " ${SITE} " ]]; then
  echo -e "${RED}Error: Invalid site '${SITE}'${NC}"
  echo "Valid sites: ${VALID_SITES[*]}"
  exit 1
fi

# Check image exists
if [[ ! -f "$IMAGE_PATH" ]]; then
  echo -e "${RED}Error: File not found: ${IMAGE_PATH}${NC}"
  exit 1
fi

# Get site URL - match .env variable names
URL_VAR="WORDPRESS_${SITE^^}_URL"
SITE_URL="${!URL_VAR}"

# Fallback to hardcoded URLs if env var not set
if [[ -z "$SITE_URL" ]]; then
  case "$SITE" in
    crashcasino)
      SITE_URL="https://crashcasino.io/wp-json"
      ;;
    crashgame)
      SITE_URL="https://crashgamegambling.com/wp-json"
      ;;
    freecrash)
      SITE_URL="https://freecrashgames.com/wp-json"
      ;;
    cryptocrash)
      SITE_URL="https://cryptocrashgambling.com/wp-json"
      ;;
  esac
fi

# Get credentials - match .env variable names
WP_USER="${WP_USERNAME:-peter}"
PASS_VAR="WORDPRESS_${SITE^^}_APP_PASSWORD"
WP_PASS="${!PASS_VAR}"

# Fallback to hardcoded creds if env var not set
if [[ -z "$WP_PASS" ]]; then
  case "$SITE" in
    crashcasino)
      WP_PASS="3vRhtTs2khfdLtTiDFqkdeXI"
      ;;
    crashgame)
      WP_PASS="MioX SygN Xaz6 pK9o RUiK tBMF"
      ;;
    freecrash)
      WP_PASS="F8Mg yZXM qJy4 jQvp BMeZ FoMG"
      ;;
    cryptocrash)
      WP_PASS="R3kQ 6vRA UwYd x7Cn KEtT Pk83"
      ;;
  esac
fi

# Get filename
FILENAME=$(basename "$IMAGE_PATH")
EXT="${FILENAME##*.}"
MIME_TYPE="image/${EXT}"

echo -e "${GREEN}=== Media Upload ===${NC}"
echo "Site: ${SITE}"
echo "File: ${IMAGE_PATH}"
echo "Alt Text: ${ALT_TEXT:-"(none)"}"
echo "Caption: ${CAPTION:-"(none)"}"
if [[ -n "$POST_ID" ]]; then
  echo "Set as featured for post: ${POST_ID}"
fi
echo ""

# Upload image
echo -e "${YELLOW}Uploading...${NC}"

RESPONSE=$(curl -s -X POST "${SITE_URL}/wp/v2/media" \
  -u "${WP_USER}:${WP_PASS}" \
  -F "file=@${IMAGE_PATH}")

# Extract media ID
MEDIA_ID=$(echo "$RESPONSE" | jq -r '.id' 2>/dev/null)

if [[ -z "$MEDIA_ID" ]] || [[ "$MEDIA_ID" == "null" ]]; then
  echo -e "${RED}✗ Upload failed${NC}"
  echo "Response: $RESPONSE"
  exit 1
fi

echo -e "${GREEN}✓ Uploaded (Media ID: ${MEDIA_ID})${NC}"

# Add alt text and caption if provided
if [[ -n "$ALT_TEXT" ]] || [[ -n "$CAPTION" ]]; then
  echo -e "${YELLOW}Adding metadata...${NC}"

  META_DATA="{"
  if [[ -n "$ALT_TEXT" ]]; then
    META_DATA+="\"alt_text\": \"${ALT_TEXT}\""
  fi
  if [[ -n "$CAPTION" ]]; then
    if [[ -n "$ALT_TEXT" ]]; then
      META_DATA+=", "
    fi
    META_DATA+="\"caption\": \"${CAPTION}\""
  fi
  META_DATA+="}"

  UPDATE_RESPONSE=$(curl -s -X POST "${SITE_URL}/wp/v2/media/${MEDIA_ID}" \
    -u "${WP_USER}:${WP_PASS}" \
    -H "Content-Type: application/json" \
    -d "$META_DATA")

  if echo "$UPDATE_RESPONSE" | jq -e '.id' > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Metadata updated${NC}"
  else
    echo -e "${YELLOW}⚠ Warning: Failed to update metadata${NC}"
  fi
fi

# Set as featured image if post_id provided
if [[ -n "$POST_ID" ]]; then
  echo -e "${YELLOW}Setting as featured image for post ${POST_ID}...${NC}"

  FEATURED_RESPONSE=$(curl -s -X POST "${SITE_URL}/wp-json/wp/v2/posts/${POST_ID}" \
    -u "${WP_USER}:${WP_PASS}" \
    -H "Content-Type: application/json" \
    -d "{\"featured_media\": ${MEDIA_ID}}")

  if echo "$FEATURED_RESPONSE" | jq -e '.featured_media' > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Set as featured image${NC}"
  else
    echo -e "${YELLOW}⚠ Warning: Failed to set as featured image${NC}"
  fi
fi

echo ""
echo -e "${GREEN}✓ Done! Media ID: ${MEDIA_ID}${NC}"

exit 0
