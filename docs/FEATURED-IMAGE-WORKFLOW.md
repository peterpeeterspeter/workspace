# Featured Image Automation Workflow

**Problem:** 49 posts across 4 crash casino sites are missing featured images
**Solution:** Automated image generation + upload pipeline

---

## Quick Start

```bash
# 1. Set your OpenAI API key
export OPENAI_API_KEY='sk-your-key-here'

# 2. Run the full pipeline
~/.openclaw/workspace/scripts/run-image-pipeline.sh
```

**That's it!** The script will:
1. Scan all sites for posts without featured images
2. Generate custom images with DALL-E 3 for each post
3. Upload images to the correct posts
4. Optimize as WebP (<200KB each)

**Total time:** ~60-90 minutes for 49 images
**Total cost:** ~$2 USD (DALL-E 3: $0.04/image)

---

## What's Happening

### Step 1: Scan (30 seconds)
```
export-missing-images.py
```
- Queries all 4 WordPress sites via REST API
- Finds posts without `featured_media` set
- Generates AI prompts based on post titles
- Exports to JSON: `temp/missing-images.json`

**Result:** 49 posts identified
- crashcasino.io: 14 posts
- crashgamegambling.com: 14 posts
- freecrashgames.com: 11 posts
- cryptocrashgambling.com: 10 posts

### Step 2: Generate Images (60-75 minutes)
```
generate-images-from-json.py
```
For each post:
1. Reads prompt from JSON
2. Calls DALL-E 3 API (1024x1792px portrait)
3. Downloads generated image
4. Converts to WebP (85% quality)
5. Saves to `temp/images/`

**Smart Prompts:** The system customizes prompts based on keywords:
- **Fairness/Rigged** → Trust badges, blue/white, security symbols
- **Bonus/Codes** → Gold coins, gift boxes, celebration
- **Strategy/Win** → Charts, upward trends, profit symbols
- **Crypto/No-KYC** → Bitcoin symbols, blockchain, futuristic
- **Global/India** → Multicultural, globe, inclusive

**Optimization:**
- Format: WebP (modern, ~40% smaller than PNG)
- Quality: 85% (good visual quality, small file size)
- Size: <200KB each (meets Google's recommendation)

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

## Alternative APIs

If you don't want to use DALL-E 3, you can switch to:

### Stability AI (Stable Diffusion XL)
```bash
export STABILITY_API_KEY='your-key'
export IMAGE_API='stability'
./run-image-pipeline.sh
```

**Pros:**
- Cheaper (~$0.002/image vs $0.04)
- Faster generation
- More customization

**Cons:**
- Lower quality than DALL-E 3
- Requires more prompt tuning
- May need manual review

---

## Manual Control

If you want to run steps separately:

```bash
# Just scan
python3 ~/.openclaw/workspace/scripts/export-missing-images.py

# Just generate (after scanning)
python3 ~/.openclaw/workspace/scripts/generate-images-from-json.py

# Just upload (after generating)
python3 ~/.openclaw/workspace/scripts/upload-images.py
```

---

## Costs Breakdown

| API | Cost per image | 49 images | Quality | Speed |
|-----|----------------|-----------|---------|-------|
| **DALL-E 3** | $0.04 | ~$2.00 | ⭐⭐⭐⭐⭐ | Slow (~1.5min) |
| **Stability AI** | $0.002 | ~$0.10 | ⭐⭐⭐ | Fast (~15s) |
| **Manual design** | $5-20 | $250-1000 | ⭐⭐⭐⭐⭐ | Very slow |

**Recommendation:** DALL-E 3 for quality, Stability AI for cost savings

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
    ├── export-missing-images.py        # Scan sites
    ├── generate-images-from-json.py    # Generate with DALL-E
    ├── upload-images.py                # Upload to WordPress
    └── run-image-pipeline.sh           # Master script
```

---

## Troubleshooting

### "OPENAI_API_KEY not set"
```bash
export OPENAI_API_KEY='sk-...'
```

### "Module 'PIL' not found"
```bash
pip3 install Pillow
```

### Upload fails for specific post
Check credentials in script or run manual:
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

## Quality Checks

After upload, verify:
- [ ] Images display on frontend
- [ ] Alt text is descriptive
- [ ] File size <200KB (run: `ls -lh temp/images/`)
- [ ] WebP format (not PNG/JPG)

Re-run optimization if needed:
```bash
# Convert all to WebP
cd temp/images
for f in *.png; do convert "$f" "${f%.png}.webp"; done
```

---

## SEO Benefits

Adding featured images improves:
- **Search appearance:** Images show in Google Images
- **Social sharing:** Open Graph images for Twitter/Facebook
- **User engagement:** Visual appeal increases CTR
- **Schema markup:** Can add `image` property to Article schema

**Next steps after images:**
1. Add image schema markup
2. Submit updated sitemap to Google
3. Monitor Google Search Console for image search traffic

---

## Next Steps

**After this automation:**
1. ✅ Featured images: All 49 posts have images
2. ⏭️ Duplicate content: Fix 3 pairs on crashcasino.io
3. ⏭️ Schema markup: Add Article + FAQPage
4. ⏭️ Internal linking: Build structure

**Priority order:** Images → Duplicates → Schema → Links

---

Created: 2026-02-05
Author: Carlottta (Coordinator Agent)
Status: ✅ Production Ready
