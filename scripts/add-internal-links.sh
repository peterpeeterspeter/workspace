#!/bin/bash
# Internal Link Builder for Pinch-to-Post
# Adds relevant internal links to all published posts

set -e

SITE_URL="${WP_SITE_URL:-https://crashcasino.io/wp-json}"
USERNAME="${WP_USERNAME:-peter}"
PASSWORD="${WP_APP_PASSWORD:-3vRhtTs2khfdLtTiDFqkdeXI}"

echo "🔗 Internal Link Builder"
echo "========================"
echo ""

# Step 1: Get all published posts
echo "📋 Fetching all published posts..."
POSTS=$(curl -s -u "${USERNAME}:${PASSWORD}" "${SITE_URL}/wp/v2/posts?per_page=100&status=publish")

# Count posts
TOTAL_POSTS=$(echo "$POSTS" | jq '. | length')
echo "Found $TOTAL_POSTS published posts"
echo ""

# Step 2: Build link database
echo "🗂️  Building link database..."
LINK_DB="/tmp/post_links.json"
echo "$POSTS" | jq -r '.[] | {
  id: .id,
  slug: .slug,
  title: .title.rendered,
  url: .link,
  keywords: (.title.rendered | ascii_downcase | gsub(" "; ","; ","; "-"; " "))
}' > "$LINK_DB"

echo "Link database created"
echo ""

# Step 3: Process each post
echo "🔄 Processing posts..."
echo ""

UPDATED=0
SKIPPED=0

for i in $(seq 0 $((TOTAL_POSTS - 1))); do
    POST=$(echo "$POSTS" | jq ".[$i]")
    POST_ID=$(echo "$POST" | jq -r '.id')
    POST_TITLE=$(echo "$POST" | jq -r '.title.rendered')
    POST_CONTENT=$(echo "$POST" | jq -r '.content.rendered')

    # Count current internal links
    CURRENT_LINKS=$(echo "$POST_CONTENT" | grep -o 'href="https://crashcasino.io' | wc -l)

    if [ "$CURRENT_LINKS" -ge 3 ]; then
        echo "⏭️  Post $POST_ID: \"$POST_TITLE\" - Already has $CURRENT_LINKS links (skipping)"
        SKIPPED=$((SKIPPED + 1))
        continue
    fi

    # Find relevant posts to link to
    # Extract keywords from current post title
    TITLE_KEYWORDS=$(echo "$POST_TITLE" | ascii_downcase | tr ' ' '\n' | grep -E '^(crash|gambling|casino|game|bet|safe|verify|rtp|bonus)' | head -3)

    echo "📝 Post $POST_ID: \"$POST_TITLE\""
    echo "   Current links: $CURRENT_LINKS"

    # Find 2-3 relevant posts to link
    LINKS_ADDED=0
    NEW_CONTENT="$POST_CONTENT"

    for keyword in $TITLE_KEYWORDS; do
        if [ $LINKS_ADDED -ge 3 ]; then
            break
        fi

        # Find posts with this keyword (excluding current post)
        TARGET_POST=$(echo "$POSTS" | jq -r ".[] | select(.id != $POST_ID and .title.rendered | ascii_downcase | contains(\"$keyword\")) | .id, .title.rendered, .link" | head -1 | tr '\n' ' ')

        if [ -n "$TARGET_POST" ]; then
            TARGET_ID=$(echo "$TARGET_POST" | awk '{print $1}')
            TARGET_TITLE=$(echo "$TARGET_POST" | awk '{print $2}')
            TARGET_URL=$(echo "$TARGET_POST" | awk '{print $3}')

            # Check if already linked
            if echo "$NEW_CONTENT" | grep -q "$TARGET_URL"; then
                continue
            fi

            # Add link at the end of the post
            LINK_HTML="<p><strong>Related:</strong> <a href=\"$TARGET_URL\">$TARGET_TITLE</a></p>"
            NEW_CONTENT="${NEW_CONTENT}${LINK_HTML}"

            LINKS_ADDED=$((LINKS_ADDED + 1))
            echo "   ➕ Added link to: $TARGET_TITLE"
        fi
    done

    if [ $LINKS_ADDED -gt 0 ]; then
        # Update post
        UPDATE_RESULT=$(curl -s -X POST "${SITE_URL}/wp/v2/posts/${POST_ID}" \
            -u "${USERNAME}:${PASSWORD}" \
            -H "Content-Type: application/json" \
            -d "{\"content\":$(echo "$NEW_CONTENT" | jq -Rs .)}")

        if echo "$UPDATE_RESULT" | jq -e '.id' > /dev/null 2>&1; then
            echo "   ✅ Updated successfully (added $LINKS_ADDED links)"
            UPDATED=$((UPDATED + 1))
        else
            echo "   ❌ Update failed"
        fi
    else
        echo "   ⚠️  No relevant links found"
    fi

    echo ""
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 SUMMARY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Total posts: $TOTAL_POSTS"
echo "Updated: $UPDATED"
echo "Skipped: $SKIPPED"
echo ""
echo "✅ Done!"
