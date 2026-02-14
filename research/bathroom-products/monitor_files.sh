#!/bin/bash
# Monitor and send scraper files

TRACKER="/root/.openclaw/workspace/research/bathroom-products/.files_sent.txt"
touch "$TRACKER"

send_file() {
    local file="$1"
    local filename=$(basename "$file")

    # Skip if already sent
    if grep -qx "$filename" "$TRACKER" 2>/dev/null; then
        return
    fi

    echo ""
    echo "📦 New file ready: $filename"
    ls -lh "$file"

    # Send will be done via message tool
    echo "📤 Ready to send via Telegram"

    # Mark as sent
    echo "$filename" >> "$TRACKER"
}

# Monitoring loop
echo "📡 Monitoring for scraper files..."
echo "Checking every 30 seconds"

while true; do
    for file in /root/.openclaw/workspace/research/bathroom-products/*5perbrand*.json /root/.openclaw/workspace/research/bathroom-products/*ALL*.json; do
        if [ -f "$file" ]; then
            send_file "$file"
        fi
    done
    sleep 30
done
