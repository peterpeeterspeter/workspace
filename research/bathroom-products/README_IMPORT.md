# Supabase Import for Sawiday Bathroom Products

## Status: ⏳ WAITING FOR SCRAPER TO COMPLETE

The scraper is still running. Run import **after** all categories complete:
- ✅ Baden
- ✅ Douche
- ✅ Kranen
- ⏳ Toiletten (in progress)
- ⏳ Wastafels
- ⏳ Spiegels

## Files Created

1. **`supabase_schema.sql`** - Run this FIRST to create table
   - Creates `products` table
   - Adds indexes for performance
   - Sets up JSONB images column
   - Adds auto-update triggers

2. **`generate_supabase_import.py`** - Generates INSERT statements
   - Reads all `*_5perbrand*.json` files
   - Deduplicates by URL
   - Maps categories (Dutch → English)
   - Calculates price tiers per category
   - Outputs `supabase_import.sql`

3. **`RUN_IMPORT.sh`** - Step-by-step guide

## Quick Start (After Scraping Completes)

```bash
# 1. Create table structure
psql --host=db.YOUR_PROJECT_REF.supabase.co --dbname=postgres \
  -f /root/.openclaw/workspace/research/bathroom-products/supabase_schema.sql

# 2. Generate SQL
cd /root/.openclaw/workspace/research/bathroom-products
python3 generate_supabase_import.py

# 3. Import data
psql --host=db.YOUR_PROJECT_REF.supabase.co --dbname=postgres \
  -f supabase_import_YYYYMMDD_HHMMSS.sql
```

## Features

### Deduplication
- Products deduplicated by URL (UNIQUE constraint)
- Same product from multiple subcategories → stored once

### Category Mapping
| Dutch | English |
|--------|----------|
| Baden | Bathtub |
| Douche | Shower |
| Kranen | Faucet |
| Toiletten | Toilet |
| Wastafels | Vanity |
| Spiegels | Lighting |

### Price Tiers (Per Category)
Calculated from actual data percentiles:
- **Budget**: 0-25th percentile
- **Economy**: 25-50th percentile
- **Premium**: 50-75th percentile
- **Luxury**: 75-100th percentile

### Images
- **`images`**: JSONB array of all image URLs
- **`primary_image_url`**: Best single image
  - Prefers `2000x2000` URLs (high quality)
  - Falls back to first image
  - CDN URLs work directly

## Table Schema

```sql
products (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(500),
  brand VARCHAR(200),
  price DECIMAL(10,2),
  category VARCHAR(100),           -- English
  subcategory VARCHAR(200),      -- Dutch
  price_tier VARCHAR(50),
  url TEXT UNIQUE,
  primary_image_url TEXT,
  images JSONB,
  category_nl VARCHAR(100),
  scraped_at TIMESTAMP,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
```

## Example Product

```json
{
  "name": "Zeza Blend Half vrijstaand bad",
  "brand": "Zeza",
  "price": 1450.00,
  "category_en": "Bathtub",
  "subcategory": "vrijstaande-baden",
  "url": "https://www.sawiday.be/nl-be/p/...",
  "primary_image_url": "https://static.rorix.nl/.../2000x2000/...",
  "images": [
    "https://static.rorix.nl/.../2000x2000/...jpg",
    "https://static.rorix.nl/.../150x150/...jpg"
  ],
  "price_tier": "premium"
}
```

## Monitoring Scraper

Check progress:
```bash
tail -f /root/.openclaw/workspace/research/bathroom-products/scraper_final.log
```

Check for new files:
```bash
ls -lh /root/.openclaw/workspace/research/bathroom-products/*5perbrand*.json
```

## Notes

- Scraper creates incremental files as each subcategory completes
- Import script processes ALL `*_5perbrand*.json` files
- Categories with 0 products are skipped
- Images stored as PostgreSQL JSONB for flexible querying

---

**Created:** 2026-02-13
**Scraper status:** Running
**ETA for completion:** ~30 minutes
