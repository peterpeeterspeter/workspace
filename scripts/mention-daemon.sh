#!/bin/bash
#
# @Mention Notification Daemon for Mission Control Phase 1
# Scans TASKBOARD_ENHANCED.md for @mentions and routes to agents
#

WORKSPACE="/root/.openclaw/workspace"
TASKBOARD="$WORKSPACE/TASKBOARD_ENHANCED.md"
MENTION_LOG="$WORKSPACE/logs/mentions.log"
LAST_SCAN="$WORKSPACE/logs/.last_mention_scan"

# Ensure log directory exists
mkdir -p "$WORKSPACE/logs"

# Agent session key mapping
declare -A AGENT_SESSIONS=(
    ["Vision"]="agent:main:cron:*"
    ["Fury"]="agent:main:cron:*"
    ["Quill"]="agent:main:cron:*"
    ["Peter"]="agent:main:main"
    ["Carlottta"]="agent:main:main"
)

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$MENTION_LOG"
}

# Function to get last scan timestamp
get_last_scan() {
    if [ -f "$LAST_SCAN" ]; then
        cat "$LAST_SCAN"
    else
        echo "0"
    fi
}

# Function to update last scan timestamp
update_scan_time() {
    date +%s > "$LAST_SCAN"
}

# Function to check if file was modified since last scan
was_modified() {
    local last_scan=$(get_last_scan)
    local file_mtime=$(stat -c %Y "$TASKBOARD" 2>/dev/null || echo "0")
    [ "$file_mtime" -gt "$last_scan" ]
}

# Function to extract @mentions from TASKBOARD
extract_mentions() {
    grep -oE '@[a-zA-Z]+' "$TASKBOARD" 2>/dev/null | sort -u
}

# Function to get context around a mention
get_mention_context() {
    local mention="$1"
    grep -B2 -A2 "$mention" "$TASKBOARD" | head -10
}

# Function to send notification to agent
send_notification() {
    local agent="$1"
    local context="$2"
    local session_key="${AGENT_SESSIONS[$agent]}"

    if [ -z "$session_key" ]; then
        log "ERROR: No session key found for agent $agent"
        return 1
    fi

    # Build notification message
    local message="🔔 **@Mention Notification**

You were mentioned in TASKBOARD:

$context

---

Check TASKBOARD_ENHANCED.md for full context."

    # Send via openclaw sessions_send
    if openclaw sessions send \
        --session "$session_key" \
        --message "$message" 2>/dev/null; then
        log "✓ Notified $agent"
        return 0
    else
        log "✗ Failed to notify $agent"
        return 1
    fi
}

# Main execution
main() {
    log "=== Mention scan started ==="

    # Check if TASKBOARD was modified
    if ! was_modified; then
        log "No changes since last scan, skipping"
        exit 0
    fi

    log "TASKBOARD modified, scanning for mentions..."

    # Extract unique mentions
    mentions=$(extract_mentions)

    if [ -z "$mentions" ]; then
        log "No mentions found"
        update_scan_time
        exit 0
    fi

    # Process each mention
    while IFS= read -r mention; do
        # Remove @ symbol
        agent="${mention#@}"

        # Skip if agent not in mapping
        if [ -z "${AGENT_SESSIONS[$agent]}" ]; then
            log "Skipping unknown agent: $agent"
            continue
        fi

        log "Found mention: $agent"

        # Get context
        context=$(get_mention_context "$mention")

        # Send notification
        send_notification "$agent" "$context"

        # Small delay to avoid overwhelming
        sleep 1
    done <<< "$mentions"

    update_scan_time
    log "=== Mention scan completed ==="
}

# Run main function
main
