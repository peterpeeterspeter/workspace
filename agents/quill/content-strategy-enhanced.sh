#!/bin/bash
# Quill's Enhanced Publishing & Marketing Workflow
# Uses ALL pinch-to-post features for full automation

TASK_ID=$1
TASK_TITLE=$2

# Pinch-to-Post wrapper
PINCH_TO_POST="/root/.openclaw/workspace/scripts/pinch-to-post.sh"

# Log setup
LOG_DIR="/root/.openclaw/workspace/tasks/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/${TASK_ID}.log"

echo "=== $(date '+%Y-%m-%d %H:%M:%S') ===" | tee -a "$LOG_FILE"
echo "Quill: Enhanced Publishing & Marketing (FULL PINCH-TO-POST INTEGRATION)" | tee -a "$LOG_FILE"
echo "Task: ${TASK_TITLE}" | tee -a "$LOG_FILE"

# ===== DAILY ROUTINE (Publishing Schedule) =====

echo "" | tee -a "$LOG_FILE"
echo "📅 Daily Publishing Schedule Review..." | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# Check today's calendar
TODAY=$(date -u +%Y-%m)
echo "Today's Content Calendar:" | tee -a "$LOG_FILE"
"$PINCH_TO_POST" calendar "$TODAY" 2>&1 | tee -a "$LOG_FILE"

echo "" | tee -a "$LOG_FILE"
echo "Current Statistics:" | tee -a "$LOG_FILE"
"$PINCH_TO_POST" stats 2>&1 | tee -a "$LOG_FILE"

# ===== TASK WORK =====

if [[ "$TASK_TITLE" =~ [Bb]rand ]] || [[ "$TASK_TITLE" =~ [Ii]dentity ]]; then
  # Brand strategy
  echo "" | tee -a "$LOG_FILE"
  echo "Task Type: Brand Strategy" | tee -a "$LOG_FILE"
  # (Your existing brand strategy logic here)

elif [[ "$TASK_TITLE" =~ [Cc]ontent.*[Ss]trategy ]] || [[ "$TASK_TITLE" =~ [Cc]alendar ]]; then
  # Content strategy
  echo "" | tee -a "$LOG_FILE"
  echo "Task Type: Content Strategy" | tee -a "$LOG_FILE"

  # Show calendar for planning
  THIS_MONTH=$(date -u +%Y-%m)
  echo "" | tee -a "$LOG_FILE"
  echo "This Month's Calendar:" | tee -a "$LOG_FILE"
  "$PINCH_TO_POST" calendar "$THIS_MONTH" 2>&1 | tee -a "$LOG_FILE"

  echo "" | tee -a "$LOG_FILE"
  echo "Draft Status:" | tee -a "$LOG_FILE"
  for site in crashcasino crashgame freecrash cryptocrash; do
    echo "[$site]" | tee -a "$LOG_FILE"
    STATS=$("$PINCH_TO_POST" stats "$site" 2>&1)
    echo "$STATS" | grep "Drafts:" | tee -a "$LOG_FILE"
  done

  # (Your existing content strategy logic here)

elif [[ "$TASK_TITLE" =~ [Gg][Tt][Mm] ]] || [[ "$TASK_TITLE" =~ [Mm]arketing.*[Pp]lan ]]; then
  # GTM strategy
  echo "" | tee -a "$LOG_FILE"
  echo "Task Type: GTM Strategy" | tee -a "$LOG_FILE"
  # (Your existing GTM logic here)

elif [[ "$TASK_TITLE" =~ [Bb]ulk.*[Pp]ublish ]] || [[ "$TASK_TITLE" =~ [Pp]ublish.*[Bb]atch ]]; then
  # Bulk publishing task
  echo "" | tee -a "$LOG_FILE"
  echo "Task Type: Bulk Publishing" | tee -a "$LOG_FILE"

  # Bulk publish to all sites
  for site in crashcasino crashgame freecrash cryptocrash; do
    echo "" | tee -a "$LOG_FILE"
    echo "Publishing to ${site}..." | tee -a "$LOG_FILE"

    # Find post IDs for this site (from drafts directory)
    POST_IDS=$(grep -h "^POST_ID:" /root/.openclaw/workspace/drafts/*.md 2>/dev/null | sed 's/^POST_ID: //' | tr '\n' ' ')

    if [ -n "$POST_IDS" ]; then
      "$PINCH_TO_POST" bulk-publish "$site" $POST_IDS 2>&1 | tee -a "$LOG_FILE"
    else
      echo "No posts to publish for ${site}" | tee -a "$LOG_FILE"
    fi
  done

elif [[ "$TASK_TITLE" =~ [Ss]ocial.*[Pp]ost ]] || [[ "$TASK_TITLE" =~ [Dd]istribute ]]; then
  # Social media distribution
  echo "" | tee -a "$LOG_FILE"
  echo "Task Type: Social Media Distribution" | tee -a "$LOG_FILE"

  # Get recently published posts (from calendar)
  echo "Checking for recently published content..." | tee -a "$LOG_FILE"

  # Example: Share top content on social media
  echo "" | tee -a "$LOG_FILE"
  echo "Sharing on social media..." | tee -a "$LOG_FILE"

  # (Check for actual published posts and share them)
  # This is a placeholder - you'd integrate with actual published content

elif [[ "$TASK_TITLE" =~ [Ww]ord[Pp]ress ]] || [[ "$TASK_TITLE" =~ [Pp]ublish ]]; then
  # WordPress publishing task
  echo "" | tee -a "$LOG_FILE"
  echo "Task Type: WordPress Publishing" | tee -a "$LOG_FILE"

  # Use Vision's publishing script
  /root/.openclaw/workspace/agents/vision/wordpress-publish-with-gateway.sh "$TASK_ID" "$TASK_TITLE" 2>&1 | tee -a "$LOG_FILE"

fi

# ===== WEEKLY ROUTINE (Content Distribution) =====

DAY_OF_WEEK=$(date -u +%A)

if [ "$DAY_OF_WEEK" = "Friday" ]; then
  echo "" | tee -a "$LOG_FILE"
  echo "📊 Weekly Content Distribution..." | tee -a "$LOG_FILE"
  echo "" | tee -a "$LOG_FILE"

  # Get weekly stats
  "$PINCH_TO_POST" stats 2>&1 | tee -a "$LOG_FILE"

  echo "" | tee -a "$LOG_FILE"
  echo "Recommendations:" | tee -a "$LOG_FILE"
  echo "  - Share top performing content on social media" | tee -a "$LOG_FILE"
  echo "  - Plan cross-posting opportunities" | tee -a "$LOG_FILE"
  echo "  - Review engagement metrics" | tee -a "$LOG_FILE"

  # Backup weekly content
  BACKUP_DIR="/root/.openclaw/workspace/backups/weekly-$(date -u +%Y%m%d)"
  "$PINCH_TO_POST" backup "$BACKUP_DIR" 2>&1 | tee -a "$LOG_FILE"
fi

echo "" | tee -a "$LOG_FILE"
echo "✅ Quill workflow complete" | tee -a "$LOG_FILE"
