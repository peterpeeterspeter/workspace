#!/bin/bash
# Fixed Ravelry to WordPress Import Script
# Uses Ravelry CDN images directly + better content

VERSION="2.0.0"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="/root/.openclaw/workspace"

# Config
RAVELRY_JSON="${WORKSPACE_DIR}/research/ravelry_dutch_patterns.json"
IMPORT_COUNT="${1:-5}"  # Default 5 patterns for test
SITE="hobbysalon"
POST_TYPE="post"
STATUS="draft"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🧶 Fixed Ravelry to WordPress Import v${VERSION}${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""
echo "Site: ${SITE}"
echo "Import limit: ${IMPORT_COUNT} patterns"
echo "Status: ${STATUS}"
echo ""

# Check if JSON exists
if [[ ! -f "${RAVELRY_JSON}" ]]; then
  echo -e "${RED}❌ Ravelry JSON not found at: ${RAVELRY_JSON}${NC}"
  exit 1
fi

# Site credentials (hobbysalon.be)
WP_URL="https://www.hobbysalon.be/wp-json"
WP_USER="kris"
WP_PASS="BAvt knyO ystE qYXk YQUo v9mu"

echo -e "${GREEN}✅ Connected to: ${WP_URL}${NC}"
echo ""

# Get first N patterns
PATTERNS=$(cat ${RAVELRY_JSON} | jq ".[:${IMPORT_COUNT}]")
PATTERN_COUNT=$(echo "${PATTERNS}" | jq 'length')

echo -e "${YELLOW}📦 Processing ${PATTERN_COUNT} patterns...${NC}"
echo ""

# Import counter
IMPORTED=0
FAILED=0

# Loop through patterns
for i in $(seq 0 $((${PATTERN_COUNT} - 1))); do
  PATTERN=$(echo "${PATTERNS}" | jq ".[${i}]")

  # Extract pattern data
  PATTERN_ID=$(echo "${PATTERN}" | jq -r '.id')
  PATTERN_NAME=$(echo "${PATTERN}" | jq -r '.name')
  DESIGNER=$(echo "${PATTERN}" | jq -r '.pattern_author.name // .designer.name // "Unknown"')
  IS_FREE=$(echo "${PATTERN}" | jq -r '.free // false')
  CRAFT=$(echo "${PATTERN}" | jq -r '.craft // "Unknown"')

  # Determine category
  if [[ "${CRAFT}" == "crochet" ]]; then
    CATEGORY_ID=39  # Haken
    CATEGORY_NAME="Haken"
    CRAFT_TYPE="haken"
  elif [[ "${CRAFT}" == "knitting" ]]; then
    CATEGORY_ID=101  # Breien
    CATEGORY_NAME="Breien"
    CRAFT_TYPE="breien"
  else
    CATEGORY_ID=39  # Default to Haken
    CATEGORY_NAME="Haken"
    CRAFT_TYPE="haken"
  fi

  # Price tag
  if [[ "${IS_FREE}" == "true" ]]; then
    PRICE="Gratis"
    PRICE_TAG="gratis"
  else
    PRICE="Betaald"
    PRICE_TAG="betaald"
  fi

  # Get image from Ravelry CDN
  IMAGE_URL=$(echo "${PATTERN}" | jq -r '.first_photo.medium_url // .first_photo.small_url // ""')

  # Ravelry pattern permalink
  RAVELRY_PERMALINK=$(echo "${PATTERN}" | jq -r '.permalink // ""')
  RAVELRY_URL="https://www.ravelry.com/patterns/library/${RAVELRY_PERMALINK}"

  # Generate post title
  POST_TITLE="${PRICE}: ${PATTERN_NAME}"

  # Generate meta description
  META_DESC="${PRICE} ${PATTERN_NAME} ${CRAFT_TYPE}patroon van ${DESIGNER}. Download nu op Ravelry. Inclusief materialenlijst en instructies."

  # Generate content with Ravelry CDN image
  if [[ -n "${IMAGE_URL}" ]]; then
    CONTENT="<p><strong>✅ ${PRICE} patroon door ${DESIGNER}!</strong></p>

<p><img src=\"${IMAGE_URL}\" alt=\"${POST_TITLE}\" /></p>

<h3>Details</h3>
<ul>
<li><strong>Designer:</strong> ${DESIGNER}</li>
<li><strong>Type:</strong> ${CATEGORY_NAME}</li>
<li><strong>Prijs:</strong> ${PRICE}</li>
</ul>

<h3>Bekijk Patroon</h3>
<p><a href=\"${RAVELRY_URL}\" target=\"_blank\" rel=\"nofollow noopener\">Bekijk dit patroon op Ravelry →</a></p>

<h3>Tools</h3>
<p>Bereken hoeveel garen je nodig hebt met onze <a href=\"/tools/yardage-calculator/\">Yardage Calculator</a>. Ontdek wat je met je garen stash kunt maken met de <a href=\"/tools/stash-calculator/\">Stash Calculator</a>. Of bereken de kosten met de <a href=\"/tools/cost-calculator/\">Cost Calculator</a>.</p>"
  else
    CONTENT="<p><strong>✅ ${PRICE} patroon door ${DESIGNer}!</strong></p>

<h3>Details</h3>
<ul>
<li><strong>Designer:</strong> ${DESIGNER}</li>
<li><strong>Type:</strong> ${CATEGORY_NAME}</li>
<li><strong>Prijs:</strong> ${PRICE}</li>
</ul>

<h3>Bekijk Patroon</h3>
<p><a href=\"${RAVELRY_URL}\" target=\"_blank\" rel=\"nofollow noopener\">Bekijk dit patroon op Ravelry →</a></p>"
  fi

  # Create post via REST API
  echo -e "${BLUE}Creating post: ${POST_TITLE}${NC}"
  echo "  Designer: ${DESIGNER}"
  echo "  Category: ${CATEGORY_NAME}"
  echo "  Image: ${IMAGE_URL}"

  # Build JSON payload using jq for proper escaping
  JSON_PAYLOAD=$(jq -n \
    --arg title "${POST_TITLE}" \
    --arg content "${CONTENT}" \
    --arg excerpt "${META_DESC}" \
    --arg status "${STATUS}" \
    '{
      title: $title,
      content: $content,
      excerpt: $excerpt,
      status: $status,
      comment_status: "closed",
      ping_status: "closed"
    }')

  RESPONSE=$(curl -s -X POST "${WP_URL}/wp/v2/posts" \
    -u "${WP_USER}:${WP_PASS}" \
    -H "Content-Type: application/json" \
    -d "${JSON_PAYLOAD}")

  # Check response
  POST_ID=$(echo "${RESPONSE}" | jq -r '.id // empty')

  if [[ -n "${POST_ID}" && "${POST_ID}" != "null" ]]; then
    echo -e "${GREEN}  ✅ Created: Post ID ${POST_ID}${NC}"
    ((IMPORTED++))
  else
    echo -e "${RED}  ❌ Failed to create post${NC}"
    echo "  Response: ${RESPONSE}"
    ((FAILED++))
  fi

  echo ""
done

# Summary
echo -e "${BLUE}============================================${NC}"
echo -e "${GREEN}✅ Import Complete!${NC}"
echo ""
echo "Imported: ${IMPORTED}"
echo "Failed: ${FAILED}"
echo ""
echo "Next steps:"
echo "1. Review posts at ${WP_URL}/wp-admin/edit.php"
echo "2. Check images display correctly"
echo "3. Verify categories assigned"
echo "4. Publish when ready"
