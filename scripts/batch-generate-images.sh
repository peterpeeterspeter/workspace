#!/bin/bash
# Batch generate and upload featured images for crash casino sites

# Configuration
OUTPUT_DIR="/root/.openclaw/workspace/temp/images"
mkdir -p "$OUTPUT_DIR"

# Image generation API (configure based on what we have access to)
# Options: DALL-E, Stability AI, Ideogram, Leonardo
IMAGE_API="${IMAGE_API:-dalle}"  # default to DALL-E

echo "🎨 Image Generation Batch Job"
echo "=============================="
echo "Output: $OUTPUT_DIR"
echo "API: $IMAGE_API"
echo ""

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to generate image prompt from post title
generate_prompt() {
  local title="$1"
  local site="$2"

  # Base prompt for crash casino theme
  local base_prompt="Professional gambling illustration, crash game multiplier rocket, casino chips, modern sleek design, 1200x630"

  # Customize based on keywords in title
  if echo "$title" | grep -iq "rigged\|fairness\|verify"; then
    echo "$base_prompt, trust badges, security symbols, blue and white color scheme"
  elif echo "$title" | grep -iq "bonus\|codes\|free"; then
    echo "$base_prompt, bonus coins, gift boxes, gold and green accents"
  elif echo "$title" | grep -iq "strategy\|cashout\|mistakes"; then
    echo "$base_prompt, charts, upward trends, profit symbols, professional business style"
  elif echo "$title" | grep -iq "bitcoin\|crypto\|no-kyc"; then
    echo "$base_prompt, bitcoin symbols, blockchain network, purple and gold theme"
  elif echo "$title" | grep -iq "india\|chinese\|german"; then
    echo "$base_prompt, multicultural elements, globe, diverse players"
  else
    echo "$base_prompt, casino gaming aesthetic"
  fi
}

# Function to generate image via API
generate_image() {
  local prompt="$1"
  local output_file="$2"

  case "$IMAGE_API" in
    dalle)
      # DALL-E 3 via OpenAI API
      # Requires: OPENAI_API_KEY env variable
      if [ -z "$OPENAI_API_KEY" ]; then
        echo "ERROR: OPENAI_API_KEY not set"
        return 1
      fi

      echo "  → Generating with DALL-E 3..."
      curl -s "https://api.openai.com/v1/images/generations" \
        -H "Authorization: Bearer $OPENAI_API_KEY" \
        -H "Content-Type: application/json" \
        -d "{
          \"model\": \"dall-e-3\",
          \"prompt\": \"$prompt\",
          \"n\": 1,
          \"size\": \"1024x1792\",
          \"style\": \"vivid\"
        }" | python3 -c "
import json, sys, urllib.request
data = json.load(sys.stdin)
if 'error' in data:
    print(f'ERROR: {data[\"error\"]}', file=sys.stderr)
    sys.exit(1)
url = data['data'][0]['url']
urllib.request.urlretrieve(url, '$output_file')
print('  ✓ Image downloaded')
"
      ;;
    
    stability)
      # Stability AI (Stable Diffusion XL)
      # Requires: STABILITY_API_KEY env variable
      if [ -z "$STABILITY_API_KEY" ]; then
        echo "ERROR: STABILITY_API_KEY not set"
        return 1
      fi

      echo "  → Generating with SDXL..."
      curl -s "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/image-to-image" \
        -H "Authorization: Bearer $STABILITY_API_KEY" \
        -H "Content-Type: application/json" \
        -d "{
          \"text_prompts\": [{\"text\": \"$prompt\"}],
          \"cfg_scale\": 7,
          \"height\": 1056,
          \"width\": 1024,
          \"steps\": 30
        }" | python3 -c "
import json, sys, base64, urllib.request
data = json.load(sys.stdin)
if 'errors' in data:
    print(f'ERROR: {data[\"errors\"]}', file=sys.stderr)
    sys.exit(1)
img_data = base64.b64decode(data['artifacts'][0]['base64'])
with open('$output_file', 'wb') as f:
    f.write(img_data)
