#!/bin/bash
# Simple monitoring script - check for new files and send via Telegram

WATCH_DIR="/root/.openclaw/workspace/research/bathroom-products"
SENT_TRACKER="$WATCH_DIR/.sent_tracker.txt"

mkdir -p "$WATCH_DIR"
touch "$SENT_TRACKER"

echo "📡 Monitoring scraper output..."
echo "Will send files as they complete"

check_and_send() {
    local file="$1"

    # Check if file exists and has content
    if [ ! -f "$file" ] || [ ! -s "$file" ]; then
        return
    fi

    local filename=$(basename "$file")

    # Check if already sent
    if grep -qx "$filename" "$SENT_TRACKER" 2>/dev/null; then
        return
    fi

    echo ""
    echo "📦 New file: $filename"
    echo "   Size: $(ls -lh "$file" | awk '{print $5}')"
    echo "   Sending via Telegram..."

    # Send via message tool
    result=$(python3 <<PYTHON
import sys
sys.path.insert(0, '/root/.local/share/pnpm/global/5/.pnpm/openclaw@2026.1.29_@types+express@5.0.6_devtools-protocol@0.0.1577676/node_modules/openclaw')

try:
    from openclaw_tools import message_tools
    msg = message_tools.send(
        channel='telegram',
        target='peterpeeterspeter',
        path='$file',
        message=f'📦 Scraper complete: {filename}'
    )
    print('SUCCESS')
except Exception as e:
    print(f'ERROR: {e}')
PYTHON
)

    if echo "$result" | grep -q "SUCCESS"; then
        echo "   ✅ Sent"
        echo "$filename" >> "$SENT_TRACKER"
    else
        echo "   ⚠️ Send issue, will retry"
    fi
}

# Monitor loop
while true; do
    for file in "$WATCH_DIR"/*5perbrand*.json "$WATCH_DIR"/*ALL*.json; do
        if [ -f "$file" ]; then
            check_and_send "$file"
        fi
    done

    sleep 15  # Check every 15 seconds
done
