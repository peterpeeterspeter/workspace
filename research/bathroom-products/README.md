# Bathroom Product Research Database

**Created:** 2026-02-09  
**Purpose:** EU manufacturer product catalog + Gemini Pro training data  
**Location:** `/root/.openclaw/workspace/research/bathroom-products/`

---

## Directory Structure

```
bathroom-products/
├── raw-images/              # Original high-res images from manufacturers
│   ├── toilets/
│   │   ├── premium/        # €650+ products (Duravit, Villeroy & Boch)
│   │   ├── mid-range/      # €250-€650 (Geberit, Ideal Standard)
│   │   └── budget/         # €100-€250 (basic models)
│   ├── sinks/              # Bathroom sinks/vanities
│   ├── showers/            # Shower cabins, sets
│   └── faucets/            # Taps, mixers, thermostats
│
├── metadata/                # JSON files with product specifications
│   ├── toilets-premium.json
│   ├── toilets-mid-range.json
│   ├── sinks-all.json
│   └── ...
│
├── catalog-ready/           # Web-optimized images (compressed, resized)
│   ├── thumbnails/         # 200x200 for listing pages
│   ├── compressed/         # Optimized for web (max 200KB each)
│   └── web-optimized/      # Display quality (800x800)
│
└── gemini-training/         # Organized by style for AI fine-tuning
    ├── minimalist_modern/   # Clean lines, geometric, white
    ├── classic_elegant/    # Traditional, ornate, curves
    ├── luxury_premium/     # High-end materials, stone, gold accents
    └── budget_functional/  # Simple, basic, functional designs
```

---

## Naming Convention

**Images:** `{manufacturer}-{product}-{category}-{style}-{angle}.{ext}`

**Examples:**
- `duravit-starck3-toilet-modern-front.jpg`
- `villeroy-geoischt-sink-luxury-side.jpg`
- `geberit-aquaclean-shower-modern-installed.jpg`

---

## Metadata Schema

```json
{
  "sku": "DUR-STARCK3-WHITE",
  "name": "Duravit Starck 3 Rimfree Toilet",
  "manufacturer": "Duravit",
  "country": "Germany",
  "category": "toilet",
  "style": "minimalist_modern",
  "price_eur": "650",
  "price_segment": "premium",
  "materials": ["ceramic", "chrome"],
  "colors": ["white"],
  "dimensions": "54x37cm",
  "mounting": "wall_hung",
  "features": ["rimfree", "softclose", "concealed_cistern"],
  "year_introduced": "2023",
  "url": "https://www.duravit.nl/product/starck-3",
  "image_count": 5,
  "image_data": {
    "filename": "duravit-starck3-toilet-modern-front.jpg",
    "resolution": "1200x1200",
    "angle": "front",
    "background": "white_studio"
  }
}
```

---

## Target Manufacturers

### Premium Tier (€650+)
- **Germany:** Duravit, Villeroy & Boch, Grohe
- **Italy:** Ceramica Flaminia, GSI
- **Spain:** Roca

### Mid-Range (€250-€650)
- **Netherlands:** Geberit, Ideal Standard
- **Germany:** Keramag, Hansgrohe
- **International:** Laufen

### Budget (€100-€250)
- House brands
- Basic collections from premium brands

---

## Collection Goals

| Category | Premium | Mid-Range | Budget | Total |
|----------|---------|----------|--------|-------|
| Toilets | 30 | 40 | 30 | 100 |
| Sinks | 25 | 30 | 25 | 80 |
| Showers | 20 | 25 | 25 | 70 |
| Faucets | - | - | - | TBD |
| **TOTAL** | **75** | **95** | **80** | **250+** |

---

## Usage

### For DeBadkamer.com Catalog
1. Images from `catalog-ready/` folder
2. Metadata from `metadata/` JSON files
3. Filter by price_segment, style, manufacturer
4. Display in product comparison pages

### For Gemini Pro Training
1. Use style-labeled folders in `gemini-training/`
2. Metadata includes style tags for prompt engineering
3. High-res originals from `raw-images/`
4. Balanced distribution across styles (avoid bias)

---

## Status

- ✅ Directory structure created
- ✅ Metadata schema defined
- 🔄 Batch 1 (toilets) pending approval
- ⏸️ Batches 2-3 awaiting Batch 1 completion

---

## Next Steps

1. Research Dutch/German manufacturers
2. Browse product catalogs (using browser tool)
3. Extract images + product data
4. Organize by category and price segment
5. Generate metadata JSON files
6. Prepare Gemini training sets by style

---

**Agent:** Carlottta (coordinator)  
**Last Updated:** 2026-02-09 14:13 UTC
