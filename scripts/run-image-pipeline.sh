#!/bin/bash
# Master script: Generate and upload featured images for all crash casino sites

set -e  # Exit on error

echo "🎨 Featured Image Pipeline"
echo "=========================="
echo ""

# Check prerequisites
echo "Step 0: Prerequisites"
echo "--------------------"

if [ -z "$OPENAI_API_KEY" ]; then
  echo "❌ OPENAI_API_KEY not set"
  echo ""
  echo "Get your API key from: https://platform.openai.com/api-keys"
  echo "Then run:"
  echo "  export OPENAI_API_KEY='sk-...'"
  echo ""
  exit 1
fi

echo "✅ OPENAI_API_KEY configured"
echo ""

# Check if Python requests is available
python3 -c "import requests, PIL" 2>/dev/null || {
  echo "Installing Python dependencies..."
  pip3 install -q requests Pillow
}

echo "✅ Python dependencies ready"
echo ""

# Step 1: Export missing images
echo "Step 1: Scanning for posts without featured images"
echo "---------------------------------------------------"
python3 /root/.openclaw/workspace/scripts/export-missing-images.py

echo ""
echo "Press Enter to continue to image generation..."
read

# Step 2: Generate images
echo ""
echo "Step 2: Generating images with DALL-E 3"
echo "----------------------------------------"
echo "This will take ~1-2 minutes per image"
echo "Cost: ~$0.04 per image (49 images = ~$2 total)"
echo ""

python3 /root/.openclaw/workspace/scripts/generate-images-from-json.py

if [ $? -ne 0 ]; then
  echo ""
  echo "❌ Image generation failed"
  exit 1
fi

echo ""
echo "Press Enter to continue to upload..."
read

# Step 3: Upload images
echo ""
echo "Step 3: Uploading images to WordPress"
echo "-------------------------------------"
python3 /root/.openclaw/workspace/scripts/upload-images.py

echo ""
echo "=========================="
echo "✨ Pipeline complete!"
echo ""
echo "Check your sites to verify images are displaying correctly."
