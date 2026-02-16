#!/bin/bash
# Ravelry to WordPress Complete Workflow
# Import → Quality Check → Publish

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="/root/.openclaw/workspace"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🧶 Ravelry → WordPress Complete Workflow${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Parameters
SITE="${1:-crashcasino}"
IMPORT_LIMIT="${2:-20}"
PUBLISH="${3:-false}"

echo "Site: ${SITE}"
echo "Import Limit: ${IMPORT_LIMIT} patterns"
echo "Auto Publish: ${PUBLISH}"
echo ""

# Step 1: Import Ravelry patterns
echo -e "${BLUE}📥 Step 1: Importing Ravelry Patterns...${NC}"
echo ""

"${WORKSPACE_DIR}/scripts/ravelry-to-wordpress-import.sh" "${SITE}" "post" "${IMPORT_LIMIT}"

if [[ $? -ne 0 ]]; then
  echo -e "${YELLOW}⚠️  Import failed. Aborting workflow.${NC}"
  exit 1
fi

echo ""
echo -e "${GREEN}✅ Import complete!${NC}"
echo ""

# Step 2: Get imported post IDs
echo -e "${BLUE}🔍 Step 2: Finding Imported Posts...${NC}"
echo ""

# Get site credentials
source "${WORKSPACE_DIR}/scripts/pinch-to-post-helpers/get-site-creds.sh"

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
esac

# Get draft posts with ravelry meta
DRAFT_POSTS=$(curl -s -u "${WP_USER}:${WP_PASS}" \
  "${WP_URL}/wp-json/wp/v2/posts?status=draft&per_page=100&meta_key=ravelry_id" | \
  jq -r '.[].id')

POST_COUNT=$(echo "${DRAFT_POSTS}" | wc -w)

echo -e "${GREEN}✅ Found ${POST_COUNT} imported pattern posts${NC}"
echo ""

# Step 3: Quality check
echo -e "${BLUE}🔍 Step 3: Running Quality Checks...${NC}"
echo ""

PASS_SCORE=0
FAIL_SCORE=0

for POST_ID in ${DRAFT_POSTS}; do
  echo -e "${BLUE}   Checking post ${POST_ID}...${NC}"

  # Use pinch-to-post health check
  "${WORKSPACE_DIR}/scripts/pinch-to-post.sh" health-check "${SITE}" "${POST_ID}" > /dev/null 2>&1

  if [[ $? -eq 0 ]]; then
    ((PASS_SCORE++))
    echo -e "${GREEN}   ✅ ${POST_ID}: Quality OK${NC}"
  else
    ((FAIL_SCORE++))
    echo -e "${YELLOW}   ⚠️  ${POST_ID}: Needs improvement${NC}"
  fi
done

echo ""
echo -e "${BLUE}📊 Quality Summary:${NC}"
echo -e "${GREEN}✅ Ready to publish: ${PASS_SCORE}${NC}"
echo -e "${YELLOW}⚠️  Needs work: ${FAIL_SCORE}${NC}"
echo ""

# Step 4: Publish (if requested)
if [[ "${PUBLISH}" == "true" && ${PASS_SCORE} -gt 0 ]]; then
  echo -e "${BLUE}🚀 Step 4: Publishing Quality Posts...${NC}"
  echo ""

  # Publish posts that passed quality check
  for POST_ID in ${DRAFT_POSTS}; do
    "${WORKSPACE_DIR}/scripts/pinch-to-post.sh" health-check "${SITE}" "${POST_ID}" > /dev/null 2>&1
    if [[ $? -eq 0 ]]; then
      echo -e "${BLUE}   Publishing ${POST_ID}...${NC}"
      "${WORKSPACE_DIR}/scripts/pinch-to-post.sh" publish "${SITE}" "${POST_ID}"
      echo -e "${GREEN}   ✅ Published: ${POST_ID}${NC}"
    fi
  done

  echo ""
  echo -e "${GREEN}✅ Publishing complete!${NC}"
elif [[ ${PASS_SCORE} -gt 0 ]]; then
  echo -e "${BLUE}📋 Next Steps:${NC}"
  echo ""
  echo "To publish quality posts, run:"
  echo "  pinch-to-post bulk-publish ${SITE} $(echo ${DRAFT_POSTS} | tr ' ' ',')"
  echo ""
  echo "Or publish individually:"
  echo "  pinch-to-post publish ${SITE} <post_id>"
  echo ""
fi

# Step 5: Calendar view
echo -e "${BLUE}📅 Step 5: Updated Publishing Calendar${NC}"
echo ""

"${WORKSPACE_DIR}/scripts/pinch-to-post.sh" calendar "$(date +%Y-%m)" "${SITE}"

echo ""
echo -e "${GREEN}✅ Workflow complete!${NC}"
