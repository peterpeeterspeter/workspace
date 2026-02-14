#!/bin/bash
# Get list of posts missing featured images

echo "Posts Missing Featured Images"
echo "=============================="
echo ""

for site in crashcasino crashgame freecrash cryptocrash; do
  case $site in
    crashcasino)
      API_URL="https://crashcasino.io/wp-json"
      CREDS="peter:3vRhtTs2khfdLtTiDFqkdeXI"
      DOMAIN="crashcasino.io"
      ;;
    crashgame)
      API_URL="https://crashgamegambling.com/wp-json"
      CREDS="@peter:MioX SygN Xaz6 pK9o RUiK tBMF"
      DOMAIN="crashgamegambling.com"
      ;;
    freecrash)
      API_URL="https://freecrashgames.com/wp-json"
      CREDS="@peter:F8Mg yZXM qJy4 jQvp BMeZ FoMG"
      DOMAIN="freecrashgames.com"
      ;;
    cryptocrash)
      API_URL="https://cryptocrashgambling.com/wp-json"
      CREDS="@peter:R3kQ 6vRA UwYd x7Cn KEtT Pk83"
      DOMAIN="cryptocrashgambling.com"
      ;;
  esac

  echo "Site: $DOMAIN"
  curl -s -u "$CREDS" "$API_URL/wp/v2/media?per_page=100" | \
    python3 -c "
import json, sys
media = json.load(sys.stdin)
featured_ids = set()
for m in media:
    if m.get('featured_media'):
        featured_ids.add(m['featured_media'])

print(f'  Total media items: {len(media)}')
print(f'  Featured images in use: {len(featured_ids)}')
"
  echo ""
done

# Now check which posts don't have featured images
echo "Posts Without Featured Images:"
echo "==============================="
echo ""

for site in crashcasino crashgame freecrash cryptocrash; do
  case $site in
    crashcasino)
      API_URL="https://crashcasino.io/wp-json"
      CREDS="peter:3vRhtTs2khfdLtTiDFqkdeXI"
      DOMAIN="crashcasino.io"
      ;;
    crashgame)
      API_URL="https://crashgamegambling.com/wp-json"
      CREDS="@peter:MioX SygN Xaz6 pK9o RUiK tBMF"
      DOMAIN="crashgamegambling.com"
      ;;
    freecrash)
      API_URL="https://freecrashgames.com/wp-json"
      CREDS="@peter:F8Mg yZXM qJy4 jQvp BMeZ FoMG"
      DOMAIN="freecrashgames.com"
      ;;
    cryptocrash)
      API_URL="https://cryptocrashgambling.com/wp-json"
      CREDS="@peter:R3kQ 6vRA UwYd x7Cn KEtT Pk83"
      DOMAIN="cryptocrashgambling.com"
      ;;
  esac

  echo "$DOMAIN:"
  curl -s -u "$CREDS" "$API_URL/wp/v2/posts?per_page=100&_fields=id,title,link,featured_media" | \
    python3 -c "
import json, sys, csv
posts = json.load(sys.stdin)
missing = []
for p in posts:
    if not p.get('featured_media') or p.get('featured_media') == 0:
        missing.append({
            'id': p['id'],
            'title': p['title']['rendered'].strip(),
            'url': p['link']
        })

if missing:
    print(f'  Missing: {len(missing)} posts')
    for m in missing[:5]:  # Show first 5
        print(f\"    ID {m['id']}: {m['title'][:60]}\")
    if len(missing) > 5:
        print(f'    ... and {len(missing) - 5} more')
else:
    print('  All posts have featured images ✅')
"
  echo ""
done
