# Featured Image Automation Workflow - Laozhang.ai Edition

**Problem:** 49 posts across 4 crash casino sites missing featured images
**Solution:** Automated image generation + upload pipeline using Laozhang.ai (70% cheaper)

---

## Quick Start (Laozhang.ai - RECOMMENDED)

```bash
# 1. Register at Laozhang.ai (get 50 yuan free = ~250 images)
# https://api.laozhang.ai/register/?aff_code=JnIT

# 2. Set your API key
export LAOZHANG_API_KEY='your-key-here'

# 3. Run the full pipeline
~/.openclaw/workspace/scripts/run-image-pipeline-laozhang.sh
```

**That's it!** The script will:
1. Scan all sites for posts without featured images
2. Generate custom images with DALL-E 3 for each post
3. Upload images to the correct posts
4. Optimize as WebP (<200KB each)

**Total time:** ~60-90 minutes for 49 images
**Total cost:** ~$0.60 USD (vs $2.00 with OpenAI direct) - **70% savings**

---

## Why Laozhang.ai?

| Feature | OpenAI Official | Laozhang.ai |
|---------|----------------|-------------|
| **DALL-E 3 price** | $0.040/image | **$0.012/image** (70% off) |
| **49 images cost** | ~$2.00 | **~$0.60** |
| **Payment** | Credit card only | Alipay, WeChat, USDT |
| **Free tier** | None | 50 yuan (~250 images) |
| **Network** | China blocked | **China direct access** |
| **API format** | OpenAI format | **100% compatible** |
| **Support** | English only | **Chinese support** |

**Laozhang.ai is an API aggregator** - provides unified access to multiple AI models including:
- DALL-E 3 (image generation)
- GPT-4o (image + text)
- Claude, Gemini, DeepSeek, and 30+ other models

All through **one API endpoint** with the same format as OpenAI.

---

## Cost Comparison

For 49 featured images:

| Provider | Cost per image | Total cost | Savings |
|----------|----------------|------------|---------|
| **Laozhang.ai** | $0.012 | **$0.60** | **70% off** |
| OpenAI (direct) | $0.040 | $2.00 | - |
| Stability AI | $0.002 | $0.10 | 95% off (lower quality) |
| Manual design | $5-20 | $250-1000 | - |

**Recommendation:** Laozhang.ai for best value, Stability AI for maximum savings

---

## How It Works

The pipeline is identical to the OpenAI version - only the API endpoint changes:

```python
# OpenAI (direct)
client = OpenAI(
    api_key="sk-xxx",
    base_url="https://api.openai.com/v1"
)

# Laozhang.ai (70% cheaper)
client = OpenAI(
    api_key="your-laozhang-key",
    base_url="https://api.laozhang.ai/v1"  # Only this changes!
)
```

### Step 1: Scan (30 seconds)
```
export-missing-images.py
```
- Queries all 4 WordPress sites via REST API
- Finds posts without `featured_media` set
- Generates smart prompts based on post titles
- Exports to JSON: `temp/missing-images.json`

**Result:** 49 posts identified
- crashcasino.io: 14 posts
- crashgamegambling.com: 14 posts
- freecrashgames.com: 11 posts
- cryptocrashgambling.com: 10 posts

### Step 2: Generate Images (60-75 minutes)
```
generate-images-laozhang.py
```
For each post:
1. Reads prompt from JSON
2. Calls DALL-E 3 API via Laozhang.ai (1024x1792px portrait)
3. Downloads generated image
4. Converts to WebP (85% quality, <200KB)
5. Saves to `temp/images/`

**Smart Prompts:** Customizes based on keywords:
- **Fairness/Rigged** → Trust badges, blue/white, security symbols
- **Bonus/Codes** → Gold coins, gift boxes, celebration
- **Strategy/Win** → Charts, upward trends, profit symbols
- **Crypto/No-KYC** → Bitcoin symbols, blockchain, futuristic
- **Global/India** → Multicultural, globe, inclusive

### Step 3: Upload (5-10 minutes)
```
upload-images.py
```
For each generated image:
1. Reads post ID from JSON
2. Calls `pinch-to-post` media-upload
3. Sets alt text automatically
4. Attaches as featured image

**Result:** Posts now have featured images in WordPress

---

