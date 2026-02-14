# Sawiday Product Images - Download Instructions

## Quick Start

```bash
cd /root/.openclaw/workspace/research/bathroom-products/scripts
bash download_product_images.sh
```

That's it! The script will:
1. Download 2,180 product images from Sawiday.be
2. Save them to `data/images/products/`
3. Show progress with percentage counter
4. Handle errors gracefully (failed downloads won't stop the batch)
5. Save statistics (success/failed counts)

## Expected Output

```
🖼️  SAWIDAY PRODUCT IMAGE DOWNLOADER
======================================

📊 Found 2180 images to download
[10.0%] 218/2180 downloaded...
[20.0%] 436/2180 downloaded...
...
==============================================================================
✅ DOWNLOAD COMPLETE!
Total: 2180
Success: 2158
Failed: 22
📁 Images saved to: .../data/images/products/
==============================================================================

📊 Statistics:
   Total processed: 2180
   Successful: 2158
   Failed: 22
```

## What Happens

**Image Download:**
- Downloads from 2,180 product image URLs
- Uses `product_id` as filename (first 10 chars + counter)
- Saves as `.jpg` (Sawiday images are JPEG)
- Organized in `data/images/products/`
- Progress updates every 10 images

**Error Handling:**
- Skips products without image URLs
- Continues on download errors (doesn't stop batch)
- Reports failed count at end

**Filename Format:** `{product_id}_{count}.jpg`
- Example: `77804155_001.jpg`
- Ensures uniqueness while being traceable

## Troubleshooting

**Downloads stuck?**
- Press Ctrl+C to stop (progress is saved)
- Script logs errors but continues

**Many failures?**
- Check internet connection
- Some URLs may be temporarily unavailable
- Script will report failed count

## After Download

**Images are ready to:**
1. Upload to Supabase storage
2. Import product data to Supabase database
3. Add lifestyle images (separate script)

## Script Location

`/root/.openclaw/workspace/research/bathroom-products/scripts/download_product_images.sh`

## Data Files

- Product data: `data/supabase/products.json` (2,180 products)
- Product images: `data/supabase/product_images.json` (2,180 URLs)
- Output directory: `data/images/products/`
