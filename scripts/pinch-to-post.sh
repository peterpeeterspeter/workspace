#!/bin/bash
# Pinch-to-Post Master Wrapper
# Main interface for all pinch-to-post features

set -e

VERSION="3.1.0"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HELPERS_DIR="${SCRIPT_DIR}/pinch-to-post-helpers"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

show_help() {
  cat << EOF
🦞 Pinch-to-Post v${VERSION}

Usage: pinch-to-post <command> [args]

Publishing Commands:
  publish <site> <post_id>              - Publish article (uses gateway)
  bulk-publish <site> <ids...>          - Publish multiple articles
  cross-post <title> <file> <sites>     - Publish to multiple sites

Content Management:
  calendar <year-month> [site]          - View publishing schedule
  stats [site]                          - Content statistics
  backup <dir> [site]                   - Export all content to markdown
  markdown-to-gutenberg <site> <id> <file> - Convert markdown to Gutenberg blocks

Media & Comments:
  media-upload <site> <file> [alt] [caption] [post_id]
                                        - Upload image with metadata
  comment-moderate <site> <action>      - Moderate comments
                                        - Actions: approve-all, spam-all, show-pending, spam-suspicious

Social Media:
  social-post <platform> <message> [url] - Post to social (twitter, linkedin, mastodon)

Quality & Health:
  health-check <site> <post_id>         - Check article quality score

Sites: crashcasino, crashgame, freecrash, cryptocrash

Examples:
  pinch-to-post publish crashcasino 123
  pinch-to-post bulk-publish crashcasino 100-110
  pinch-to-post calendar 2026-02
  pinch-to-post stats crashcasino
  pinch-to-post media-upload crashcasino image.jpg "Screenshot" "Game play" 123
  pinch-to-post comment-moderate crashcasino spam-suspicious
  pinch-to-post social-post twitter "New article!" "https://crashcasino.io/post"
  pinch-to-post backup /root/backups/2026-02-03

EOF
  exit 0
}

# Check if command provided
if [[ $# -lt 1 ]]; then
  show_help
fi

COMMAND="$1"
shift

case "$COMMAND" in
  publish)
    # Use gateway for single publish
    exec "${SCRIPT_DIR}/publish-gateway.sh" "$@"
    ;;

  health-check)
    # Use gateway for health check
    exec "${SCRIPT_DIR}/publish-gateway.sh" check "$@"
    ;;

  bulk-publish)
    exec "${HELPERS_DIR}/bulk-publish.sh" "$@"
    ;;

  calendar)
    exec "${HELPERS_DIR}/content-calendar.sh" "$@"
    ;;

  stats)
    exec "${HELPERS_DIR}/stats-report.sh" "$@"
    ;;

  backup)
    exec "${HELPERS_DIR}/content-backup.sh" "$@"
    ;;

  media-upload)
    exec "${HELPERS_DIR}/media-upload.sh" "$@"
    ;;

  comment-moderate)
    exec "${HELPERS_DIR}/comment-moderate.sh" "$@"
    ;;

  social-post)
    exec "${HELPERS_DIR}/social-post.sh" "$@"
    ;;

  cross-post)
    exec "${HELPERS_DIR}/cross-post.sh" "$@"
    ;;

  markdown-to-gutenberg)
    exec "${HELPERS_DIR}/markdown-to-gutenberg.sh" "$@"
    ;;

  help|--help|-h)
    show_help
    ;;

  *)
    echo -e "${RED}Unknown command: ${COMMAND}${NC}"
    echo ""
    echo "Run 'pinch-to-post help' for usage"
    exit 1
    ;;
esac
