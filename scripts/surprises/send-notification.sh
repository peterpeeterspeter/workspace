#!/bin/bash
#
# Send morning surprise notification to Peter via Telegram
# Called by midnight-surprise.sh after generating content
#

SURPRISE_FILE=$1
SURPRISE_TYPE=$2
DATE=$3

# Extract key info from the surprise file
TITLE=$(head -n 1 "$SURPRISE_FILE" | sed 's/^# //')
FIRST_PARAGRAPH=$(grep -A 5 "## 🎯 Executive Summary" "$SURPRISE_FILE" | tail -4 | head -n 1)

# Create notification message
MESSAGE="🌙 **MIDNIGHT SURPRISE - $SURPRISE_TYPE**

**Date:** $DATE
**File:** $(basename "$SURPRISE_FILE")

$FIRST_PARAGRAPH

📁 **Full report:** \`/root/.openclaw/workspace/midnight-surprises/$(basename "$SURPRISE_FILE")\`

---

🎯 **Action item:** Check the report when you have time. If you want me to dive deeper into anything, just reply!

*Created autonomously while you slept* ✨"

# Send via Telegram using message tool
# Note: This will be called from within the cron job, so we need to use the API directly
# For now, we'll save the notification to a file that gets picked up

echo "$MESSAGE" > "/root/.openclaw/workspace/midnight-surprises/notification-$DATE.txt"

echo "Notification saved: /root/.openclaw/workspace/midnight-surprises/notification-$DATE.txt"
