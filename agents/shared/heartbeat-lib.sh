#!/bin/bash
# Shared heartbeat library for all agents
# Usage: source /root/.openclaw/workspace/agents/shared/heartbeat-lib.sh

# Convex configuration
CONVEX_URL="https://fast-duck-920.convex.cloud"
CONVEX_DEPLOY_KEY="dev:fast-duck-920|eyJ2MiI6ImMwNGVkMzQ5NGE4NzRkNWRhNDM4MDQ4NDc4OWQ4MWY0In0="

# Agent configuration (set by individual heartbeat scripts)
AGENT_ID=""
AGENT_NAME=""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Log with timestamp and agent name
log() {
  local level=$1
  shift
  local message="$@"
  local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
  echo -e "${timestamp} [${AGENT_NAME}] ${level}: ${message}"
}

log_info() {
  log "${BLUE}INFO${NC}" "$@"
}

log_success() {
  log "${GREEN}SUCCESS${NC}" "$@"
}

log_warning() {
  log "${YELLOW}WARNING${NC}" "$@"
}

log_error() {
  log "${RED}ERROR${NC}" "$@"
}

# Query Convex for tasks
convex_query() {
  local function_name=$1
  local args=$2

  cd /root/.openclaw/workspace/mission-control-dashboard
  npx convex run --prod "${function_name}" "${args}" 2>&1 | grep -v "^Ignoring"
}

# Update task in Convex
convex_update_task() {
  local task_id=$1
  local status=$2
  local progress=$3
  local handoff_to=$4

  local args="{\"taskId\": \"${task_id}\", \"status\": \"${status}\""

  if [ -n "$progress" ]; then
    args="${args}, \"progress\": ${progress}"
  fi

  if [ -n "$handoff_to" ]; then
    args="${args}, \"handoffTo\": \"${handoff_to}\""
  fi

  args="${args}}"

  cd /root/.openclaw/workspace/mission-control-dashboard
  npx convex run --prod tasks:updateTask "${args}" 2>&1 | grep -v "^Ignoring"
}

# Check for assigned tasks
check_assigned_tasks() {
  local args="{\"assigneeId\": \"${AGENT_ID}\"}"
  convex_query "tasks:getTasks" "${args}"
}

# Check for notifications
check_notifications() {
  local args="{\"agentId\": \"${AGENT_ID}\"}"
  convex_query "activities/getActivities" "${args}"
}

# Update agent status in Convex (placeholder - would need updateAgentStatus function)
update_agent_status() {
  local status=$1
  log_info "Agent status: ${status}"
  # TODO: Implement updateAgentStatus in Convex
}

# Extract task ID from JSON
extract_task_id() {
  local json=$1
  echo "$json" | jq -r '.[0]._id // empty'
}

# Extract task title from JSON
extract_task_title() {
  local json=$1
  echo "$json" | jq -r '.[0].title // empty'
}

# Extract task description from JSON
extract_task_description() {
  local json=$1
  echo "$json" | jq -r '.[0].description // empty'
}

# Extract task status from JSON
extract_task_status() {
  local json=$1
  echo "$json" | jq -r '.[0].status // empty'
}

# Find first assigned task from JSON array
find_first_assigned_task() {
  local json=$1
  echo "$json" | jq -r '[.[] | select(.status == "assigned")] | .[0] | tostring'
}

# Main heartbeat loop
heartbeat_main() {
  log_info "Heartbeat check"

  # Check for assigned tasks
  local all_tasks=$(check_assigned_tasks)

  if [ "$all_tasks" = "[]" ] || [ -z "$all_tasks" ]; then
    log_info "No tasks. Standing by."
    return 0
  fi

  # Find first task with status "assigned"
  local tasks_json=$(echo "$all_tasks" | jq -r '[.[] | select(.status == "assigned")] | tostring')

  if [ "$tasks_json" = "[]" ] || [ "$tasks_json" = "null" ]; then
    log_info "No assigned tasks (have tasks with other statuses). Standing by."
    return 0
  fi

  # Get first assigned task
  local task_id=$(echo "$all_tasks" | jq -r '[.[] | select(.status == "assigned")] | .[0]._id')
  local task_title=$(echo "$all_tasks" | jq -r '[.[] | select(.status == "assigned")] | .[0].title')
  local task_description=$(echo "$all_tasks" | jq -r '[.[] | select(.status == "assigned")] | .[0].description')
  local task_handoff=$(echo "$all_tasks" | jq -r '[.[] | select(.status == "assigned")] | .[0].handoffTo._id // empty')

  if [ -z "$task_id" ] || [ "$task_id" = "null" ]; then
    log_warning "Could not extract task ID from response"
    return 1
  fi

  log_success "Task assigned: ${task_title}"

  # Update task to IN_PROGRESS
  log_info "Updating task status to IN_PROGRESS"
  convex_update_task "$task_id" "in_progress" "" ""

  # Call agent's work function (must be defined in agent-specific script)
  if declare -f agent_work > /dev/null; then
    log_info "Starting work on task"

    # Run agent work and capture exit code
    if agent_work "$task_id" "$task_title" "$task_description"; then
      # Work completed successfully
      log_success "Task completed: ${task_title}"

      # Update task to DONE
      convex_update_task "$task_id" "done" "100" ""

      # Check if there's a handoff target
      if [ -n "$task_handoff" ] && [ "$task_handoff" != "null" ]; then
        log_info "Handoff to agent: ${task_handoff}"
      fi
    else
      # Work failed
      log_error "Task failed: ${task_title}"
      convex_update_task "$task_id" "blocked" "" ""
    fi
  else
    log_error "agent_work function not defined. Cannot process task."
    return 1
  fi
}
