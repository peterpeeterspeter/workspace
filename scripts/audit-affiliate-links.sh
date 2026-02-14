#!/bin/bash
# Audit posts for affiliate links across all crash casino sites

AFFILIATE_DOMAINS=(
  "cybetplay.com"
  "bzstarz1.com"
  "betzrd.com"
  "7bit.partners"
  "mirax.partners"
  "trustdice.win"
  "reffpa.com"
  "betfury.bet"
)

check_affiliate_links() {
  local post_content="$1"
  local post_id="$2"
  local has_affiliate="NO"
  local found_links=()

  for domain in "${AFFILIATE_DOMAINS[@]}"; do
    if echo "$post_content" | grep -q "$domain"; then
      has_affiliate="YES"
      found_links+=("$domain")
    fi
  done

  echo "$post_id|$has_affiliate|${found_links[@]}"
}

audit_site() {
  local site="$1"
  local base_url="$2"
  local username="$3"
  local password="$4"

  echo "=========================================="
  echo "AUDIT: $site ($base_url)"
  echo "=========================================="
  echo ""

  # Get published posts
  posts=$(curl -s "${base_url}/wp-json/wp/v2/posts?per_page=100&status=publish" \
    -u "${username}:${password}")

  post_count=$(echo "$posts" | jq 'length')
  echo "Total published posts: $post_count"
  echo ""

  # Audit each post
  echo "ID | Title | Affiliate Links | Found Domains"
  echo "---|-------|-----------------|---------------"

  for i in $(seq 0 $((post_count - 1))); do
    post_id=$(echo "$posts" | jq -r ".[$i].id")
    title=$(echo "$posts" | jq -r ".[$i].title.rendered" | head -c 60)
    content=$(echo "$posts" | jq -r ".[$i].content.rendered")

    result=$(check_affiliate_links "$content" "$post_id")
    has_affiliate=$(echo "$result" | cut -d'|' -f2)
    domains=$(echo "$result" | cut -d'|' -f3- | sed 's/ /, /g')

    if [ "$has_affiliate" = "YES" ]; then
      echo "✅ $post_id | $title | YES | $domains"
    else
      echo "❌ $post_id | $title | NO | -"
    fi
  done

  echo ""
  echo "Summary:"
  with_affiliates=$(echo "$posts" | jq '[.[] | select(.content.rendered | test("cybetplay|bzstarz|betzrd|7bit.partners|mirax.partners|trustdice|reffpa|betfury"))] | length')
  without_affiliates=$((post_count - with_affiliates))
  echo "  With affiliate links: $with_affiliates"
  echo "  Without affiliate links: $without_affiliates"
  echo ""
}

# Read credentials from .env
source /root/.openclaw/workspace/.env 2>/dev/null || true

# Audit all sites
audit_site "crashcasino" "https://crashcasino.io/wp-json" \
  "${WORDPRESS_CRASHCASINO_USER}" "${WORDPRESS_CRASHCASINO_APP_PASSWORD}"

audit_site "crashgame" "https://crashgamegambling.com/wp-json" \
  "${WORDPRESS_CRASHGAMEGAMBLING_USER}" "${WORDPRESS_CRASHGAMEGAMBLING_APP_PASSWORD}"

audit_site "freecrash" "https://freecrashgames.com/wp-json" \
  "${WORDPRESS_FREECRASH_USER}" "${WORDPRESS_FREECRASH_APP_PASSWORD}"

audit_site "cryptocrash" "https://cryptocrashgambling.com/wp-json" \
  "${WORDPRESS_CRYPTOCRASH_USER}" "${WORDPRESS_CRYPTOCRASH_APP_PASSWORD}"
