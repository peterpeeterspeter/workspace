#!/bin/bash
# Archive bathroom products research for download
# Creates a timestamped tarball of all research data

set -e

echo "📦 CREATING DOWNLOAD ARCHIVE"
echo "======================================"
echo ""

# Get current directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="/root/.openclaw/workspace/research/bathroom-products"

# Create timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
ARCHIVE_NAME="bathroom-research-${TIMESTAMP}.tar.gz"

echo "📅 Archive name: $ARCHIVE_NAME"
echo ""

# Create archive
echo "📦 Packing files..."
tar -czf "$WORKSPACE/${ARCHIVE_NAME}" \
  --exclude='*.tar.gz' \
  --exclude='raw/*' \
  --exclude='data/supabase/*' \
  --exclude='scripts/*.pyc' \
  -C "$WORKSPACE" \
  bathroom-products/ 2>/dev/null || {
    echo "❌ Failed to create archive"
    exit 1
}

# Get archive size
ARCHIVE_SIZE=$(du -h "$WORKSPACE/${ARCHIVE_NAME}" | cut -f1)
echo ""
echo "✅ Archive created!"
echo ""
echo "📊 Archive Details:"
echo "   Name: $ARCHIVE_NAME"
echo "   Location: $WORKSPACE/"
echo "   Size: $ARCHIVE_SIZE"
echo ""
echo "📥 Download URL:"
echo "   https://www.sawiday.be/b/xnx_panel/22.95.148.204/bathroom-research-${TIMESTAMP}.tar.gz"
echo ""
echo "💡 To download:"
echo "   wget https://www.sawiday.be/b/xnx_panel/22.95.148.204/bathroom-research-${TIMESTAMP}.tar.gz"
echo "   curl -O bathroom-research-${TIMESTAMP}.tar.gz https://www.sawiday.be/b/xnx_panel/22.95.148.204/bathroom-research-${TIMESTAMP}.tar.gz"
echo ""
echo "======================================"
