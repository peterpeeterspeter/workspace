#!/bin/bash
# Test Ravelry import to hobbysalon.be
# Small batch of 5 patterns for testing

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="/root/.openclaw/workspace"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🧶 Testing Ravelry Import to hobbysalon.be${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""

# Site config
SITE="hobbysalon"
WP_URL="https://www.hobbysalon.be"
WP_USER="kris"
WP_PASS="yiN7vXcZ2U2Tt2SM4DZX1mKw"
IMPORT_LIMIT=5

echo "Site: ${WP_URL}"
echo "Import: ${IMPORT_LIMIT} patterns (test batch)"
echo ""

# Test connection
echo -e "${BLUE}1. Testing WordPress connection...${NC}"
TEST_USER=$(curl -sL -u "${WP_USER}:${WP_PASS}" "${WP_URL}/wp-json/wp/v2/users/me" | jq -r '.name // empty')

if [[ "${TEST_USER}" == "Kris" ]]; then
  echo -e "${GREEN}✅ Connected as: ${TEST_USER}${NC}"
else
  echo -e "${YELLOW}⚠️  Connection failed${NC}"
  exit 1
fi

echo ""

# Check Ravelry JSON
RAVELRY_JSON="${WORKSPACE_DIR}/research/ravelry_dutch_patterns.json"
if [[ ! -f "${RAVELRY_JSON}" ]]; then
  echo -e "${YELLOW}⚠️  Ravelry JSON not found${NC}"
  exit 1
fi

TOTAL_PATTERNS=$(jq '. | length' "${RAVELRY_JSON}")
echo -e "${BLUE}2. Ravelry patterns available: ${TOTAL_PATTERNS}${NC}"
echo ""

# Import patterns
echo -e "${BLUE}3. Importing ${IMPORT_LIMIT} patterns...${NC}"
echo ""

IMPORTED=0

jq -c '.[:'"${IMPORT_LIMIT}"']' "${RAVELRY_JSON}" | while IFS= read -r pattern; do
  PATTERN_ID=$(echo "${pattern}" | jq -r '.id // empty')
  PATTERN_NAME=$(echo "${pattern}" | jq -r '.name // empty')
  DESIGNER=$(echo "${pattern}" | jq -r '.designer.name // .pattern_author.name // "Unknown"')
  PERMALINK=$(echo "${pattern}" | jq -r '.permalink // empty')
  IS_FREE=$(echo "${pattern}" | jq -r '.free // false')
  PHOTO_URL=$(echo "${pattern}" | jq -r '.first_photo.medium_url // empty')

  # Build content
  POST_CONTENT="<p><strong>${DESIGNER}</strong></p>"

  if [[ "${IS_FREE}" == "true" ]]; then
    POST_CONTENT="<p>✅ <strong>Gratis patroon!</strong></p>${POST_CONTENT}"
  fi

  POST_CONTENT="${POST_CONTENT}
<p><a href=\"https://www.ravelry.com/patterns/library/${PERMALINK}\" target=\"_blank\" rel=\"nofollow\">Bekijk dit patroon op Ravelry →</a></p>
"

  # Build title
  POST_TITLE="${PATTERN_NAME}"
  if [[ "${IS_FREE}" == "true" ]]; then
    POST_TITLE="Gratis: ${POST_TITLE}"
  fi

  # Create post
  echo -e "${BLUE}   Creating: ${POST_TITLE}${NC}"

  CREATE_RESPONSE=$(curl -sL -X POST -u "${WP_USER}:${WP_PASS}" \
    "${WP_URL}/wp-json/wp/v2/posts" \
    -H "Content-Type: application/json" \
    -d '{
      "title": "'"${POST_TITLE}"'",
      "content": "'"${POST_CONTENT}"'",
      "status": "draft",
      "slug": "'"${PERMALINK}"'"
    }')

  NEW_POST_ID=$(echo "${CREATE_RESPONSE}" | jq -r '.id // empty')

  if [[ -n "${NEW_POST_ID}" && "${NEW_POST_ID}" != "null" ]]; then
    ((IMPORTED++))
    echo -e "${GREEN}   ✅ Created: ${POST_TITLE} (ID: ${NEW_POST_ID})${NC}"

    # Download and set featured image
    if [[ -n "${PHOTO_URL}" ]]; then
      IMAGE_FILE="/tmp/ravelry_${PATTERN_ID}.jpg"
      curl -s "${PHOTO_URL}" -o "${IMAGE_FILE}"

      MEDIA_RESPONSE=$(curl -sL -X POST -u "${WP_USER}:${WP_PASS}" \
        "${WP_URL}/wp-json/wp/v2/media" \
        -F "file=@${IMAGE_FILE}")

      MEDIA_ID=$(echo "${MEDIA_RESPONSE}" | jq -r '.id // empty')

      if [[ -n "${MEDIA_ID}" && "${MEDIA_ID}" != "null" ]]; then
        curl -sL -X POST -u "${WP_USER}:${WP_PASS}" \
          "${WP_URL}/wp-json/wp/v2/posts/${NEW_POST_ID}" \
          -H "Content-Type: application/json" \
          -d '{"featured_media": '"${MEDIA_ID}"'}' > /dev/null

        echo -e "${GREEN}      📷 Featured image set${NC}"
      fi

      rm -f "${IMAGE_FILE}"
    fi
  else
    echo -e "${YELLOW}   ⚠️  Failed: ${POST_TITLE}${NC}"
    echo "${CREATE_RESPONSE}" | jq -r '.message // .code // empty'
  fi

  echo ""
done

# Summary
echo -e "${BLUE}============================================${NC}"
echo -e "${GREEN}✅ Test import complete!${NC}"
echo -e "${GREEN}✅ Imported: ${IMPORTED}/${IMPORT_LIMIT} patterns${NC}"
echo ""
echo -e "${BLUE}View drafts:${NC}"
echo "https://www.hobbysalon.be/wp-admin/edit.php?post_status=draft"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "1. Review the ${IMPORTED} imported patterns"
echo "2. Edit if needed"
echo "3. Publish when ready"
echo ""
