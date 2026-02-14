#!/bin/bash
# Smart Internal Link Builder for Pinch-to-Post
# Analyzes content and adds contextually relevant internal links

set -e

SITE_URL="${WP_SITE_URL:-https://crashcasino.io/wp-json}"
USERNAME="${WP_USERNAME:-peter}"
PASSWORD="${WP_APP_PASSWORD:-3vRhtTs2khfdLtTiDFqkdeXI}"

echo "🔗 Smart Internal Link Builder"
echo "================================"
echo ""

# Step 1: Get all published posts
echo "📋 Fetching all published posts..."
POSTS_JSON=$(curl -s -u "${USERNAME}:${PASSWORD}" "${SITE_URL}/wp/v2/posts?per_page=100&status=publish")

# Count posts
TOTAL_POSTS=$(echo "$POSTS_JSON" | jq '. | length')
echo "✅ Found $TOTAL_POSTS published posts"
echo ""

# Step 2: Build a keyword-to-post mapping
echo "🗂️  Building content index..."

# Create a temporary file for the mapping
MAPPING_FILE="/tmp/post_mapping.json"
echo "{}" > "$MAPPING_FILE"

echo "$POSTS_JSON" | jq -c '.[]' | while read -r post; do
    POST_ID=$(echo "$post" | jq -r '.id')
    TITLE=$(echo "$post" | jq -r '.title.rendered' | sed 's/<[^>]*>//g')
    SLUG=$(echo "$post" | jq -r '.slug')
    URL=$(echo "$post" | jq -r '.link')

    # Extract keywords (lowercase, remove special chars)
    KEYWORDS=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | tr -cs '[:alpha:]' '\n' | grep -E 'crash|gambling|casino|game|bet|safe|verify|rtp|bonus|stake|bcgame|roobet|aviator|provably|fair|license|curacao|strategy|guide|scam|avoid' | sort -u | head -5)

    # Add to mapping
    for kw in $KEYWORDS; do
        jq --arg id "$POST_ID" --arg title "$TITLE" --arg url "$URL" --arg kw "$kw" \
           '.[$kw] += [{id: $id, title: $title, url: $url}]' "$MAPPING_FILE" > "${MAPPING_FILE}.tmp"
        mv "${MAPPING_FILE}.tmp" "$MAPPING_FILE"
    done
done

echo "✅ Index built"
echo ""

# Step 3: Process each post
echo "🔄 Analyzing and updating posts..."
echo ""

UPDATED=0
SKIPPED=0
TOTAL_LINKS_ADDED=0

