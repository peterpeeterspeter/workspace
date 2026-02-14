#!/bin/bash
# Master script: Generate and upload featured images for all crash casino sites
# Using Laozhang.ai API (70% cheaper than OpenAI)

set -e  # Exit on error

echo "🎨 Featured Image Pipeline"
echo "=========================="
echo ""

# Check prerequisites
echo "Step 0: Prerequisites"
echo "--------------------"

if [ -z "$LAOZHANG_API_KEY" ] && [ -z "$OPENAI_API_KEY" ]; then
  echo "❌ API key not set"
  echo ""
  echo "Option 1: Laozhang.ai (RECOMMENDED - 70% cheaper)"
  echo "  - Register: https://api.laozhang.ai/register/?aff_code=JnIT"
  echo "  - Get 50 yuan free credit (~250 images)"
  echo "  - Pay via Alipay/WeChat/USDT"
  echo "  - Export: export LAOZHANG_API_KEY='your-key'"
  echo ""
  echo "Option 2: OpenAI (more expensive)"
  echo "  - Cost: \$0.04/image vs \$0.012/image"
  echo "  - Export: export OPENAI_API_KEY='sk-...'"
  echo ""
  exit 1
fi

# Use Laozhang.ai if available
if [ -n "$LAOZHANG_API_KEY" ]; then
  echo "✅ LAOZHANG_API_KEY configured"
  echo "   Provider: Laozhang.ai (70% savings)"
  echo "   Cost: ~\$0.60 for 49 images"
else
  echo "✅ OPENAI_API_KEY configured"
  echo "   Provider: OpenAI (official)"
  echo "   Cost: ~\$2.00 for 49 images"
fi

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
if [ -n "$LAOZHANG_API_KEY" ]; then
  echo "Using Laozhang.ai API (70% cheaper, China-friendly)"
  echo "Cost: ~\$0.012/image (vs OpenAI \$0.04/image)"
else
  echo "Using OpenAI API (official)"
  echo "Cost: ~\$0.04/image"
fi
echo ""
echo "Estimated time: ~1-2 minutes per image"
echo ""

python3 /root/.openclaw/workspace/scripts/generate-images-laozhang.py

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
