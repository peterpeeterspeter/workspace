#!/bin/bash
#
# Enhanced @Mention Notification Daemon for Mission Control Phase 2
# Polls JSON database for undelivered notifications and routes to agents
#

WORKSPACE="/root/.openclaw/workspace"
DB="$WORKSPACE/mission-control.db.json"
LOG="$WORKSPACE/logs/notification-daemon.log"

# Ensure log directory exists
mkdir -p "$WORKSPACE/logs"

# Agent session key mapping
declare -A AGENT_SESSIONS=(
    ["vision"]="agent:main:cron:*"
    ["fury"]="agent:main:cron:*"
    ["quill"]="agent:main:cron:*"
    ["peter"]="agent:main:main"
    ["carlottta"]="agent:main:main"
)

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG"
}

# Function to check if database exists
check_db() {
    if [ ! -f "$DB" ]; then
        log "ERROR: Database not found at $DB"
        return 1
    fi
    return 0
}

# Function to extract undelivered notifications
get_undelivered_notifications() {
    # Use jq to parse JSON and find undelivered notifications
    if command -v jq &> /dev/null; then
        jq -r '.notifications[] | select(.delivered == false) | .id' "$DB"
    else
        # Fallback: grep for undelivered (less reliable)
        grep -oP '"id":\s*"\K[^"]+' "$DB" | while read id; do
            # Check if delivered is false (simplified check)
            if grep -A5 "\"id\": \"$id\"" "$DB" | grep -q '"delivered": false'; then
                echo "$id"
            fi
        done
    fi
}

# Function to get notification details
get_notification() {
    local notif_id="$1"

    if command -v jq &> /dev/null; then
        jq -r ".notifications[] | select(.id == \"$notif_id\")" "$DB"
    else
        log "ERROR: jq not installed. Cannot parse notification details"
        return 1
    fi
}

# Function to send notification to agent
send_notification() {
    local notif_id="$1"
    local agent_id="$2"
    local content="$3"
    local task_id="$4"

    local session_key="${AGENT_SESSIONS[$agent_id]}"

    if [ -z "$session_key" ]; then
        log "ERROR: No session key found for agent $agent_id"
        return 1
    fi

    # Build notification message
    local message="🔔 **Mission Control Notification**

$content

---

Check mission-control for details."

    # Send via openclaw sessions_send
    if openclaw sessions send \
        --session "$session_key" \
        --message "$message" 2>/dev/null; then
        log "✓ Notified @$agent_id (notification: $notif_id)"
        mark_delivered "$notif_id"
        return 0
    else
        log "✗ Failed to notify @$agent_id (notification: $notif_id)"
        return 1
    fi
}

# Function to mark notification as delivered
mark_delivered() {
    local notif_id="$1"

    if command -v jq &> /dev/null; then
        # Update notification in JSON
        local temp_db="${DB}.tmp"
        local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

        jq "(.notifications[] | select(.id == \"$notif_id\")) |=
            (.delivered = true | .delivered_at = \"$timestamp\")" "$DB" > "$temp_db"

        if [ $? -eq 0 ]; then
            mv "$temp_db" "$DB"
            log "✓ Marked notification $notif_id as delivered"
        else
            log "ERROR: Failed to mark notification $notif_id as delivered"
            rm -f "$temp_db"
        fi
    else
        log "ERROR: jq not installed. Cannot mark notification as delivered"
    fi
}

# Main execution
main() {
    log "=== Notification daemon started ==="

    # Check if database exists
    if ! check_db; then
        exit 1
    fi

    # Check if jq is installed
    if ! command -v jq &> /dev/null; then
        log "WARNING: jq not installed. Installing..."
        if command -v apt-get &> /dev/null; then
            apt-get update -qq && apt-get install -y -qq jq
        elif command -v yum &> /dev/null; then
            yum install -y -q jq
        else
            log "ERROR: Cannot install jq. Please install manually."
            exit 1
        fi
    fi

    # Get undelivered notifications
    notif_ids=$(get_undelivered_notifications)

    if [ -z "$notif_ids" ]; then
        log "No undelivered notifications found"
        exit 0
    fi

    log "Found $(echo "$notif_ids" | wc -l) undelivered notifications"

    # Process each notification
    while IFS= read -r notif_id; do
        log "Processing notification: $notif_id"

        # Get notification details
        notif_json=$(get_notification "$notif_id")

        if [ -z "$notif_json" ]; then
            log "ERROR: Could not retrieve notification $notif_id"
            continue
        fi

        # Extract fields
        agent_id=$(echo "$notif_json" | jq -r '.mentioned_agent_id')
        content=$(echo "$notif_json" | jq -r '.content')
        task_id=$(echo "$notif_json" | jq -r '.task_id // empty')

        # Send notification
        send_notification "$notif_id" "$agent_id" "$content" "$task_id"

        # Small delay to avoid overwhelming
        sleep 1
    done <<< "$notif_ids"

    log "=== Notification daemon completed ==="
}

# Run main function
main
