#!/usr/bin/env python3
"""Send file to Telegram via OpenClaw message tool"""

import sys
import os

def send_file(file_path):
    """Send file to Peter via Telegram."""
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False

    filename = os.path.basename(file_path)
    print(f"\n📦 Sending: {filename}")
    print(f"   Path: {file_path}")
    print(f"   Size: {os.path.getsize(file_path)} bytes")

    # Import message tool
    sys.path.insert(0, '/root/.local/share/pnpm/global/5/.pnpm/openclaw@2026.1.29_@types+express@5.0.6_devtools-protocol@0.0.1577676/node_modules/openclaw')

    try:
        from openclaw_tools import message_tools
        result = message_tools.send(
            channel='telegram',
            message=f'📦 Scraper output: {filename}',
            path=file_path
        )
        print("   ✅ Sent successfully")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: send_file_telegram.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    send_file(file_path)
