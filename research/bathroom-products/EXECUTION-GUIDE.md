# Sawiday.be Scraper - Execution Guide

## Status: ✅ READY TO SCRAPE

**Created:** `sawiday_browser_scraper.py` (Selenium-based, handles JavaScript)

---

## Quick Start Commands

### 1. Install Dependencies (One-time)
```bash
pip install selenium webdriver-manager
```

### 2. Test Scraper
```bash
# Quick test on one category
python sawiday_browser_scraper.py --category vrijstaande --export json --delay 5.0
```

### 3. Full Production Run

#### Option A: One Category (Testing)
```bash
# Freestanding baths (highest priority)
python sawiday_browser_scraper.py --category vrijstaande --export json --delay 3.0
```

#### Option B: All Categories (Complete)
```bash
# All 6 categories (will take 2-3 hours)
python sawiday_browser_scraper.py --category alle --export json --delay 3.0
```

---

## What the Scraper Does

1. **Launches Chrome browser** (headless, no sandbox)
2. **Navigates to category URL**
3. **Waits for products to load** (AJAX rendering)
4. **Extracts from each product tile:**
   - Product name
   - Brand (from text or link)
   - Price (EUR)
   - Features (bulleted list)
   - Product URL
   - Image URL
5. **Handles pagination:**
   - Clicks "next" button
   - Waits for next page
   - Scrapes all pages
6. **Handles errors gracefully:**
   - Rate limiting delays
   - Network retries
   - Missing data logging
7. **Saves progress:**
   - Incremental JSON saves
   - Can resume if interrupted
8. **Exports to JSON:**
   - `sawiday-bathtubs-{timestamp}.json`
   - Complete metadata (source, scrape date, totals)

---

## Categories Available

All 6 Sawiday.be bathtub categories:
1. **alle** (all products)
2. **vrijstaande** (freestanding)
3. **inbouw** (built-in)
4. **half-vrijstaande** (half freestanding)
5. **hoek** (corner)
6. **whirlpool** (whirlpools)
7. **douche** (bath-shower combos)

---

## Output Format

Each product includes:
```json
{
  "name": "Villeroy & Boch Libra bad 170x75cm",
  "brand": "Villeroy & Boch",
  "category": "bathtubs",
  "price_eur": 797.97,
  "url": "https://www.sawiday.be/nl-be/p/16161/...",
  "image_url": "https://cdn.sawiday.be/...",
  "features": ["quaryl rechthoekig met poten wit", "badkuipvorm: inbouw", "afmetingen: 170x75cm"],
  "popularity_score": 101
}
```

---

## Next Steps (After Scraping)

1. **Review output JSON** - Check for quality
2. **Deduplicate** - Remove exact duplicates
3. **Add missing fields** - EAN, dimensions, materials
4. **Image scraping** - Download images from URLs
5. **Import to database** - Load into DeBadkamer.com

---

## Estimated Time

| Category | Pages | Time |
|-----------|-------|------|
| Freestanding | ~5-8 | 20-30 min |
| Built-in | ~3-5 | 15-20 min |
| All 6 | ~15-20 | 1.5-2 hours |

---

## 💡 Tips

**Start with one category first** (vrijstaande) to test scraper
**Monitor first run** - Check extracted data quality
**Use --delay flag** - Increase delay if Sawiday blocks requests
**Save progress files** - Scraper saves incremental progress

---

**Ready to execute? Run:**

```bash
cd /root/.openclaw/workspace/research/bathroom-products/scrapers
python sawiday_browser_scraper.py --category vrijstaande --export json --delay 3.0 2>&1
```

**This will:**
- Launch headless Chrome
- Scrape freestanding baths
- Extract 50+ products
- Save to JSON
- **~20-30 minutes execution time**

---

**Want me to run it now?** Just confirm!
