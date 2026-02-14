#!/bin/bash
# Pinch-to-Post Workflow: Daily Content Operations
# Run daily checks and tasks

set -e

WORKSPACE="/root/.openclaw/workspace"
PINCH_TO_POST="${WORKSPACE}/scripts/pinch-to-post.sh"

echo "=== Daily Content Operations ==="
echo "Date: $(date -u +%Y-%m-%d)"
echo ""

# 1. Check stats across all sites
echo "📊 Content Statistics"
"$PINCH_TO_POST" stats

echo ""
echo "---"
echo ""

# 2. Show pending comments
echo "💬 Pending Comments Review"
for site in crashcasino crashgame freecrash cryptocrash; do
  echo "[$site]"
  "$PINCH_TO_POST" comment-moderate "$site" show-pending | head -20
done

echo ""
echo "---"
echo ""

# 3. Show today's publishing calendar
echo "📅 Today's Content Calendar"
TODAY=$(date -u +%Y-%m)
"$PINCH_TO_POST" calendar "$TODAY"

echo ""
echo "---"
echo ""

# 4. Recommendations
echo "💡 Recommendations:"
echo "  - Run 'pinch-to-post comment-moderate <site> spam-suspicious' to clean spam"
echo "  - Run 'pinch-to-post bulk-publish <site> <ids>' to publish drafts"
echo "  - Run 'pinch-to-post social-post twitter \"message\" \"url\"' to share content"

echo ""
echo "✅ Daily check complete"
