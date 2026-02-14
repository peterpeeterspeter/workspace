#!/bin/bash
# WordPress Publisher using Pinch-to-Post (Proper Integration)
# Uses pinch-to-post skill with YAML/table preprocessing

set -e

# Preprocess markdown (strip YAML, convert tables to HTML)
preprocess() {
    python3 /root/.openclaw/workspace/agents/shared/preprocess_markdown.py "$1"
}

# Main publishing function
publish() {
    local md_file="$1"
    local site="${2:-crashcasino.io}"
    local status="${3:-publish}"

    [ ! -f "$md_file" ] && { echo "❌ File not found: $md_file" >&2; return 1; }

    # Extract title
    local title=$(grep -m1 "^# " "$md_file" | sed 's/^# //')
    [ -z "$title" ] && title=$(basename "$md_file" .md)

    echo "=========================================="
    echo "📝 Publishing: $title"
    echo "🌐 Site: $site"
    echo "📊 Status: $status"
    echo "=========================================="

    # Preprocess (strip YAML, convert tables)
    local temp_md=$(mktemp)
    preprocess "$md_file" > "$temp_md"

    # Set multi-site credentials for pinch-to-post
    case "$site" in
        crashcasino.io)
            export WP_SITE_CRASHCASINO_URL="https://crashcasino.io"
            export WP_SITE_CRASHCASINO_USER="peter"
            export WP_SITE_CRASHCASINO_PASS="3vRhtTs2khfdLtTiDFqkdeXI"
            site_name="crashcasino"
            ;;
        cryptocrashgambling.com)
            export WP_SITE_CRYPTOCRASH_URL="https://cryptocrashgambling.com"
            export WP_SITE_CRYPTOCRASH_USER="peter"
            export WP_SITE_CRYPTOCRASH_PASS="R3kQ 6vRA UwYd x7Cn KEtT Pk83"
            site_name="cryptocrash"
            ;;
        crashgamegambling.com)
            export WP_SITE_CRASHGAME_URL="https://crashgamegambling.com"
            export WP_SITE_CRASHGAME_USER="peter"
            export WP_SITE_CRASHGAME_PASS="MioX SygN Xaz6 pK9o RUiK tBMF"
            site_name="crashgame"
            ;;
        freecrashgames.com)
            export WP_SITE_FREECRASH_URL="https://freecrashgames.com"
            export WP_SITE_FREECRASH_USER="peter"
            export WP_SITE_FREECRASH_PASS="F8Mg yZXM qJy4 jQvp BMeZ FoMG"
            site_name="freecrash"
            ;;
        *)
            echo "❌ Unknown site: $site" >&2
            rm -f "$temp_md"
            return 1
            ;;
    esac

    # Call pinch-to-post wp-rest.sh with multi-site support
    local response=$(/root/.openclaw/workspace/skills/pinch-to-post/wp-rest.sh \
        create-post-markdown "$title" "$temp_md" "$status" --site="$site_name")

    local exit_code=$?
    rm -f "$temp_md"

    if [ $exit_code -eq 0 ] && echo "$response" | jq -e '.id' > /dev/null 2>&1; then
        local post_id=$(echo "$response" | jq -r '.id')
        local post_link=$(echo "$response" | jq -r '.link')

        echo ""
        echo "✅ SUCCESS!"
        echo "   Post ID: $post_id"
        echo "   Link: $post_link"

        # Archive if published
        if [ "$status" = "publish" ]; then
            local archive_dir="/root/.openclaw/workspace/drafts/published"
            mkdir -p "$archive_dir"
            cp "$md_file" "$archive_dir/"
            echo "   📦 Archived: $archive_dir/$(basename "$md_file")"
        fi

        return 0
    else
        echo ""
        echo "❌ Publishing failed"
        echo "   Exit code: $exit_code"
        echo "   Response: $response" >&2
        return 1
    fi
}

# If run directly
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    if [ -z "$1" ]; then
        echo "Usage: $0 <markdown-file> [site] [status]"
        echo ""
        echo "Examples:"
        echo "  $0 article.md crashcasino.io publish"
        echo "  $0 article.md cryptocrashgambling.com draft"
        echo ""
        echo "Supported sites:"
        echo "  - crashcasino.io"
        echo "  - cryptocrashgambling.com"
        echo "  - crashgamegambling.com"
        echo "  - freecrashgames.com"
        exit 1
    fi

    publish "$@"
fi
