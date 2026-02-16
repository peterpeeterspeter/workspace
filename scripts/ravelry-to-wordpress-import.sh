#!/bin/bash
# Ravelry to WordPress Import Script
# Imports Ravelry patterns from JSON and creates WordPress posts

set -e

VERSION="1.0.0"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="/root/.openclaw/workspace"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Config
RAVELRY_JSON="${WORKSPACE_DIR}/research/ravelry_dutch_patterns.json"
SITE="${1:-crashcasino}"  # Default site, can override
POST_TYPE="${2:-post}"    # 'post' or custom post type
IMPORT_LIMIT="${3:-50}"   # Number of patterns to import

echo -e "${BLUE}🧶 Ravelry to WordPress Import v${VERSION}${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""
echo "Site: ${SITE}"
echo "Post Type: ${POST_TYPE}"
echo "Import Limit: ${IMPORT_LIMIT} patterns"
echo ""

# Check if JSON exists
if [[ ! -f "${RAVELRY_JSON}" ]]; then
  echo -e "${YELLOW}⚠️  Ravelry JSON not found at: ${RAVELRY_JSON}${NC}"
  exit 1
fi

# Load site credentials
source "${WORKSPACE_DIR}/scripts/pinch-to-post-helpers/get-site-creds.sh"

# Get credentials for site
case "$SITE" in
  crashcasino)
    WP_URL="${WP_SITE_1_URL:-https://crashcasino.io}"
    WP_USER="${WP_SITE_1_USER}"
    WP_PASS="${WP_SITE_1_PASS}"
    ;;
  crashgame)
    WP_URL="${WP_SITE_2_URL:-https://crashgamegambling.com}"
    WP_USER="${WP_SITE_2_USER}"
    WP_PASS="${WP_SITE_2_PASS}"
    ;;
  freecrash)
    WP_URL="${WP_SITE_3_URL:-https://freecrashgames.com}"
    WP_USER="${WP_SITE_3_USER}"
    WP_PASS="${WP_SITE_3_PASS}"
    ;;
  cryptocrash)
    WP_URL="${WP_SITE_4_URL:-https://cryptocrashgambling.com}"
    WP_USER="${WP_SITE_4_USER}"
    WP_PASS="${WP_SITE_4_PASS}"
    ;;
  *)
    echo -e "${YELLOW}⚠️  Unknown site: ${SITE}${NC}"
    echo "Available sites: crashcasino, crashgame, freecrash, cryptocrash"
    exit 1
    ;;
esac

if [[ -z "${WP_USER}" || -z "${WP_PASS}" ]]; then
  echo -e "${YELLOW}⚠️  WordPress credentials not configured for ${SITE}${NC}"
  echo "Set ${SITE}_WP_USER and ${SITE}_WP_PASS in ~/.openclaw/workspace/.env"
  exit 1
fi

echo -e "${GREEN}✅ Connected to: ${WP_URL}${NC}"
echo ""

# Count total patterns
TOTAL_PATTERNS=$(jq '. | length' "${RAVELRY_JSON}")
echo -e "${BLUE}📊 Total patterns in JSON: ${TOTAL_PATTERNS}${NC}"
echo -e "${BLUE}📥 Importing: ${IMPORT_LIMIT} patterns${NC}"
echo ""

# Import counter
IMPORTED=0
UPDATED=0
SKIPPED=0
ERRORS=0

# Process patterns
jq -c '.[:'"${IMPORT_LIMIT}"']' "${RAVELRY_JSON}" | while IFS= read -r pattern; do
  PATTERN_ID=$(echo "${pattern}" | jq -r '.id')
  PATTERN_NAME=$(echo "${pattern}" | jq -r '.name')
  DESIGNER=$(echo "${pattern}" | jq -r '.designer.name // .pattern_author.name // "Unknown"')
  PERMALINK=$(echo "${pattern}" | jq -r '.permalink')
  IS_FREE=$(echo "${pattern}" | jq -r '.free // false')
  PHOTO_URL=$(echo "${pattern}" | jq -r '.first_photo.medium_url // empty')

  # Build post content
  POST_CONTENT=""

  if [[ "${IS_FREE}" == "true" ]]; then
    POST_CONTENT="${POST_CONTENT}<p><strong>✅ Gratis patroon!</strong></p>"
  fi

  POST_CONTENT="${POST_CONTENT}
<h3>Details</h3>
<ul>
<li><strong>Designer:</strong> ${DESIGNER}</li>
<li><strong>Type:</strong> Breien/Haken</li>
</ul>

<h3>Bekijk Patroon</h3>
<p><a href=\"https://www.ravelry.com/patterns/library/${PERMALINK}\" target=\"_blank\" rel=\"nofollow\">Bekijk dit patroon op Ravelry →</a></p>
"

  # Add calculator (if installed)
  POST_CONTENT="${POST_CONTENT}