# Process posts in batches
echo "$POSTS_JSON" | jq -c '.[]' | while read -r post; do
    POST_ID=$(echo "$post" | jq -r '.id')
    TITLE=$(echo "$post" | jq -r '.title.rendered' | sed 's/<[^>]*>//g')
    CONTENT=$(echo "$post" | jq -r '.content.rendered')

    # Count current internal links
    CURRENT_LINKS=$(echo "$CONTENT" | grep -o 'href="https://crashcasino.io' | wc -l)

    # Skip if already has 3+ internal links
    if [ "$CURRENT_LINKS" -ge 3 ]; then
        echo "⏭️  [$POST_ID] \"$TITLE\" - Already has $CURRENT_LINKS links"
        SKIPPED=$((SKIPPED + 1))
        continue
    fi

    echo "📝 [$POST_ID] \"$TITLE\""
    echo "   Current internal links: $CURRENT_LINKS"

    # Extract keywords from content
    CONTENT_WORDS=$(echo "$CONTENT" | sed 's/<[^>]*>//g' | tr '[:upper:]' '[:lower:]' | tr -cs '[:alpha:]' '\n' | sort | uniq -c | sort -rn | head -20 | awk '{print $2}')

    LINKS_TO_ADD=$((3 - CURRENT_LINKS))
    LINKS_ADDED=0
    MODIFIED_CONTENT="$CONTENT"

    # Find relevant posts based on content keywords
    for word in $CONTENT_WORDS; do
        if [ $LINKS_ADDED -ge $LINKS_TO_ADD ]; then
            break
        fi

        # Skip short words or common words
        if [ ${#word} -lt 4 ]; then
            continue
        fi

        # Find posts matching this keyword
        RELATED_POSTS=$(jq -r --arg kw "$word" '.[$kw] // [] | map(select(.id != '$POST_ID')) | .[0:3] | .[]' "$MAPPING_FILE" 2>/dev/null)

        if [ -z "$RELATED_POSTS" ]; then
            continue
        fi

        # Add links from related posts
        echo "$RELATED_POSTS" | while read -r related; do
            if [ $LINKS_ADDED -ge $LINKS_TO_ADD ]; then
                break
            fi

            RELATED_ID=$(echo "$related" | jq -r '.id')
            RELATED_TITLE=$(echo "$related" | jq -r '.title')
            RELATED_URL=$(echo "$related" | jq -r '.url')

            # Check if already linked
            if echo "$MODIFIED_CONTENT" | grep -q "$RELATED_URL"; then
                continue
            fi

            # Find a natural place to insert the link (before closing </p> tag)
            # Use the keyword as anchor text if it exists in the content
            if echo "$MODIFIED_CONTENT" | grep -qi ">[^<]*${word}[^<]*</p>"; then
                # Replace the word occurrence with a link
                MODIFIED_CONTENT=$(echo "$MODIFIED_CONTENT" | sed "0,/\(${word}\)/I\\<a href=\"${RELATED_URL}\\">\\1<\/a>/")
                echo "   ➕ Linked \"$word\" → \"$RELATED_TITLE\""
                LINKS_ADDED=$((LINKS_ADDED + 1))
            fi
        done
    done

    # If we couldn't add natural links, add a "Related Reading" section at the end
    if [ $LINKS_ADDED -lt $LINKS_TO_ADD ] && [ $LINKS_ADDED -eq 0 ]; then
        # Get most recent posts
        RECENT_POSTS=$(echo "$POSTS_JSON" | jq -r '[.[] | select(.id != '$POST_ID')] | sort_by(.date) | reverse | .[0:3] | .[]' | while read -r rp; do
            RID=$(echo "$rp" | jq -r '.id')
            RTITLE=$(echo "$rp" | jq -r '.title.rendered')
            RURL=$(echo "$rp" | jq -r '.link')
            echo "<li><a href=\"$RURL\">$RTITLE</a></li>"
        done)

        if [ -n "$RECENT_POSTS" ]; then
            RELATED_SECTION="\n\n<hr/>\n<h3>Related Reading</h3>\n<ul>$RECENT_POSTS</ul>"
            MODIFIED_CONTENT="${MODIFIED_CONTENT}${RELATED_SECTION}"
            LINKS_ADDED=$((LINKS_ADDED + $(echo "$RECENT_POSTS" | wc -l)))
            echo "   ➕ Added \"Related Reading\" section with links"
        fi
    fi

    # Update the post if we added links
    if [ $LINKS_ADDED -gt 0 ]; then
        UPDATE_RESULT=$(curl -s -X POST "${SITE_URL}/wp/v2/posts/${POST_ID}" \
            -u "${USERNAME}:${PASSWORD}" \
            -H "Content-Type: application/json" \
            -d "{\"content\":$(echo "$MODIFIED_CONTENT" | jq -Rs .)}")

        if echo "$UPDATE_RESULT" | jq -e '.id' > /dev/null 2>&1; then
            echo "   ✅ Updated (+$LINKS_ADDED links)"
            UPDATED=$((UPDATED + 1))
            TOTAL_LINKS_ADDED=$((TOTAL_LINKS_ADDED + LINKS_ADDED))
        else
            echo "   ❌ Update failed"
        fi
    else
        echo "   ⚠️  No suitable links found"
    fi

    echo ""
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 SUMMARY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Total posts analyzed: $TOTAL_POSTS"
echo "Posts updated: $UPDATED"
echo "Posts skipped (already linked): $SKIPPED"
echo "Total links added: $TOTAL_LINKS_ADDED"
echo ""
echo "✅ Internal link building complete!"
