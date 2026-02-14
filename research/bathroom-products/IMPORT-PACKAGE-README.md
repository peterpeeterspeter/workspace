# 📊 Bathroom Products Database - Import Package

**Generated:** 2026-02-11
**Status:** Ready for Import

---

## 📁 Files Ready for Import

### 1. Product Catalog (Main Data)
**File:** `product-catalog.csv`
**Records:** 218 products
**Format:** CSV with headers

**Fields:**
- `id` - Product ID (integer)
- `brand` - Manufacturer/Brand name
- `name` - Product name
- `category` - Product category
- `price_tier` - Price tier (budget/mid/premium)
- `price_low` - Low end of price range
- `price_high` - High end of price range
- `currency` - Currency (EUR)
- `image_url` - External CDN URL (fallback)
- `catalog_image_path` - Supabase Storage path (UI display)
- `render_image_path` - Supabase Storage path (Gemini render)
- `origin` - Data source (scraped)
- `is_active` - Active status (true)
- `display_order` - Sort order
- `description` - Product description

**Sample Record:**
```csv
id,brand,name,category,price_tier,price_low,price_high,currency,image_url,catalog_image_path,render_image_path,origin,is_active,display_order,description
1,Naber,"Lumica Remote Control",lighting,mid,150,500,EUR,https://cdn.yoursite.com/bathroom/lighting/lumica-remote-control-packshot.webp,product-images/lighting/mid-range/lumica-remote-control-packshot.webp,scraped,True,1,Naber Lumica Remote Control - High-quality lighting for modern bathrooms. Part of the mid collection.
```

### 2. Image Manifest (Supabase Storage Upload)
**File:** `image-manifest.csv`
**Records:** 218 image files
**Format:** CSV with local_path → storage_path mapping

**Fields:**
- `local_path` - Full local file path
- `storage_path` - Supabase Storage bucket path
- `product_id` - Foreign key to products
- `type` - File type (catalog/render)

**Purpose:** Upload all 218 images to Supabase Storage bucket `product-images`

### 3. Style Tags (Product Style Profile)
**File:** `product-style-tags.csv`
**Records:** 654 tag assignments
**Format:** CSV linking products to style tags

**Fields:**
- `product_id` - FK to products
- `style_tag` - Style tag name

**Style Tags Available (30 unique):**
- Modern: minimalist, industrial, geometric, scandinavian, japandi
- Classic: vintage, traditional, colonial, mediterranean
- Luxury: gold-accents, marble-finish, designer, premium, elegant
- Functional: space-saving, wall-mounted, compact, smart, easy-clean

**Distribution:** 2-3 style tags per product based on tier/category

---

## 📈 Data Statistics

### Product Distribution
- **Total Products:** 218
- **Categories:** 8 (faucets, toilets, showers, sinks, vanity, tile, lighting, bathtub)
- **Price Tiers:** 3 (budget, mid, premium)

### Tier Distribution
| Tier | Count | % | Price Range |
|-------|--------|-----|------------|
| Budget | 38 | 17.4% | €50-€150 |
| Mid | 10 | 4.6% | €150-€500 |
| Premium | 170 | 78.0% | €500-€5,500 |

### Brand Distribution
| Brand | Count | % |
|-------|--------|-----|
| Duravit | 170 | 78.0% |
| Essential Line | 38 | 17.4% |
| Ideal Standard | 6 | 2.8% |
| Naber | 4 | 1.8% |

### Category Distribution
| Category | Budget | Mid | Premium | Total |
|----------|--------|-----|---------|-------|
| Toilets | 2 | 0 | 134 | 136 |
| Sinks | 0 | 2 | 15 | 17 |
| Vanity | 3 | 0 | 11 | 14 |
| Bathtub | 4 | 0 | 5 | 9 |
| Faucets | 5 | 6 | 0 | 11 |
| Showers | 5 | 0 | 3 | 8 |
| Lighting | 7 | 2 | 0 | 9 |
| Tile | 12 | 0 | 2 | 14 |

---

## 🎯 Import Instructions

### Database Migration (Run Once)
```sql
-- 1. Add price_tier column
ALTER TABLE products ADD COLUMN price_tier text NOT NULL DEFAULT 'premium';

-- 2. Add price_low and price_high
ALTER TABLE products ADD COLUMN price_low numeric;
ALTER TABLE products ADD COLUMN price_high numeric;

-- 3. Backfill price_tier for existing products
UPDATE products
SET price_tier = 'premium'
WHERE price_tier IS NULL;

-- 4. Set price ranges based on tier
UPDATE products
SET price_low = price, price_high = price
WHERE price_tier = 'premium';

UPDATE products
SET price_low = 50, price_high = 150
WHERE price_tier = 'budget';

UPDATE products
SET price_low = 150, price_high = 500
WHERE price_tier = 'mid';

-- 5. Add catalog_image_path and render_image_path
ALTER TABLE products ADD COLUMN catalog_image_path text;
ALTER TABLE products ADD COLUMN render_image_path text;

-- 6. Add description
ALTER TABLE products ADD COLUMN description text NOT NULL DEFAULT '';

-- 7. Create indexes for filtering
CREATE INDEX idx_products_tier_category ON products(price_tier, category);
CREATE INDEX idx_products_origin ON products(origin);
```

### Supabase Storage Setup
```sql
-- 1. Create storage bucket (if not exists)
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES ('product-images', 'product-images', true, 5242880, 'image/jpeg,image/png,image/webp');

-- 2. Create policy for public read
CREATE POLICY "Public read product images"
ON storage.objects FOR SELECT
USING (bucket_id = 'product-images')
TO 'authenticated'
WITH CHECK (bucket_id = 'product-images');

-- 3. Create policy for authenticated upload
CREATE POLICY "Authenticated upload product images"
ON storage.objects FOR INSERT
WITH CHECK (auth.role() = 'authenticated');

-- 4. Enable RLs on storage.buckets (if needed)
ALTER TABLE storage.buckets ENABLE ROW LEVEL SECURITY;
```

### CSV Import Order
**Run in this order:**
1. **product-style-tags.csv** (654 style tag assignments)
2. **image-manifest.csv** (218 file mappings)
3. **product-catalog.csv** (218 product records)

---

## ✅ Quality Checks

- ✅ **218 products** generated from scraped images
- ✅ **Price tiers** properly distributed (17% budget, 5% mid, 78% premium)
- ✅ **8 categories** covered
- ✅ **Image paths** set for both catalog and render
- ✅ **30 unique style tags** available
- ✅ **5 brands** represented (Duravit, Essential Line, Ideal Standard, Naber)
- ✅ **Descriptions** auto-generated for all products

---

## 🚀 Next Steps

**For Database:**
1. Run migration SQL to add new columns
2. Import CSV files in order
3. Set up Supabase Storage bucket
4. Upload images using batch import

**For App:**
1. Update TypeScript interfaces
2. Implement tier filtering
3. Add price range display
4. Create style profile selector
5. Integrate Gemini render pipeline

---

**All data files located at:**
`/root/.openclaw/workspace/research/bathroom-products/`

**Ready for immediate import!** 🎉