<h3>Bereken Garen</h3>
<p>Gebruik onze <a href=\"/stash-calculator/\">Stash Calculator</a> om te zien wat je met je garen kunt maken!</p>
"

  # Build post title
  POST_TITLE="${PATTERN_NAME}"
  if [[ "${IS_FREE}" == "true" ]]; then
    POST_TITLE="Gratis: ${POST_TITLE}"
  fi

  # Check if post already exists (by meta field)
  EXISTING_POST=$(curl -s -u "${WP_USER}:${WP_PASS}" \
    "${WP_URL}/wp-json/wp/v2/${POST_TYPE}?slug=${PERMALINK}&_fields=id" | jq -r '.[0].id // empty')

  if [[ -n "${EXISTING_POST}" && "${EXISTING_POST}" != "null" ]]; then
    echo -e "${YELLOW}↻  Updating: ${POST_TITLE} (ID: ${EXISTING_POST})${NC}"

    # Update existing post
    UPDATE_RESPONSE=$(curl -s -X POST -u "${WP_USER}:${WP_PASS}" \
      "${WP_URL}/wp-json/wp/v2/${POST_TYPE}/${EXISTING_POST}" \
      -H "Content-Type: application/json" \
      -d "{
        \"title\": \"${POST_TITLE}\",
        \"content\": \"${POST_CONTENT}\",
        \"status\": \"draft\",
        \"meta\": {
          \"ravelry_id\": \"${PATTERN_ID}\",
          \"ravelry_designer\": \"${DESIGNER}\",
          \"ravelry_free\": \"${IS_FREE}\"
        }
      }")

    if echo "${UPDATE_RESPONSE}" | jq -e '.id' > /dev/null; then
      ((UPDATED++))
      echo -e "${GREEN}✅ Updated: ${POST_TITLE}${NC}"
    else
      ((ERRORS++))
      echo -e "${YELLOW}⚠️  Update failed: ${POST_TITLE}${NC}"
    fi

  else
    echo -e "${BLUE}➕ Creating: ${POST_TITLE}${NC}"

    # Create new post
    CREATE_RESPONSE=$(curl -s -X POST -u "${WP_USER}:${WP_PASS}" \
      "${WP_URL}/wp-json/wp/v2/${POST_TYPE}" \
      -H "Content-Type: application/json" \
      -d "{
        \"title\": \"${POST_TITLE}\",
        \"content\": \"${POST_CONTENT}\",
        \"status\": \"draft\",
        \"slug\": \"${PERMALINK}\",
        \"meta\": {
          \"ravelry_id\": \"${PATTERN_ID}\",
          \"ravelry_designer\": \"${DESIGNER}\",
          \"ravelry_free\": \"${IS_FREE}\"
        }
      }")

    NEW_POST_ID=$(echo "${CREATE_RESPONSE}" | jq -r '.id // empty')

    if [[ -n "${NEW_POST_ID}" && "${NEW_POST_ID}" != "null" ]]; then
      ((IMPORTED++))
      echo -e "${GREEN}✅ Created: ${POST_TITLE} (ID: ${NEW_POST_ID})${NC}"

      # Download and set featured image
      if [[ -n "${PHOTO_URL}" ]]; then
        echo -e "${BLUE}   📷 Downloading featured image...${NC}"

        # Download image
        IMAGE_FILE="/tmp/ravelry_${PATTERN_ID}.jpg"
        curl -s "${PHOTO_URL}" -o "${IMAGE_FILE}"

        # Upload to WordPress
        MEDIA_RESPONSE=$(curl -s -X POST -u "${WP_USER}:${WP_PASS}" \
          "${WP_URL}/wp-json/wp/v2/media" \
          -F "file=@${IMAGE_FILE}" \
          -F "caption=${PATTERN_NAME}" \
          -F "alt_text=${POST_TITLE}")

        MEDIA_ID=$(echo "${MEDIA_RESPONSE}" | jq -r '.id // empty')

        if [[ -n "${MEDIA_ID}" && "${MEDIA_ID}" != "null" ]]; then
          # Set as featured image
          curl -s -X POST -u "${WP_USER}:${WP_PASS}" \
            "${WP_URL}/wp-json/wp/v2/${POST_TYPE}/${NEW_POST_ID}" \
            -H "Content-Type: application/json" \
            -d "{\"featured_media\": ${MEDIA_ID}}" > /dev/null

          echo -e "${GREEN}   ✅ Featured image set (Media ID: ${MEDIA_ID})${NC}"
        else
          echo -e "${YELLOW}   ⚠️  Failed to upload image${NC}"
        fi

        # Clean up temp file
        rm -f "${IMAGE_FILE}"
      fi

    else
      ((ERRORS++))
      echo -e "${YELLOW}⚠️  Create failed: ${POST_TITLE}${NC}"
    fi
  fi

  echo ""
done

# Summary
echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}📊 Import Summary${NC}"
echo -e "${BLUE}======================================${NC}"
echo -e "${GREEN}✅ Imported: ${IMPORTED}${NC}"
echo -e "${YELLOW}↻  Updated: ${UPDATED}${NC}"
echo -e "${YELLOW}⊘ Skipped: ${SKIPPED}${NC}"
echo -e "${YELLOW}⚠️  Errors: ${ERRORS}${NC}"
echo ""

# Next steps
if [[ ${IMPORTED} -gt 0 || ${UPDATED} -gt 0 ]]; then
  echo -e "${BLUE}🚀 Next Steps:${NC}"
  echo ""
  echo "1. Review imported posts:"
  echo "   ${WP_URL}/wp-admin/edit.php?post_type=${POST_TYPE}&post_status=draft"
  echo ""
  echo "2. Use pinch-to-post to publish:"
  echo "   pinch-to-post publish ${SITE} <post_id>"
  echo ""
  echo "3. Or bulk publish all imported patterns:"
  echo "   pinch-to-post bulk-publish ${SITE} <id_range>"
  echo ""
fi
