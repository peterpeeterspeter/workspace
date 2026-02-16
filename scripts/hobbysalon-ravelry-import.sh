#!/bin/bash

# Hobbysalon Ravelry Pattern Importer
# Imports patterns from JSON to WordPress with proper taxonomies
# Usage: ./hobbysalon-ravelry-import.sh [limit] [offset]

set -e

# Configuration
SITE="hobbysalon"
SOURCE_FILE="/root/.openclaw/workspace/research/ravelry_dutch_patterns.json"
LIMIT=${1:-10}  # Default 10 patterns per batch
OFFSET=${2:-0}
POST_TYPE="post"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Load WordPress credentials
if [ -f "/root/.openclaw/workspace/.env" ]; then
  source /root/.openclaw/workspace/.env
else
  echo -e "${RED}❌ Error: .env file not found${NC}"
  exit 1
fi

# Validate credentials
if [ -z "${WORDPRESS_HOBBYSALON_URL}" ] || [ -z "${WORDPRESS_HOBBYSALON_USER}" ] || [ -z "${WORDPRESS_HOBBYSALON_APP_PASSWORD}" ]; then
  echo -e "${RED}❌ Error: WordPress credentials not set in .env${NC}"
  echo "Required variables:"
  echo "  - WORDPRESS_HOBBYSALON_URL"
  echo "  - WORDPRESS_HOBBYSALON_USER"
  echo "  - WORDPRESS_HOBBYSALON_APP_PASSWORD"
  exit 1
fi

WP_URL="${WORDPRESS_HOBBYSALON_URL}"
WP_USER="${WORDPRESS_HOBBYSALON_USER}"
WP_APP_PASS="${WORDPRESS_HOBBYSALON_APP_PASSWORD}"

# Auth header (Basic Auth)
AUTH_BASE64=$(echo -n "${WP_USER}:${WP_APP_PASS}" | base64)

# Validate source file
if [ ! -f "${SOURCE_FILE}" ]; then
  echo -e "${RED}❌ Error: Ravelry JSON file not found: ${SOURCE_FILE}${NC}"
  exit 1
fi

# Check if jq is installed
if ! command -v jq &> /dev/null; then
  echo -e "${RED}❌ Error: jq is not installed${NC}"
  echo "Install with: apt-get install jq"
  exit 1
fi

# Logging
LOG_DIR="/root/.openclaw/workspace/logs"
mkdir -p "${LOG_DIR}"
LOG_FILE="${LOG_DIR}/hobbysalon-import-$(date +%Y%m%d).log"

# Functions
log() {
  echo -e "$1" | tee -a "${LOG_FILE}"
}

detect_technique() {
  local pattern_name=$1
  local pattern_tags=$2
  
  # Detect from name or tags
  if [[ "${pattern_name}" =~ [Hh]aak ]] || [[ "${pattern_name}" =~ [Cc]rochet ]] || echo "${pattern_tags}" | grep -iq "crochet"; then
    echo "haken"
  elif [[ "${pattern_name}" =~ [Bb]rei ]] || [[ "${pattern_name}" =~ [Kk]nit ]] || echo "${pattern_tags}" | grep -iq "knit"; then
    echo "breien"
  elif [[ "${pattern_name}" =~ [Mm]acram ]]; then
    echo "macrame"
  else
    # Default to haken for now
    echo "haken"
  fi
}

map_thema() {
  local techniek=$1
  
  case "${techniek}" in
    haken|breien|macrame|quilten-borduren)
      echo "wol-naald"
      ;;
    kaarten-maken|scrapbooking|bullet-journaling|origami)
      echo "papier-pen"
      ;;
    juwelen|sieraden-beading)
      echo "kralen-draad"
      ;;
    naaien)
      echo "stof-steek"
      ;;
    bloemschikken)
      echo "bloemen-groen"
      ;;
    *)
      echo "wol-naald"  # Default
      ;;
  esac
}

sanitize_content() {
  local content=$1
  # Remove null bytes
  echo "${content}" | tr -d '\000'
}

