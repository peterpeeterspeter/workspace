#!/bin/bash
# Pinch-to-Post Helper: Content Backup
# Export all content to markdown with metadata

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
  echo "Usage: $0 <backup_dir> [site]"
  echo ""
  echo "Example:"
  echo "  $0 /root/backups/2026-02-03"
  echo "  $0 /root/backups/2026-02-03 crashcasino"
  exit 1
}

# Check arguments
if [[ $# -lt 1 ]]; then
  usage
fi

BACKUP_DIR="$1"
SITE="${2:-all}"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Sites to backup
if [[ "$SITE" == "all" ]]; then
  SITES=("crashcasino" "crashgame" "freecrash" "cryptocrash")
else
  SITES=("$SITE")
fi

echo -e "${GREEN}=== Content Backup ===${NC}"
echo "Backup Directory: ${BACKUP_DIR}"
echo "Sites: ${SITES[*]}"
echo ""

for site in "${SITES[@]}"; do
  # Get site URL
  SITE_URL_VAR="WP_SITE_${site^^}_URL"
  SITE_URL="${!SITE_URL_VAR}"

  if [[ -z "$SITE_URL" ]]; then
    echo -e "${YELLOW}Warning: No URL configured for '${site}'${NC}"
    continue
  fi

  # Get credentials
  WP_USER="${WP_USERNAME:-peter}"
  WP_PASS="${WP_SITE_${site^^}_PASS}"

  echo -e "${YELLOW}[${site}]${NC} Backing up..."

  SITE_DIR="${BACKUP_DIR}/${site}"
  mkdir -p "${SITE_DIR}/posts"
  mkdir -p "${SITE_DIR}/pages"

  # Backup posts
  echo -e "  Exporting posts..."

  PAGE=1
  PER_PAGE=100
  TOTAL_POSTS=0

  while true; do
    POSTS=$(curl -s "${SITE_URL}/wp-json/wp/v2/posts?per_page=${PER_PAGE}&page=${PAGE}&status=publish" \
      -u "${WP_USER}:${WP_PASS}")

    COUNT=$(echo "$POSTS" | jq 'length' 2>/dev/null || echo "0")

    if [[ "$COUNT" -eq 0 ]]; then
      break
    fi

    while IFS= read -r post; do
      POST_ID=$(echo "$post" | jq -r '.id')
      POST_TITLE=$(echo "$post" | jq -r '.title.rendered' | sed 's/[\/:*?"<>|]/_/g')
      POST_SLUG=$(echo "$post" | jq -r '.slug')
      POST_DATE=$(echo "$post" | jq -r '.date')
      POST_CONTENT=$(echo "$post" | jq -r '.content.rendered')
      POST_EXCERPT=$(echo "$post" | jq -r '.excerpt.rendered')
      POST_LINK=$(echo "$post" | jq -r '.link')

      # Create markdown file with frontmatter
      cat > "${SITE_DIR}/posts/${POST_ID}-${POST_SLUG}.md" << EOF
---
id: ${POST_ID}
title: ${POST_TITLE}
slug: ${POST_SLUG}
date: ${POST_DATE}
link: ${POST_LINK}
excerpt: |
$(echo "$POST_EXCERPT" | sed 's/<[^>]*>//g')
---

# ${POST_TITLE}

$(echo "$POST_CONTENT" | sed 's/<[^>]*>//g')
EOF

      ((TOTAL_POSTS++))
    done < <(echo "$POSTS" | jq -c '.[]')

    ((PAGE++))
  done

  echo -e "  ${GREEN}✓ ${TOTAL_POSTS} posts exported${NC}"

  # Backup pages
  echo -e "  Exporting pages..."

  PAGE=1
  TOTAL_PAGES=0

  while true; do
    PAGES=$(curl -s "${SITE_URL}/wp-json/wp/v2/pages?per_page=${PER_PAGE}&page=${PAGE}" \
      -u "${WP_USER}:${WP_PASS}")

    COUNT=$(echo "$PAGES" | jq 'length' 2>/dev/null || echo "0")

    if [[ "$COUNT" -eq 0 ]]; then
      break
    fi

    while IFS= read -r page; do
      PAGE_ID=$(echo "$page" | jq -r '.id')
      PAGE_TITLE=$(echo "$page" | jq -r '.title.rendered' | sed 's/[\/:*?"<>|]/_/g')
      PAGE_SLUG=$(echo "$page" | jq -r '.slug')

      cat > "${SITE_DIR}/pages/${PAGE_ID}-${PAGE_SLUG}.md" << EOF
---
id: ${PAGE_ID}
title: ${PAGE_TITLE}
slug: ${PAGE_SLUG}
---

$(echo "$page" | jq -r '.content.rendered' | sed 's/<[^>]*>//g')
EOF

      ((TOTAL_PAGES++))
    done < <(echo "$PAGES" | jq -c '.[]')

    ((PAGE++))
  done

  echo -e "  ${GREEN}✓ ${TOTAL_PAGES} pages exported${NC}"

  # Backup categories
  echo -e "  Exporting categories..."

  curl -s "${SITE_URL}/wp-json/wp/v2/categories?per_page=100&hide_empty=false" \
    -u "${WP_USER}:${WP_PASS}" > "${SITE_DIR}/categories.json"

  echo -e "  ${GREEN}✓ Categories exported${NC}"

  # Backup tags
  echo -e "  Exporting tags..."

  curl -s "${SITE_URL}/wp-json/wp/v2/tags?per_page=100&hide_empty=false" \
    -u "${WP_USER}:${WP_PASS}" > "${SITE_DIR}/tags.json"

  echo -e "  ${GREEN}✓ Tags exported${NC}"
done

echo ""
echo -e "${GREEN}=== Backup Complete ===${NC}"
echo "Location: ${BACKUP_DIR}"

exit 0