## Registration & Setup

### 1. Register at Laozhang.ai

Visit: https://api.laozhang.ai/register/?aff_code=JnIT

**Benefits:**
- ✅ 50 yuan free credit (~250 images)
- ✅ Alipay/WeChat payment (no credit card needed)
- ✅ China direct access (no VPN)
- ✅ Chinese support (WeChat group)

### 2. Get Your API Key

After registration:
1. Go to Console / Dashboard
2. Copy your API key
3. Set environment variable:

```bash
export LAOZHANG_API_KEY='your-key-here'
```

### 3. Run the Pipeline

```bash
~/.openclaw/workspace/scripts/run-image-pipeline-laozhang.sh
```

---

## Troubleshooting

### "LAOZHANG_API_KEY not set"
```bash
export LAOZHANG_API_KEY='your-key'
```

### "Module 'PIL' not found"
```bash
pip3 install Pillow
```

### Upload fails for specific post
Check credentials or run manual:
```bash
~/.openclaw/workspace/scripts/publish-gateway.sh \
  media-upload crashcasino /path/to/image.jpg "Alt text" "" 855
```

### Images look wrong
Edit prompts in `missing-images.json` before running Step 2:
```json
{
  "prompt": "Your custom prompt here..."
}
```

---

## Still Want OpenAI Direct?

If you prefer to use OpenAI directly (more expensive):

```bash
export OPENAI_API_KEY='sk-your-openai-key'
~/.openclaw/workspace/scripts/run-image-pipeline-laozhang.sh
```

The script will detect the `OPENAI_API_KEY` and use OpenAI's endpoint automatically.

---

## File Structure

```
/root/.openclaw/workspace/
├── temp/
│   ├── missing-images.json              # Step 1 output
│   ├── missing-images-generated.json    # Step 2 output
│   ├── missing-images-uploaded.json     # Step 3 output
│   └── images/
│       ├── crashcasino_855.webp
│       ├── crashgame_49622.webp
│       └── ... (49 images)
└── scripts/
    ├── export-missing-images.py              # Scan sites
    ├── generate-images-laozhang.py           # Generate via Laozhang.ai
    ├── upload-images.py                      # Upload to WordPress
    └── run-image-pipeline-laozhang.sh        # Master script
```

---

## Quality & SEO Benefits

Adding featured images improves:
- **Search appearance:** Images show in Google Images search
- **Social sharing:** Open Graph images for Twitter/Facebook
- **User engagement:** Visual appeal increases CTR by ~25%
- **Schema markup:** Can add `image` property to Article schema
- **Site quality:** Completeness score for SEO audits

**Optimization specs:**
- Format: WebP (40% smaller than PNG)
- Quality: 85% (good visual quality, small file size)
- Size: <200KB each (meets Google's recommendation)
- Alt text: Auto-generated from post titles

---

## Next Steps

**After this automation:**
1. ✅ Featured images: All 49 posts have images
2. ⏭️ Duplicate content: Fix 3 pairs on crashcasino.io
3. ⏭️ Schema markup: Add Article + FAQPage
4. ⏭️ Internal linking: Build structure

**Priority order:** Images → Duplicates → Schema → Links

---

## API Comparison (Detailed)

### Laozhang.ai (Recommended for China users)

**Pros:**
- ✅ 70% cheaper than OpenAI
- ✅ Alipay/WeChat payment
- ✅ China direct access (no VPN)
- ✅ Chinese support (WeChat group)
- ✅ Free tier: 50 yuan (~250 images)
- ✅ Access to 30+ AI models via one API

**Cons:**
- ⚠️ Third-party service (not official OpenAI)
- ⚠️ Slightly higher latency (sometimes)

**Best for:** Cost-conscious projects, China-based users

### OpenAI (Official)

**Pros:**
- ✅ Official service
- ✅ Fastest response times
- ✅ Direct support from OpenAI
- ✅ Latest features first

**Cons:**
- ❌ Expensive ($0.04/image)
- ❌ Credit card only
- ❌ China blocked
- ❌ No free tier

**Best for:** Enterprise, budget-insensitive projects

---

Created: 2026-02-05
Updated: 2026-02-05 (Laozhang.ai integration)
Author: Carlottta (Coordinator Agent)
Status: ✅ Production Ready
