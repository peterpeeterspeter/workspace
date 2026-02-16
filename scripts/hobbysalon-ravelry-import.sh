#!/bin/bash

# Hobbysalon Ravelry Pattern Importer
# Imports patterns from JSON to WordPress with proper taxonomies
# Usage: ./hobbysalon-ravelry-import.sh [limit] [offset]

set +e

# Configuration
SITE="hobbysalon"
SOURCE_FILE="/root/.openclaw/workspace/research/ravelry_dutch_patterns.json"
LIMIT=${1:-10}
OFFSET=${2:-0}

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Load WordPress credentials
source /root/.openclaw/workspace/.env
WP_URL="${WORDPRESS_HOBBYSALON_URL}"
WP_USER="${WORDPRESS_HOBBYSALON_USER}"
WP_APP_PASS="${WORDPRESS_HOBBYSALON_APP_PASSWORD}"
AUTH_BASE64=$(echo -n "${WP_USER}:${WP_APP_PASS}" | base64)

# Logging
LOG_DIR="/root/.openclaw/workspace/logs"
mkdir -p "${LOG_DIR}"
LOG_FILE="${LOG_DIR}/hobbysalon-import-$(date +%Y%m%d).log"

log() {
  echo -e "$1" | tee -a "${LOG_FILE}"
}

detect_technique() {
  local pattern_name=$1
  if [[ "${pattern_name}" =~ [Hh]aak ]] || [[ "${pattern_name}" =~ [Cc]rochet ]]; then
    echo "haken"
  elif [[ "${pattern_name}" =~ [Bb]rei ]] || [[ "${pattern_name}" =~ [Kk]nit ]]; then
    echo "breien"
  elif [[ "${pattern_name}" =~ [Mm]acram ]]; then
    echo "macrame"
  else
    echo "haken"
  fi
}

map_thema() {
  local techniek=$1
  case "${techniek}" in
    haken|breien|macrame|quilten-borduren) echo "wol-naald" ;;
    kaarten-maken|scrapbooking|bullet-journaling|origami) echo "papier-pen" ;;
    juwelen|sieraden-beading) echo "kralen-draad" ;;
    naaien) echo "stof-steek" ;;
    bloemschikken) echo "bloemen-groen" ;;
    *) echo "wol-naald" ;;
  esac
}

