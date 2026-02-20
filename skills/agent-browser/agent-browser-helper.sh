#!/bin/bash
#
# agent-browser helper script
# Quick wrapper for common agent-browser commands
#

set -e

COMMAND="$1"
shift
ARGS="$@"

case "$COMMAND" in
  open)
    agent-browser open "$ARGS"
    ;;
  snapshot)
    agent-browser snapshot -i "$ARGS"
    ;;
  click)
    agent-browser click "$ARGS"
    ;;
  fill)
    agent-browser fill "$ARGS"
    ;;
  type)
    agent-browser type "$ARGS"
    ;;
  close)
    agent-browser close "$ARGS"
    ;;
  screenshot)
    agent-browser screenshot "$ARGS"
    ;;
  wait)
    agent-browser wait "$ARGS"
    ;;
  *)
    echo "agent-browser helper"
    echo ""
    echo "Usage: $0 <command> [args]"
    echo ""
    echo "Commands:"
    echo "  open <url>              - Navigate to URL"
    echo "  snapshot                - Get interactive elements"
    echo "  click @ref              - Click element"
    echo "  fill @ref \"text\"       - Fill input"
    echo "  type @ref \"text\"       - Type text"
    echo "  close                   - Close browser"
    echo "  screenshot [path]       - Take screenshot"
    echo "  wait <condition>        - Wait for condition"
    echo ""
    echo "Examples:"
    echo "  $0 open https://example.com"
    echo "  $0 snapshot"
    echo "  $0 click @e1"
    echo "  $0 fill @e2 \"test@example.com\""
    ;;
esac
