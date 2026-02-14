#!/bin/bash
# Daily Google Search Console data pull
# Runs at 08:00 UTC every day

cd /root/.openclaw/workspace/google-search-console

echo "[$(date)] Starting GSC data pull..."

# Activate virtual environment and run setup
source venv/bin/activate
python setup.py

echo "[$(date)] GSC data pull complete"
