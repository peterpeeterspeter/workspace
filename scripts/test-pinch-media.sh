#!/bin/bash
# Test pinch-to-post media-upload feature
# Safely adds image to post without touching content

POST_ID=787
IMAGE="/root/.openclaw/workspace/temp/images-custom-batch2/crashcasino_787.png"
ALT_TEXT="Featured image for article: Safe Crash Gambling: Red Flags to Avoid in 2026"
SITE="crashcasino"

echo "Testing pinch-to-post media-upload feature"
echo "=========================================="
echo "Post ID: $POST_ID"
echo "Image: $IMAGE"
echo "Site: $SITE"
echo ""

# Check content length before
echo "Checking content BEFORE..."
CONTENT_BEFORE=$(curl -s "https://crashcasino.io/wp-json/wp/v2/posts/$POST_ID" -u "peter:3vRhtTs2khfdLtTiDFqkdeXI" | python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d.get('content',{}).get('raw','')))")
echo "Content length: $CONTENT_BEFORE chars"
echo ""

# Try pinch-to-post media-upload
echo "Running pinch-to-post media-upload..."
~/.openclaw/workspace/scripts/publish-gateway.sh media-upload "$SITE" "$IMAGE" "$ALT_TEXT" "" "$POST_ID"

echo ""
echo "Checking content AFTER..."
CONTENT_AFTER=$(curl -s "https://crashcasino.io/wp-json/wp/v2/posts/$POST_ID" -u "peter:3vRhtTs2khfdLtTiDFqkdeXI" | python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d.get('content',{}).get('raw','')))")
echo "Content length: $CONTENT_AFTER chars"
echo ""

if [ "$CONTENT_BEFORE" == "$CONTENT_AFTER" ]; then
    echo "✅ SUCCESS: Content preserved ($CONTENT_BEFORE chars = $CONTENT_AFTER chars)"
else
    echo "⚠️ WARNING: Content changed (was $CONTENT_BEFORE, now $CONTENT_AFTER)"
fi
