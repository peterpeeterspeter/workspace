#!/bin/bash
# Pinch-to-Post Helper: Social Cross-Posting
# Post content to Twitter, LinkedIn, Mastodon (if configured)

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
  echo "Usage: $0 <platform> <message> [url]"
  echo ""
  echo "Platforms: twitter, linkedin, mastodon"
  echo ""
  echo "Example:"
  echo '  $0 twitter "New article published!" "https://crashcasino.io/article"'
  echo '  $0 linkedin "Check out our latest post" "https://crashcasino.io/post"'
  exit 1
}

# Check arguments
if [[ $# -lt 2 ]]; then
  usage
fi

PLATFORM="$1"
MESSAGE="$2"
URL="${3:-}"

# Validate platform
VALID_PLATFORMS=("twitter" "linkedin" "mastodon")
if [[ ! " ${VALID_PLATFORMS[@]} " =~ " ${PLATFORM} " ]]; then
  echo -e "${RED}Error: Invalid platform '${PLATFORM}'${NC}"
  echo "Valid platforms: ${VALID_PLATFORMS[*]}"
  exit 1
fi

echo -e "${GREEN}=== Social Cross-Posting ===${NC}"
echo "Platform: ${PLATFORM}"
echo "Message: ${MESSAGE}"
if [[ -n "$URL" ]]; then
  echo "URL: ${URL}"
fi
echo ""

case "$PLATFORM" in
  twitter)
    # Check if Twitter credentials are configured
    if [[ -z "$TWITTER_API_KEY" ]]; then
      echo -e "${YELLOW}⚠ Twitter not configured. Set TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET in .env${NC}"
      exit 0
    fi

    # Post to Twitter using API v2
    if command -v twurl &> /dev/null; then
      if [[ -n "$URL" ]]; then
        FULL_MESSAGE="${MESSAGE} ${URL}"
      else
        FULL_MESSAGE="$MESSAGE"
      fi

      if twurl -X POST "/2/tweets" -d "text=${FULL_MESSAGE}" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Posted to Twitter${NC}"
      else
        echo -e "${RED}✗ Failed to post to Twitter${NC}"
        exit 1
      fi
    else
      echo -e "${YELLOW}⚠ twurl not installed. Install with: gem install twurl${NC}"
      exit 0
    fi
    ;;

  linkedin)
    # Check if LinkedIn credentials are configured
    if [[ -z "$LINKEDIN_ACCESS_TOKEN" ]]; then
      echo -e "${YELLOW}⚠ LinkedIn not configured. Set LINKEDIN_ACCESS_TOKEN in .env${NC}"
      exit 0
    fi

    # Post to LinkedIn
    if [[ -n "$URL" ]]; then
      FULL_MESSAGE="${MESSAGE}\n\n${URL}"
    else
      FULL_MESSAGE="$MESSAGE"
    fi

    RESPONSE=$(curl -s -X POST "https://api.linkedin.com/v2/ugcPosts" \
      -H "Authorization: Bearer ${LINKEDIN_ACCESS_TOKEN}" \
      -H "Content-Type: application/json" \
      -H "X-Restli-Protocol-Version: 2.0.0" \
      -d "{
        \"author\": \"urn:li:person:${LINKEDIN_PERSON_ID}\",
        \"lifecycleState\": \"PUBLISHED\",
        \"specificContent\": {
          \"com.linkedin.ugc.ShareContent\": {
            \"shareCommentary\": {
              \"text\": \"${FULL_MESSAGE}\"
            },
            \"shareMediaCategory\": \"NONE\"
          }
        },
        \"visibility\": {
          \"com.linkedin.ugc.MemberNetworkVisibility\": \"PUBLIC\"
        }
      }")

    if echo "$RESPONSE" | jq -e '.id' > /dev/null 2>&1; then
      echo -e "${GREEN}✓ Posted to LinkedIn${NC}"
    else
      echo -e "${RED}✗ Failed to post to LinkedIn${NC}"
      exit 1
    fi
    ;;

  mastodon)
    # Check if Mastodon credentials are configured
    if [[ -z "$MASTODON_INSTANCE" ]] || [[ -z "$MASTODON_ACCESS_TOKEN" ]]; then
      echo -e "${YELLOW}⚠ Mastodon not configured. Set MASTODON_INSTANCE and MASTODON_ACCESS_TOKEN in .env${NC}"
      exit 0
    fi

    # Post to Mastodon
    if [[ -n "$URL" ]]; then
      FULL_MESSAGE="${MESSAGE} ${URL}"
    else
      FULL_MESSAGE="$MESSAGE"
    fi

    RESPONSE=$(curl -s -X POST "${MASTODON_INSTANCE}/api/v1/statuses" \
      -H "Authorization: Bearer ${MASTODON_ACCESS_TOKEN}" \
      -H "Content-Type: application/json" \
      -d "{
        \"status\": \"${FULL_MESSAGE}\"
      }")

    if echo "$RESPONSE" | jq -e '.id' > /dev/null 2>&1; then
      echo -e "${GREEN}✓ Posted to Mastodon${NC}"
    else
      echo -e "${RED}✗ Failed to post to Mastodon${NC}"
      exit 1
    fi
    ;;

esac

exit 0
