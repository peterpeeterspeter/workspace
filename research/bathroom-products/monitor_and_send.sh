#!/bin/bash
# Monitor and send completed scraper files via Telegram

WATCH_DIR="/root/.openclaw/workspace/research/bathroom-products"
SENT_FILES="/root/.openclaw/workspace/research/bathroom-products/sent_files.txt"

# Initialize sent files tracking
touch "$SENT_FILES"

echo "📡 Monitoring for scraper output files..."
echo "Will send via Telegram as each completes"

while true; do
    # Find new JSON files
    for file in "$WATCH_DIR"/*5perbrand*.json; do
        if [ -f "$file" ]; then
            filename=$(basename "$file")

            # Check if already sent
            if ! grep -q "$filename" "$SENT_FILES" 2>/dev/null; then
                echo ""
                echo "📦 New file detected: $filename"

                # Send via Telegram
                /root/.openclaw/workspace/scripts/telegram-send "$file" "📦 Scraper update: $filename"

                if [ $? -eq 0 ]; then
                    echo "  ✅ Sent successfully"
                    echo "$filename" >> "$SENT_FILES"
                else
                    echo "  ❌ Send failed, will retry"
                fi
            fi
        fi
    done

    # Check every 30 seconds
    sleep 30
done
