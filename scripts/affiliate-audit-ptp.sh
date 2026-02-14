#!/bin/bash
# Affiliate Link Audit using Pinch-to-Post Skill Patterns
# Following SKILL.md documented REST API approach

echo "🔍 AFFILIATE LINK AUDIT - Pinch-to-Post Method"
echo "=================================================="
echo ""

# Affiliate domains from memory
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

# Site credentials (from pinch-to-post skill config)
declare -A SITES
SITES[crashcasino_url]="https://crashcasino.io/wp-json"
SITES[crashcasino_user]="peter"
SITES[crashcasino_pass]="3vRhtTs2khfdLtTiDFqkdeXI"

SITES[crashgame_url]="https://crashgamegambling.com/wp-json"
SITES[crashgame_user]="@peter"
SITES[crashgame_pass]="MioX SygN Xaz6 pK9o RUiK tBMF"

SITES[freecrash_url]="https://freecrashgames.com/wp-json"
SITES[freecrash_user]="@peter"
SITES[freecrash_pass]="F8Mg yZXM qJy4 jQvp BMeZ FoMG"

SITES[cryptocrash_url]="https://cryptocrashgambling.com/wp-json"
SITES[cryptocrash_user]="@peter"
SITES[cryptocrash_pass]="R3kQ 6vRA UwYd x7Cn KEtT Pk83"

audit_site() {
  local site="$1"
  local url="${SITES[${site}_url]}"
  local user="${SITES[${site}_user]}"
  local pass="${SITES[${site}_pass]}"

  echo "=== $site ==="
  echo ""

  # Get published posts (using pinch-to-post REST API pattern)
  posts=$(curl -s "${url}/wp/v2/posts?per_page=100&status=publish" \
    -u "${user}:${pass}")

  post_count=$(echo "$posts" | jq 'length')
  echo "Published posts: $post_count"
  echo ""

  # Check each post for affiliate links
  with_affiliates=0
  without_affiliates=0

  for i in $(seq 0 $((post_count - 1))); do
    post_id=$(echo "$posts" | jq -r ".[$i].id")
    title=$(echo "$posts" | jq -r ".[$i].title.rendered" | sed 's/|/-/g' | head -c 60)
    content=$(echo "$posts" | jq -r ".[$i].content.rendered")

    # Check for affiliate domains
    affiliate_count=0
    for domain in "${AFFILIATE_DOMAINS[@]}"; do
      count=$(echo "$content" | grep -oi "$domain" | wc -l)
      affiliate_count=$((affiliate_count + count))
    done

    if [ $affiliate_count -gt 0 ]; then
      echo "✅ Post $post_id | YES | $affiliate_count links | $title..."
      with_affiliates=$((with_affiliates + 1))
    else
      echo "❌ Post $post_id | NO | Missing | $title..."
      without_affiliates=$((without_affiliates + 1))
    fi
  done

  echo ""
  echo "Summary: With affiliates: $with_affiliates | Without: $without_affiliates"
  echo ""
}

# Audit each site
audit_site "crashcasino"
audit_site "crashgame"
audit_site "freecrash"
audit_site "cryptocrash"

echo "=================================================="
echo "Audit complete using pinch-to-post REST API patterns"
echo "=================================================="