print('  ✓ Image downloaded')
"
      ;;

    *)
      echo "ERROR: Unsupported IMAGE_API: $IMAGE_API"
      echo "Supported: dalle, stability"
      return 1
      ;;
  esac
}

# Function to upload image via pinch-to-post
upload_image() {
  local image_file="$1"
  local site="$2"
  local post_id="$3"
  local alt_text="$4"

  echo "  → Uploading to $site..."
  
  # Use pinch-to-post media-upload
  ~/.openclaw/workspace/scripts/publish-gateway.sh media-upload "$site" "$image_file" "$alt_text" "" "$post_id"
  
  if [ $? -eq 0 ]; then
    echo "  ✓ Uploaded successfully"
    return 0
  else
    echo "  ✗ Upload failed"
    return 1
  fi
}

# Main processing loop
process_site() {
  local site="$1"
  local api_url="$2"
  local creds="$3"

  echo ""
  echo -e "${YELLOW}Processing: $site${NC}"
  echo "================================"

  # Get posts without featured images
  curl -s -u "$creds" "$api_url/wp/v2/posts?per_page=100&_fields=id,title,link,featured_media" | \
    python3 -c "
import json, sys, os

posts = json.load(sys.stdin)
missing = [p for p in posts if not p.get('featured_media') or p.get('featured_media') == 0]

print(f'Found {len(missing)} posts without images')

for p in missing:
    post_id = p['id']
    title = p['title']['rendered'].strip()
    url = p['link']
    
    print(f'\nPost {post_id}: {title[:60]}')
    
    # Generate prompt
    prompt = '''Professional gambling illustration, crash game multiplier rocket, casino chips, modern sleek design, 1200x630, high quality, no text overlay'''
    
    # Output filename
    safe_title = ''.join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in title)
    safe_title = safe_title[:50]
    img_file = f'$OUTPUT_DIR/{site}_{post_id}_{safe_title}.png'
    
    alt_text = f'Featured image for article: {title}'
    
    print(f'  Prompt: {prompt[:80]}...')
    print(f'  Output: {img_file}')
    print(f'  Alt text: {alt_text}')
    print(f'  POST_ID={post_id}|SITE={site}|IMG={img_file}|ALT={alt_text}')
"
}

# Process each site
echo "Step 1: Scanning for posts without images..."
echo ""

case "$1" in
  crashcasino)
    process_site "crashcasino" \
      "https://crashcasino.io/wp-json" \
      "peter:3vRhtTs2khfdLtTiDFqkdeXI"
    ;;
  crashgame)
    process_site "crashgame" \
      "https://crashgamegambling.com/wp-json" \
      "@peter:MioX SygN Xaz6 pK9o RUiK tBMF"
    ;;
  freecrash)
    process_site "freecrash" \
      "https://freecrashgames.com/wp-json" \
      "@peter:F8Mg yZXM qJy4 jQvp BMeZ FoMG"
    ;;
  cryptocrash)
    process_site "cryptocrash" \
      "https://cryptocrashgambling.com/wp-json" \
      "@peter:R3kQ 6vRA UwYd x7Cn KEtT Pk83"
    ;;
  all|"")
    # Process all sites
    for site in crashcasino crashgame freecrash cryptocrash; do
      $0 "$site"
    done
    ;;
  *)
    echo "Usage: $0 [crashcasino|crashgame|freecrash|cryptocrash|all]"
    echo ""
    echo "Environment variables needed:"
    echo "  OPENAI_API_KEY=xxx    # For DALL-E 3"
    echo "  STABILITY_API_KEY=xxx # For Stability AI"
    exit 1
    ;;
esac

echo ""
echo "=============================="
echo "Scan complete!"
echo ""
echo "Next step:"
echo "1. Set your API key: export OPENAI_API_KEY='your-key'"
echo "2. Run generation: $0 all | grep 'POST_ID=' > batch.txt"
echo "3. Process batch: ./process-batch.sh batch.txt"
