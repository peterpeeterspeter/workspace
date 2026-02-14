#!/bin/bash

# WordPress Homepage Update Script
# Updates all 4 crash gambling site homepages via REST API
#
# Usage: ./update_homepages.sh
#
# Requirements:
# - WordPress Application Passwords plugin installed on each site
# - API tokens generated for each site
# - .env file with API credentials

set -e

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "Error: .env file not found"
    echo "Create .env with the following variables:"
    echo "  CRYPTOCRASH_URL=https://cryptocrashgambling.com"
    echo "  CRYPTOCRASH_API_TOKEN=your_token_here"
    echo "  CRASHCASINO_URL=https://crashcasino.io"
    echo "  CRASHCASINO_API_TOKEN=your_token_here"
    echo "  CRASHGAME_URL=https://crashgamegambling.com"
    echo "  CRASHGAME_API_TOKEN=your_token_here"
    echo "  FREECRASH_URL=https://freecrashgames.com"
    echo "  FREECRASH_API_TOKEN=your_token_here"
    exit 1
fi

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== WordPress Homepage Update Script ===${NC}\n"

# Function to update homepage
update_homepage() {
    local site_name=$1
    local site_url=$2
    local api_token=$3
    local content_file=$4

    echo -e "${BLUE}Updating ${site_name}...${NC}"

    # Check if content file exists
    if [ ! -f "$content_file" ]; then
        echo -e "${RED}Error: Content file not found: ${content_file}${NC}"
        return 1
    fi

    # Get homepage ID
    echo "Fetching homepage ID..."
    homepage_response=$(curl -s "${site_url}/wp-json/wp/v2/pages?slug=home")

    if [ -z "$homepage_response" ]; then
        echo -e "${RED}Error: Could not fetch pages. Check API access.${NC}"
        return 1
    fi

    homepage_id=$(echo "$homepage_response" | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)

    if [ -z "$homepage_id" ]; then
        echo -e "${RED}Error: Could not find homepage ID. Check page slug.${NC}"
        return 1
    fi

    echo "Homepage ID: $homepage_id"

    # Extract content from markdown file (between HTML code blocks)
    # This is a simple extraction - you may need to adjust based on actual file format
    content=$(sed -n '/<html/,/<\/html>/p' "$content_file" | sed '1d;$d')

    if [ -z "$content" ]; then
        echo -e "${RED}Error: Could not extract content from ${content_file}${NC}"
        return 1
    fi

    # Update via REST API
    echo "Updating homepage via REST API..."
    response=$(curl -s -X POST "${site_url}/wp-json/wp/v2/pages/${homepage_id}" \
        -H "Authorization: Bearer ${api_token}" \
        -H "Content-Type: application/json" \
        -d "{\"content\": $(echo "$content" | jq -Rs .)}")

    # Check for errors
    if echo "$response" | grep -q "code"; then
        echo -e "${RED}Error updating homepage:${NC}"
        echo "$response" | jq -r '.message // .'
        return 1
    fi

    echo -e "${GREEN}✓ ${site_name} updated successfully${NC}\n"
    return 0
}

# Update each site
# Note: Content files need to be created from the markdown files first
# This script assumes you've extracted HTML content to .html files

# CryptoCrashGambling.com
# update_homepage "CryptoCrashGambling" "$CRYPTOCRASH_URL" "$CRYPTOCRASH_API_TOKEN" "drafts/cryptocrashgambling-homepage.html"

# CrashCasino.io
# update_homepage "CrashCasino" "$CRASHCASINO_URL" "$CRASHCASINO_API_TOKEN" "drafts/crashcasino-homepage.html"

# CrashGameGambling.com
# update_homepage "CrashGameGambling" "$CRASHGAME_URL" "$CRASHGAME_API_TOKEN" "drafts/crashgamegambling-homepage.html"

# FreeCrashGames.com
# update_homepage "FreeCrashGames" "$FREECRASH_URL" "$FREECRASH_API_TOKEN" "drafts/freecrashgames-homepage.html"

echo -e "${GREEN}=== All updates complete ===${NC}"
echo ""
echo "Note: Script is commented out by default."
echo "Uncomment the update_homepage calls after:"
echo "1. Creating .env with API credentials"
echo "2. Extracting HTML content from markdown files"
echo "3. Testing with one site first"
