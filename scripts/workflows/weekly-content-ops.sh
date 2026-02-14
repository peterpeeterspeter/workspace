#!/bin/bash
# Pinch-to-Post Workflow: Weekly Content Operations
# Run weekly maintenance and batch operations

set -e

WORKSPACE="/root/.openclaw/workspace"
PINCH_TO_POST="${WORKSPACE}/scripts/pinch-to-post.sh"
BACKUP_DIR="${WORKSPACE}/backups/content-$(date -u +%Y-%m-%d)"

echo "=== Weekly Content Operations ==="
echo "Date: $(date -u +%Y-%m-%d)"
echo ""

# 1. Full content backup
echo "💾 Creating Content Backup"
"$PINCH_TO_POST" backup "$BACKUP_DIR"
echo "  Backup location: $BACKUP_DIR"

echo ""
echo "---"
echo ""

# 2. Show full calendar for this month
echo "📅 This Month's Calendar"
MONTH=$(date -u +%Y-%m)
"$PINCH_TO_POST" calendar "$MONTH"

echo ""
echo "---"
echo ""

# 3. Draft status across sites
echo "📝 Draft Status"
for site in crashcasino crashgame freecrash cryptocrash; do
  COUNT=$("$PINCH_TO_POST" stats "$site" 2>&1 | grep "Drafts:" | awk '{print $2}')
  echo "  $site: $COUNT drafts"
done

echo ""
echo "---"
echo ""

# 4. Comment cleanup recommendations
echo "💬 Comment Moderation Summary"
for site in crashcasino crashgame freecrash cryptocrash; do
  COUNT=$("$PINCH_TO_POST" comment-moderate "$site" show-pending 2>&1 | tail -1 | awk '{print $3}')
  echo "  $site: $COUNT pending"
done

echo ""
echo "---"
echo ""

# 5. Weekly recommendations
echo "💡 Weekly Tasks:"
echo "  1. Review drafts and bulk-publish ready content"
echo "  2. Run comment moderation on all sites"
echo "  3. Share published content on social media"
echo "  4. Review content calendar for next week"
echo ""
echo "  Example commands:"
echo "    pinch-to-post bulk-publish crashcasino 100-120"
echo "    pinch-to-post comment-moderate crashcasino spam-suspicious"
echo "    pinch-to-post social-post twitter \"Weekly recap!\""

echo ""
echo "✅ Weekly check complete"