import_patterns() {
  local limit=$1
  local offset=$2

  log "${BLUE}🧶 Hobbysalon Ravelry Pattern Importer${NC}"
  log "${BLUE}═══════════════════════════════════════════${NC}"
  log ""
  log "📊 Limit: ${limit}, Offset: ${offset}"
  log ""

  local tmp_dir=$(mktemp -d)
  echo "0" > "${tmp_dir}/imported"
  echo "0" > "${tmp_dir}/skipped"
  echo "0" > "${tmp_dir}/failed"

  jq -c ".[${offset}:$((${offset}+limit))][]" "${SOURCE_FILE}" | while read -r pattern; do
    PATTERN_ID=$(echo "${pattern}" | jq -r '.id // empty')
    [ -z "${PATTERN_ID}" ] && continue

    PATTERN_NAME=$(echo "${pattern}" | jq -r '.name // "Unknown"')
    DESIGNER=$(echo "${pattern}" | jq -r '.designer.name // "Unknown"')
    IS_FREE=$(echo "${pattern}" | jq -r '.free // false')
    PATTERN_URL=$(echo "${pattern}" | jq -r '.permalink // ""')
    PHOTO_URL=$(echo "${pattern}" | jq -r '.first_photo?.small_url // ""')
    DIFFICULTY=$(echo "${pattern}" | jq -r '.difficulty // ""')
    YARN_WEIGHT=$(echo "${pattern}" | jq -r '.yarn_weight?.name // ""')

    TECHNIEK=$(detect_technique "${PATTERN_NAME}")
    THEMA=$(map_thema "${TECHNIEK}")

    POST_TITLE="${PATTERN_NAME}"
    [ "${IS_FREE}" = "true" ] && POST_TITLE="Gratis: ${PATTERN_NAME}"

    # Build HTML content (no newlines, let WordPress wpautop handle it)
    POST_CONTENT="<p><strong>"
    if [ "${IS_FREE}" = "true" ]; then
      POST_CONTENT+="✅ Gratis patroon door ${DESIGNER}!</strong></p>"
    else
      POST_CONTENT+="Patroon door ${DESIGNER}!</strong></p>"
    fi

    POST_CONTENT+="<h3>Details</h3><ul><li><strong>Designer:</strong> ${DESIGNER}</li>"

    if [ -n "${DIFFICULTY}" ]; then
      POST_CONTENT+="<li><strong>Moeilijkheid:</strong> ${DIFFICULTY}</li>"
    fi

    if [ -n "${YARN_WEIGHT}" ]; then
      POST_CONTENT+="<li><strong>Garen:</strong> ${YARN_WEIGHT}</li>"
    fi

    POST_CONTENT+="</ul>"

    POST_CONTENT+="<h3>Bekijk Patroon</h3><p><a href=\"https://www.ravelry.com/patterns/library/${PATTERN_URL}\" target=\"_blank\" rel=\"nofollow sponsored\">Bekijk dit patroon op Ravelry →</a></p>"

    POST_CONTENT+="<h3>Tools</h3><p>Bereken hoeveel garn je nodig hebt met onze <a href=\"/tools/yardage-calculator/\">Yardage Calculator</a>. Ontdek wat je met je garen stash kunt maken met de <a href=\"/tools/stash-calculator/\">Stash Calculator</a>. Of bereken de kosten met de <a href=\"/tools/cost-calculator/\">Cost Calculator</a>.</p>"

    META_DESC="Gratis ${PATTERN_NAME} patroon door ${DESIGNER}."
    [ "${IS_FREE}" = "true" ] && META_DESC+=" Download nu op Ravelry. Inclusief materialenlijst en instructies."

    # Create post JSON
    POST_JSON=$(jq -n \
      --arg title "${POST_TITLE}" \
      --arg content "${POST_CONTENT}" \
      --arg excerpt "${META_DESC}" \
      --arg ravelry_id "${PATTERN_ID}" \
      --arg ravelry_designer "${DESIGNER}" \
      --arg ravelry_free "${IS_FREE}" \
      --arg ravelry_permalink "${PATTERN_URL}" \
      '{
        title: $title,
        content: $content,
        status: "draft",
        excerpt: $excerpt,
        meta: {
          ravelry_id: $ravelry_id,
          ravelry_designer: $ravelry_designer,
          ravelry_free: $ravelry_free,
          ravelry_permalink: $ravelry_permalink
        }
      }')

    log "${BLUE}📝 Creating post: ${POST_TITLE}${NC}"

    RESPONSE=$(curl -s -X POST \
      "${WP_URL}/wp/v2/posts" \
      -H "Authorization: Basic ${AUTH_BASE64}" \
      -H "Content-Type: application/json" \
      -d "${POST_JSON}")

    if echo "${RESPONSE}" | grep -q "code"; then
      log "${RED}❌ Failed${NC}"
      echo $(($(cat "${tmp_dir}/failed") + 1)) > "${tmp_dir}/failed"
      continue
    fi

    POST_ID=$(echo "${RESPONSE}" | jq -r '.id // empty')
    if [ -z "${POST_ID}" ] || [ "${POST_ID}" = "null" ]; then
      log "${RED}❌ No ID${NC}"
      echo $(($(cat "${tmp_dir}/failed") + 1)) > "${tmp_dir}/failed"
      continue
    fi

    log "${GREEN}✅ Created: ${POST_ID}${NC}"

    # Upload featured image
    if [ -n "${PHOTO_URL}" ]; then
      log "${BLUE}   📷 Uploading image...${NC}"
      IMAGE_DATA=$(curl -s "${PHOTO_URL}" 2>&1)

      if [ -n "${IMAGE_DATA}" ]; then
        MEDIA_RESPONSE=$(curl -s -X POST \
          "${WP_URL}/wp/v2/media" \
          -H "Authorization: Basic ${AUTH_BASE64}" \
          -H "Content-Disposition: attachment; filename=${PATTERN_ID}.jpg" \
          -H "Content-Type: image/jpeg" \
          --data-binary "${IMAGE_DATA}")

        FEATURED_ID=$(echo "${MEDIA_RESPONSE}" | jq -r '.id // empty')

        if [ -n "${FEATURED_ID}" ] && [ "${FEATURED_ID}" != "null" ]; then
          # Update alt text
          curl -s -X POST "${WP_URL}/wp/v2/media/${FEATURED_ID}" \
            -H "Authorization: Basic ${AUTH_BASE64}" \
            -H "Content-Type: application/json" \
            -d "{\"alt_text\": \"${POST_TITLE}\"}" > /dev/null

          # Attach to post
          curl -s -X POST "${WP_URL}/wp/v2/posts/${POST_ID}" \
            -H "Authorization: Basic ${AUTH_BASE64}" \
            -H "Content-Type: application/json" \
            -d "{\"featured_media\": ${FEATURED_ID}}" > /dev/null

          log "${GREEN}   ✅ Image: ${FEATURED_ID}${NC}"
        fi
      fi
    fi

    # Assign taxonomies
    log "${BLUE}   🏷️  Tax: ${THEMA} / ${TECHNIEK}${NC}"
    curl -s -X POST "${WP_URL}/wp/v2/posts/${POST_ID}" \
      -H "Authorization: Basic ${AUTH_BASE64}" \
      -H "Content-Type: application/json" \
      -d "{\"hs_thema\": \"${THEMA}\", \"hs_techniek\": \"${TECHNIEK}\"}" > /dev/null 2>&1

    echo $(($(cat "${tmp_dir}/imported") + 1)) > "${tmp_dir}/imported"
    log ""
  done

  local imported=$(cat "${tmp_dir}/imported")
  local skipped=$(cat "${tmp_dir}/skipped")
  local failed=$(cat "${tmp_dir}/failed")
  rm -rf "${tmp_dir}"

  log "${GREEN}✅ Import complete!${NC}"
  log "📊 Imported: ${imported}, Skipped: ${skipped}, Failed: ${failed}"
}

import_patterns $LIMIT $OFFSET
