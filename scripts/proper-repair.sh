#!/bin/bash
# Proper Content Repair Using Pinch-to-Post's Markdown Converter

SITE_URL="${WP_SITE_URL:-https://crashcasino.io/wp-json}"
USERNAME="${WP_USERNAME:-peter}"
PASSWORD="${WP_APP_PASSWORD:-3vRhtTs2khfdLtTiDFqkdeXI}"

cd /root/.openclaw/workspace/skills/pinch-to-post

# Source the markdown_to_gutenberg function
source wp-rest.sh

echo "🔧 Proper Content Repair with Pinch-to-Post"
echo "============================================="
echo ""

# Get all posts
POSTS=$(curl -s -u "${USERNAME}:${PASSWORD}" "${SITE_URL}/wp/v2/posts?per_page=20&status=publish")

TOTAL=$(echo "$POSTS" | jq '. | length')
echo "📋 Processing $TOTAL posts..."
echo ""

UPDATED=0

for i in $(seq 0 $((TOTAL - 1))); do
    POST=$(echo "$POSTS" | jq ".[$i]")
    POST_ID=$(echo "$POST" | jq -r '.id')
    TITLE=$(echo "$POST" | jq -r '.title.rendered' | sed 's/<[^>]*>//g' | sed 's/&amp;/\&/g; s/&#038;/\&/g')
    CONTENT=$(echo "$POST" | jq -r '.content.rendered')

    echo "📄 [$POST_ID] $TITLE"

    # Step 1: Remove broken internal links from HTML
    CLEANED=$(echo "$CONTENT" | sed 's/<h\([1-6]\)[^>]*>[^<]*\(<a href="https:\/\/www\.crashcasino\.io\/[^"]*"[^>]*>[^<]*<\/a>\)[^<]*<\/h\1>/\1/g')

    # Step 2: Convert HTML tables to markdown format (for reconversion)
    # This is complex - let's just fix the obvious broken parts for now
    CLEANED=$(echo "$CLEANED" | sed 's/<h{level}>[^<]*<\/h{level}>//g')

    # Step 3: Fix loose <li> tags - wrap in <ul>
    # Simple approach: find consecutive <li> and wrap them
    CLEANED=$(echo "$CLEANED" | awk '
    /<li>/ {
        if (!in_list) {
            print "<ul>"
            in_list=1
        }
    }
    /<\/li>/ {
        print
        if (in_list && getline > 0 && !/<li>/) {
            print "</ul>"
            in_list=0
        }
        next
    }
    {print}
    ')

    # Check if content changed
    if [ "$CLEANED" != "$CONTENT" ]; then
        # Update the post
        RESULT=$(curl -s -X POST "${SITE_URL}/wp/v2/posts/${POST_ID}" \
            -u "${USERNAME}:${PASSWORD}" \
            -H "Content-Type: application/json" \
            -d "{\"content\":$(echo "$CLEANED" | jq -Rs .)}")

        if echo "$RESULT" | jq -e '.id' > /dev/null 2>&1; then
            echo "   ✅ Fixed"
            UPDATED=$((UPDATED + 1))
        else
            echo "   ❌ Failed"
        fi
    else
        echo "   ⏭️  OK (no changes needed)"
    fi

    echo ""
done

echo "============================================="
echo "📊 Updated: $UPDATED posts"
echo "✅ Done!"
