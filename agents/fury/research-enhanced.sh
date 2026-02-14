#!/bin/bash
# Fury's Enhanced Research & Editing Workflow
# Uses ALL pinch-to-post features for full automation

TASK_ID=$1
TASK_TITLE=$2
TASK_DESCRIPTION="${3:-}"

# Pinch-to-Post wrapper
PINCH_TO_POST="/root/.openclaw/workspace/scripts/pinch-to-post.sh"

# Log setup
LOG_DIR="/root/.openclaw/workspace/tasks/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/${TASK_ID}.log"

echo "=== $(date '+%Y-%m-%d %H:%M:%S') ===" | tee -a "$LOG_FILE"
echo "Fury: Enhanced Research & Editing (FULL PINCH-TO-POST INTEGRATION)" | tee -a "$LOG_FILE"
echo "Task: ${TASK_TITLE}" | tee -a "$LOG_FILE"

# ===== DAILY ROUTINE (Comment Moderation) =====

echo "" | tee -a "$LOG_FILE"
echo "💬 Daily Comment Moderation..." | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# Moderate comments across all sites
for site in crashcasino crashgame freecrash cryptocrash; do
  echo "[$site] Checking for spam..." | tee -a "$LOG_FILE"

  # Auto-filter suspicious comments
  "$PINCH_TO_POST" comment-moderate "$site" spam-suspicious 2>&1 | tee -a "$LOG_FILE"

  echo "" | tee -a "$LOG_FILE"
done

# ===== TASK WORK =====

# Determine task type
if [[ "$TASK_TITLE" =~ [Ss][Ee][Rr][Pp] ]] || [[ "$TASK_TITLE" =~ [Cc]ompetitor ]]; then
  # SERP/Competitor analysis
  echo "" | tee -a "$LOG_FILE"
  echo "Task Type: SERP/Competitor Analysis" | tee -a "$LOG_FILE"

  # Get stats for competitive analysis
  echo "" | tee -a "$LOG_FILE"
  echo "Current Site Statistics (for competitive analysis):" | tee -a "$LOG_FILE"
  "$PINCH_TO_POST" stats 2>&1 | tee -a "$LOG_FILE"

  # (Your existing SERP analysis logic here)

elif [[ "$TASK_TITLE" =~ [Kk]eyword ]]; then
  # Keyword research
  echo "" | tee -a "$LOG_FILE"
  echo "Task Type: Keyword Research" | tee -a "$LOG_FILE"

  # (Your existing keyword research logic here)

  # After keyword research, provide recommendations
  echo "" | tee -a "$LOG_FILE"
  echo "💡 Content Opportunities Based on Keywords:" | tee -a "$LOG_FILE"

  # Check calendar for gaps
  TODAY=$(date -u +%Y-%m)
  echo "Check calendar: pinch-to-post calendar $TODAY" | tee -a "$LOG_FILE"

elif [[ "$TASK_TITLE" =~ [Rr]esearch ]] || [[ "$TASK_TITLE" =~ [Aa]nalysis ]]; then
  # General research
  echo "" | tee -a "$LOG_FILE"
  echo "Task Type: General Research" | tee -a "$LOG_FILE"

  # Backup content for analysis
  echo "" | tee -a "$LOG_FILE"
  echo "Backing up content for analysis..." | tee -a "$LOG_FILE"

  BACKUP_DIR="/root/.openclaw/workspace/backups/analysis-$(date -u +%Y%m%d-%H%M%S)"
  "$PINCH_TO_POST" backup "$BACKUP_DIR" 2>&1 | tee -a "$LOG_FILE"

  echo "Analysis backup complete: $BACKUP_DIR" | tee -a "$LOG_FILE"

  # (Your existing research logic here)

elif [[ "$TASK_TITLE" =~ [Ww]ord[Pp]ress ]] || [[ "$TASK_TITLE" =~ [Pp]ublish ]]; then
  # WordPress publishing task
  echo "" | tee -a "$LOG_FILE"
  echo "Task Type: WordPress Publishing" | tee -a "$LOG_FILE"

  # Use Vision's publishing script
  /root/.openclaw/workspace/agents/vision/wordpress-publish-with-gateway.sh "$TASK_ID" "$TASK_TITLE" 2>&1 | tee -a "$LOG_FILE"

fi

# ===== WEEKLY ROUTINE (Competitor Monitoring) =====

DAY_OF_WEEK=$(date -u +%A)

if [ "$DAY_OF_WEEK" = "Monday" ]; then
  echo "" | tee -a "$LOG_FILE"
  echo "🔍 Weekly Competitor Analysis..." | tee -a "$LOG_FILE"
  echo "" | tee -a "$LOG_FILE"

  # Get full stats across all sites
  "$PINCH_TO_POST" stats 2>&1 | tee -a "$LOG_FILE"

  echo "" | tee -a "$LOG_FILE"
  echo "Recommendations:" | tee -a "$LOG_FILE"
  echo "  - Review competitor content strategies" | tee -a "$LOG_FILE"
  echo "  - Identify content gaps" | tee -a "$LOG_FILE"
  echo "  - Check for new keyword opportunities" | tee -a "$LOG_FILE"

  # Backup for analysis
  BACKUP_DIR="/root/.openclaw/workspace/backups/weekly-$(date -u +%Y%m%d)"
  "$PINCH_TO_POST" backup "$BACKUP_DIR" 2>&1 | tee -a "$LOG_FILE"
fi

echo "" | tee -a "$LOG_FILE"
echo "✅ Fury workflow complete" | tee -a "$LOG_FILE"
