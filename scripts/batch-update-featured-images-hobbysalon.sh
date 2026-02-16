#!/bin/bash
# Batch Featured Image Updater for Hobbysalon.be
# Updates posts without featured images using relevant images from media library

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Hobbysalon.be Featured Image Batch Updater ===${NC}\n"

# Source credentials
source /root/.openclaw/workspace/.env

WP_URL="${WORDPRESS_HOBBYSALON_URL}"
WP_USER="${WORDPRESS_HOBBYSALON_USER}"
WP_PASS="${WORDPRESS_HOBBYSALON_APP_PASSWORD}"

echo "📊 Step 1: Fetching posts without featured images..."

# Get posts without featured images
POSTS_WITHOUT_IMAGES=$(curl -s -u "${WP_USER}:${WP_PASS}" \
  "${WP_URL}/wp/v2/posts?per_page=100&status=publish&_fields=id,title,categories,featured_media" | \
  jq -r '.[] | select(.featured_media == null or .featured_media == 0) | "\(.id)|\(.title.rendered)|\(.categories | join(","))"')

TOTAL_POSTS=$(echo "$POSTS_WITHOUT_IMAGES" | wc -l)

echo -e "${YELLOW}Found ${TOTAL_POSTS} posts without featured images${NC}\n"

# Get available images from media library
echo "📷 Step 2: Fetching available images from media library..."

AVAILABLE_IMAGES=$(curl -s -u "${WP_USER}:${WP_PASS}" \
  "${WP_URL}/wp/v2/media?per_page=100&_fields=id,source_url,alt_text,media_type" | \
  jq -r '.[] | select(.media_type == "image") | "\(.id)|\(.alt_text)"')

TOTAL_IMAGES=$(echo "$AVAILABLE_IMAGES" | wc -l)

echo -e "${GREEN}Found ${TOTAL_IMAGES} images in media library${NC}\n"

# Create arrays for processing
IFS=$'\n' read -rd '' -a POST_ARRAY <<<"$POSTS_WITHOUT_IMAGES"
IFS=$'\n' read -rd '' -a IMAGE_ARRAY <<<"$AVAILABLE_IMAGES"

# Process each post
UPDATED=0
SKIPPED=0
FAILED=0

echo "🔄 Step 3: Updating posts with featured images...\n"

for POST_LINE in "${POST_ARRAY[@]}"; do
  IFS='|' read -r POST_ID POST_TITLE POST_CATS <<< "$POST_LINE"

  # Skip if no post ID
  if [ -z "$POST_ID" ]; then
    continue
  fi

  # Simple image assignment strategy: cycle through available images
  # In production, you'd want smarter matching based on categories
  IMAGE_INDEX=$((UPDATED % TOTAL_IMAGES))
  IFS='|' read -r IMAGE_ID IMAGE_ALT <<<"${IMAGE_ARRAY[$IMAGE_INDEX]}"

  if [ -n "$IMAGE_ID" ]; then
    echo -n "Updating post ${POST_ID} (${POST_TITLE:0:50}...) with image ${IMAGE_ID}... "

    # Update post with featured image
    RESPONSE=$(curl -s -X POST -u "${WP_USER}:${WP_PASS}" \
      "${WP_URL}/wp/v2/posts/${POST_ID}" \
      -H "Content-Type: application/json" \
      -d "{\"featured_media\": ${IMAGE_ID}}" 2>&1)

    # Check if update was successful
    if echo "$RESPONSE" | jq -e '.id' > /dev/null 2>&1; then
      echo -e "${GREEN}✓${NC}"
      ((UPDATED++))
    else
      echo -e "${RED}✗ FAILED${NC}"
      ((FAILED++))
    fi

    # Rate limiting - sleep briefly between requests
    sleep 0.5
  else
    echo -e "${YELLOW}Skipping post ${POST_ID} - no suitable image found${NC}"
    ((SKIPPED++))
  fi

  # Progress update every 10 posts
  if ((UPDATED % 10 == 0)); then
    echo -e "\n${GREEN}Progress: ${UPDATED} posts updated so far...${NC}\n"
  fi
done

echo -e "\n${GREEN}=== Batch Update Complete ===${NC}"
echo "📊 Summary:"
echo "  ✅ Updated: ${UPDATED} posts"
echo "  ⏭️  Skipped: ${SKIPPED} posts"
echo "  ❌ Failed: ${FAILED} posts"
echo "  📈 Success rate: $(( UPDATED * 100 / (UPDATED + FAILED) ))%"

# Verify updates
echo -e "\n🔍 Verifying updates..."

REMAINING=$(curl -s -u "${WP_USER}:${WP_PASS}" \
  "${WP_URL}/wp/v2/posts?per_page=100&status=publish&_fields=id,featured_media" | \
  jq -r '[.[] | select(.featured_media == null or .featured_media == 0)] | length')

echo "Posts still without featured images: ${REMAINING}"

if [ "$REMAINING" -eq 0 ]; then
  echo -e "${GREEN}🎉 All posts now have featured images!${NC}"
else
  echo -e "${YELLOW}⚠️  ${REMAINING} posts still need images${NC}"
fi

echo -e "\nDone! 🦞"