import_patterns() {
  local limit=$1
  local offset=$2
  
  log "${BLUE}🧶 Hobbysalon Ravelry Pattern Importer${NC}"
  log "${BLUE}═══════════════════════════════════════════${NC}"
  log ""
  log "📊 Configuration:"
  log "   Source: ${SOURCE_FILE}"
  log "   Limit: ${limit} patterns"
  log "   Offset: ${offset}"
  log "   Site: ${SITE}"
  log "   URL: ${WP_URL}"
  log ""
  
  # Count total patterns
  TOTAL_PATTERNS=$(jq '.patterns | length' "${SOURCE_FILE}")
  log "📦 Total patterns available: ${TOTAL_PATTERNS}"
  log ""
  
  # Calculate end index
  local end_index=$((offset + limit))
  if [ $end_index -gt $TOTAL_PATTERNS ]; then
    end_index=$TOTAL_PATTERNS
  fi
  
  log "🚀 Starting import (patterns ${offset} to ${end_index})..."
  log ""
  
  # Track statistics
  local imported=0
  local skipped=0
  local failed=0
  
  # Extract patterns from JSON
  jq -c ".patterns[${offset}:${end_index}][]" "${SOURCE_FILE}" | while read -r pattern; do
    PATTERN_ID=$(echo "${pattern}" | jq -r '.id // empty')
    
    if [ -z "${PATTERN_ID}" ]; then
      log "${YELLOW}⚠️  Skipping pattern (no ID)${NC}"
      ((skipped++))
      continue
    fi
    
    # Check if pattern already exists
    EXISTING=$(curl -s "${WP_URL}/wp/v2/posts?meta_key=ravelry_id&meta_value=${PATTERN_ID}" \
      -H "Authorization: Basic ${AUTH_BASE64}" | jq -r '.[0].id // empty')
    
    if [ -n "${EXISTING}" ]; then
      log "${YELLOW}⏭️  Pattern ${PATTERN_ID} already exists (post ID: ${EXISTING})${NC}"
      ((skipped++))
      continue
    fi
    
    # Extract pattern data
    PATTERN_NAME=$(echo "${pattern}" | jq -r '.name // "Unknown Pattern"')
    DESIGNER=$(echo "${pattern}" | jq -r '.designer.name // "Unknown Designer"')
    IS_FREE=$(echo "${pattern}" | jq -r '.free // false')
    PATTERN_URL=$(echo "${pattern}" | jq -r '.permalink // ""')
    PHOTO_URL=$(echo "${pattern}" | jq -r '.first_photo?.small_url // ""')
    DIFFICULTY=$(echo "${pattern}" | jq -r '.difficulty // "Niet gespecificeerd"')
    YARN_WEIGHT=$(echo "${pattern}" | jq -r '.yarn_weight?.name // "Niet gespecificeerd"')
    CRAFT=$(echo "${pattern}" | jq -r '.craft.name // ""')
    TAGS=$(echo "${pattern}" | jq -r '.tags[]?.name // ""' | tr '\n' ',' | sed 's/,$//')
    
    # Detect technique and thema
    TECHNIEK=$(detect_technique "${PATTERN_NAME}" "${TAGS}")
    THEMA=$(map_thema "${TECHNIEK}")
    
    # Prepare post title
    POST_TITLE="${PATTERN_NAME}"
    if [ "${IS_FREE}" = "true" ]; then
      POST_TITLE="Gratis: ${PATTERN_NAME}"
    fi
    
    # Prepare post content
    POST_CONTENT="<p><strong>"
    if [ "${IS_FREE}" = "true" ]; then
      POST_CONTENT+="✅ Gratis patroon door ${DESIGNER}!</strong></p>"
    else
      POST_CONTENT+="Patroon door ${DESIGNER}!</strong></p>"
    fi
    
    POST_CONTENT+="<h3>Details</h3>"
    POST_CONTENT+="<ul>"
    POST_CONTENT+="<li><strong>Designer:</strong> ${DESIGNER}</li>"
    
    if [ "${DIFFICULTY}" != "Niet gespecificeerd" ]; then
      POST_CONTENT+="<li><strong>Moeilijkheid:</strong> ${DIFFICULTY}</li>"
    fi
    
    if [ "${YARN_WEIGHT}" != "Niet gespecificeerd" ]; then
      POST_CONTENT+="<li><strong>Garen:</strong> ${YARN_WEIGHT}</li>"
    fi
    
    POST_CONTENT+="</ul>"
    
    POST_CONTENT+="<h3>Bekijk Patroon</h3>"
    POST_CONTENT+="<p><a href=\"${PATTERN_URL}\" target=\"_blank\" rel=\"nofollow sponsored\">Bekijk dit patroon op Ravelry →</a></p>"
    
    POST_CONTENT+="<h3>Tools</h3>"
    POST_CONTENT+="<p>Bereken hoeveel garn je nodig hebt met onze <a href=\"/tools/yardage-calculator/\">Yardage Calculator</a>.</p>"
    POST_CONTENT+="<p>Ontdek wat je met je garen stash kunt maken met de <a href=\"/tools/stash-calculator/\">Stash Calculator</a>.</p>"
    
    # Prepare meta description
    META_DESC="Gratis ${PATTERN_NAME} patroon door ${DESIGNER}."
    if [ "${IS_FREE}" = "true" ]; then
      META_DESC+=" Download nu op Ravelry. Inclusief materialenlijst en instructies."
    else
      META_DESC+=" Beschikbaar op Ravelry."
    fi
    
    # Sanitize content (remove null bytes)
    POST_CONTENT=$(sanitize_content "${POST_CONTENT}")
    POST_TITLE=$(sanitize_content "${POST_TITLE}")
    META_DESC=$(sanitize_content "${META_DESC}")
    
    # Create post JSON
    POST_JSON=$(cat <<EOF
{
  "title": "${POST_TITLE}",
  "content": "${POST_CONTENT}",
  "status": "draft",
  "excerpt": "${META_DESC}",
  "meta": {
    "ravelry_id": "${PATTERN_ID}",
    "ravelry_designer": "${DESIGNER}",
    "ravelry_free": "${IS_FREE}",
    "ravelry_permalink": "${PATTERN_URL}"
  }
}
EOF
)
    
    # Send to WordPress REST API
    log "${BLUE}📝 Creating post: ${POST_TITLE}${NC}"
    
    RESPONSE=$(curl -s -X POST \
      "${WP_URL}/wp/v2/posts" \
      -H "Authorization: Basic ${AUTH_BASE64}" \
      -H "Content-Type: application/json" \
      -d "${POST_JSON}" 2>&1)
    
    # Check for errors
    if echo "${RESPONSE}" | grep -q "code"; then
      log "${RED}❌ Failed to create post${NC}"
      log "${RESPONSE}"
      ((failed++))
      continue
    fi
    
    POST_ID=$(echo "${RESPONSE}" | jq -r '.id // empty')
    
    if [ -z "${POST_ID}" ] || [ "${POST_ID}" = "null" ]; then
      log "${RED}❌ Failed to create post (no ID returned)${NC}"
      log "${RESPONSE}"
      ((failed++))
      continue
    fi
    
    log "${GREEN}✅ Created post ID: ${POST_ID}${NC}"
    
    # Upload featured image if photo URL exists
    if [ -n "${PHOTO_URL}" ]; then
      log "${BLUE}   📷 Uploading featured image...${NC}"
      
      # Download image
      IMAGE_DATA=$(curl -s "${PHOTO_URL}" 2>&1)
      
      if [ -n "${IMAGE_DATA}" ]; then
        # Upload to WordPress
        MEDIA_RESPONSE=$(curl -s -X POST \
          "${WP_URL}/wp/v2/media" \
          -H "Authorization: Basic ${AUTH_BASE64}" \
          -H "Content-Disposition: attachment; filename=${PATTERN_ID}.jpg" \
          -H "Content-Type: image/jpeg" \
          --data-binary "${IMAGE_DATA}" 2>&1)
        
        FEATURED_ID=$(echo "${MEDIA_RESPONSE}" | jq -r '.id // empty')
        
        if [ -n "${FEATURED_ID}" ] && [ "${FEATURED_ID}" != "null" ]; then
          # Attach featured image to post
          curl -s -X POST \
            "${WP_URL}/wp/v2/posts/${POST_ID}" \
            -H "Authorization: Basic ${AUTH_BASE64}" \
            -H "Content-Type: application/json" \
            -d "{\"featured_media\": ${FEATURED_ID}}" > /dev/null
          
          log "${GREEN}   ✅ Featured image uploaded: ${FEATURED_ID}${NC}"
        else
          log "${YELLOW}   ⚠️  Failed to upload image${NC}"
        fi
      else
        log "${YELLOW}   ⚠️  Failed to download image${NC}"
      fi
    fi
    
    # Assign taxonomies (if hs_thema and hs_techniek taxonomies exist)
    log "${BLUE}   🏷️  Assigning taxonomies: ${THEMA} / ${TECHNIEK}${NC}"
    
    # Try to assign custom taxonomies (may fail if not created yet)
    curl -s -X POST \
      "${WP_URL}/wp/v2/posts/${POST_ID}" \
      -H "Authorization: Basic ${AUTH_BASE64}" \
      -H "Content-Type: application/json" \
      -d "{
        \"hs_thema\": \"${THEMA}\",
        \"hs_techniek\": \"${TECHNIEK}\"
      }" > /dev/null 2>&1
    
    ((imported++))
    log ""
  done
  
  # Print summary
  log "${BLUE}═══════════════════════════════════════════${NC}"
  log "${GREEN}✅ Import complete!${NC}"
  log ""
  log "📊 Statistics:"
  log "   Imported: ${imported}"
  log "   Skipped: ${skipped}"
  log "   Failed: ${failed}"
  log ""
  log "📝 Log file: ${LOG_FILE}"
  log ""
}

# Execute
import_patterns $LIMIT $OFFSET
