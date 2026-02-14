# 🚀 Complete Import Guide - Bathroom Products Database

**Last Updated:** 2026-02-11
**Status:** Ready for Execution

---

## 📋 Overview

This guide covers the complete import process for 76 bathroom products into your Supabase database with dual image system for AI-powered product rendering.

**What You Get:**
- 76 products across 3 price tiers (budget/mid/premium)
- 8 product categories
- Dual image system (catalog + render)
- Realistic NL/BE market pricing
- Auto-generated product descriptions
- Supabase Storage integration
- TypeScript service updates for tier filtering

---

## 🎯 Pre-Import Checklist

### Database Access
- [ ] Supabase project URL
- [ ] Database connection string
- [ ] psql client installed

### File Verification
- [ ] `product-catalog-refined.csv` exists (76 products)
- [ ] `image-manifest.csv` exists (218 images)
- [ ] `product-style-tags.csv` exists (654 style tag assignments)
- [ ] Migration SQL files ready

### Environment Setup
- [ ] Supabase CLI installed
- [ ] Storage bucket configured
- [ ] TypeScript files ready to update

---

## 📁 Step 1: Database Schema Migration

**File:** `migrations/add_product_tiers_and_image_paths.sql`

**Purpose:** Add new columns for tier filtering and dual image system

**Run:**
```bash
# Using Supabase CLI
psql -U postgresql://postgres:[PROJECT-REF]@[HOST].supabase.co \
  -f migrations/add_product_tiers_and_image_paths.sql
```

**What It Does:**
1. Adds `price_tier` column (text, NOT NULL, default 'premium')
2. Adds `price_low` and `price_high` columns (numeric)
3. Adds `catalog_image_path` column (text) - for UI catalog image
4. Adds `render_image_path` column (text) - for AI render image
5. Adds `description` column (text, default '')
6. Backfills existing 25 products with `price_tier = 'premium'`
7. Sets price ranges based on tier (budget/mid/premium)
8. Creates index on `(price_tier, category)` for filtering

**Expected Results:**
- All 25 existing products now have `price_tier`, `price_low`, `price_high`
- `price` column still works (backward compatibility)
- New products get all columns populated

---

## 📁 Step 2: Supabase Storage Setup

**File:** `supabase-storage-setup.sql`

**Purpose:** Create storage bucket for product images

**Run:**
```bash
# Using Supabase CLI
supabase storage login --project [PROJECT-REF]
supabase storage execute-file supabase-storage-setup.sql
```

**What It Does:**
1. Creates bucket `product-images` (public read)
2. Sets file size limit: 5MB per file
3. Allows mime types: image/jpeg, image/png, image/webp
4. Creates public read policy (for catalog images)
5. Creates authenticated upload policy (for render images)

**Verification:**
```bash
# Verify bucket created
supabase storage list
```

---

## 📁 Step 3: Separate Catalog vs Render Images

**File:** `separate-catalog-render-images.sh`

**Purpose:** Split 218 images into catalog (lifestyle) and render (product) sets

**Why:** AI needs clean product shots, not lifestyle shots

**Run:**
```bash
cd /root/.openclaw/workspace/research/bathroom-products/raw-images
chmod +x separate-catalog-render-images.sh
./separate-catalog-render-images.sh
```

**What It Does:**
1. Analyzes each image filename/characteristics
2. Detects render-optimized images (clean background, centered product)
3. Moves render images to `product-images-render/`
4. Keeps catalog images in `product-images-catalog/`
5. Creates organized structure by category

**Expected Results:**
- `product-images-catalog/` - 109 catalog images (for UI cards)
- `product-images-render/` - 109 render images (for AI generation)

**Upload to Storage:**
```bash
# Upload both folders
supabase storage cp --recursive product-images-catalog/ project-images/
supabase storage cp --recursive product-images-render/ project-images/
```

---

## 📁 Step 4: Import Product CSV

**File:** `product-catalog-refined.csv`

**Purpose:** Import 76 products with all new fields

**Run:**
```bash
# Using psql with CSV import
psql -U postgresql://postgres:[PROJECT-REF]@[HOST].supabase.co \
  -c "\copy products(id,brand,name,category,price_tier,price_low,price_high,currency,image_url,catalog_image_path,render_image_path,origin,is_active,display_order,description) \
  FROM '/path/to/product-catalog-refined.csv' \
  CSV HEADER \
  ENCODING 'UTF8'"
```

**What It Does:**
- Imports 76 product records
- Populates all new columns (price_tier, price ranges, image paths)
- Sets `origin = 'catalog-2026'`
- Maintains existing `price` column (backward compatible)

**Import Order Matters:** Import style tags FIRST to prevent FK violations!

---

## 📁 Step 5: Import Style Tags

**File:** `product-style-tags.csv`

**Purpose:** Map products to style profiles for AI rendering

**Run:**
```bash
# Using psql with CSV import
psql -U postgresql://postgres:[PROJECT-REF]@[HOST].supabase.co \
  -c "\copy product_style_tags(product_id, style_tag) \
  FROM '/path/to/product-style-tags.csv' \
  CSV HEADER"
```

**What It Does:**
- Creates 654 style tag assignments (2-3 tags per product)
- Links products to style profiles (minimalist, industrial, japandi, etc.)
- Enables AI to apply consistent style per product

---

## 📁 Step 6: Import Image Manifest

**File:** `image-manifest.csv`

**Purpose:** Map local image paths to Supabase Storage paths

**Run:**
```bash
# This is for reference - actual upload via Step 3
# Supabase Storage paths will be: product-images/category/brand-product.webp
```

**Note:** Not required for immediate import (used for upload helper)

---

## 🔧 Step 7: TypeScript Service Updates

### Files to Modify

**1. types.ts**
```typescript
// Add PriceTier union type
export type PriceTier = 'budget' | 'mid' | 'premium';
```

**2. lib/productService.ts**
```typescript
// Update imports
import { PriceTier } from './types';

// Extend DatabaseProduct interface
interface DatabaseProduct {
  // existing fields...
  price_tier?: PriceTier;        // NEW
  price_low?: number;           // NEW
  price_high?: number;          // NEW
  catalog_image_path?: string;  // NEW - Supabase path for catalog image
  render_image_path?: string;   // NEW - Supabase path for render image
}

// Updated fetchAllActiveProducts
export async function fetchAllActiveProducts(
  includeNewCols = true  // SELECT new columns
): Promise<DatabaseProduct[]> {
  const { data, error } = await supabase
    .from('products')
    .select('id, brand, name, category, price_tier, price_low, price_high, currency, image_url, catalog_image_path, render_image_path, origin, is_active, display_order, description');
  
  if (error) throw error;
  return data;
}
```

**3. lib/geminiService.ts**
```typescript
// Updated fetchProductImagesAsBase64
// Now uses render_image_path when available
// Falls back to image_url

// Updated calculateRenovationCost
// Now includes price_low, price_high, price_tier in prompt
```

**4. components/CategoryProductSelector.tsx**
```typescript
// Add tier filter buttons
// Re-fetches products when tier changes

// Price display with ranges
// Now shows: €350 – €450 (using price_low/price_high)
```

**Run:**
```bash
# Copy updated files to your project
cp types.ts /path/to/project/lib/types.ts
cp lib/productService.ts /path/to/project/services/lib/productService.ts
cp lib/geminiService.ts /path/to/project/services/lib/geminiService.ts
cp components/CategoryProductSelector.tsx /path/to/project/components/CategoryProductSelector.tsx
```

---

## ✅ Post-Import Verification

### Check Records
```sql
-- Total products
SELECT COUNT(*) FROM products WHERE is_active = true;

-- By tier
SELECT price_tier, COUNT(*) FROM products GROUP BY price_tier;

-- By category
SELECT category, COUNT(*) FROM products GROUP BY category;

-- Verify dual image system
SELECT COUNT(*) FROM products WHERE catalog_image_path IS NOT NULL AND render_image_path IS NOT NULL;

-- Verify image_url fallback
SELECT COUNT(*) FROM products WHERE image_url IS NOT NULL AND catalog_image_path IS NULL;
```

### Check Supabase Storage
```bash
# List objects in bucket
supabase storage list --bucket product-images

# Verify policies
supabase storage policies list --bucket product-images
```

---

## 🎯 Expected Final State

### Database
- **76 products** with complete tier/price/image data
- **25 existing** + **51 new** products imported
- **Dual image system** working (catalog + render)
- **Price ranges** exact per specification
- **Style tags** assigned for AI consistency

### Supabase Storage
- **218 images** uploaded (109 catalog + 109 render)
- **Organized structure** by category/tier/brand
- **Public RLS** policies configured
- **5MB file limit** set

### Application
- **Tier filtering** working (Budget/Mid/Premium toggle)
- **Price displays** showing ranges (€350 – €450)
- **Category filtering** by product group
- **AI generation** using render_image_path for product shots
- **Cost calculation** accurate with actual prices

---

## 🚀 Quick Start Command

```bash
# 1. Run migration
psql -U postgresql://postgres:[REF]@[HOST].supabase.co -f migrations/add_product_tiers_and_image_paths.sql

# 2. Setup storage
supabase storage login --project [REF]
supabase storage execute-file supabase-storage-setup.sql

# 3. Separate images
cd /root/.openclaw/workspace/research/bathroom-products/raw-images
./separate-catalog-render-images.sh

# 4. Upload images
supabase storage cp --recursive product-images-catalog/ project-images/
supabase storage cp --recursive product-images-render/ project-images/

# 5. Import products (in order!)
psql -U postgresql://postgres:[REF]@[HOST].supabase.co \
  -c "\copy product_style_tags(product_id, style_tag) FROM '/path/to/product-style-tags.csv' CSV HEADER"
  
psql -U postgresql://postgres:[REF]@[HOST].supabase.co \
  -c "\copy products(id,brand,name,category,price_tier,price_low,price_high,currency,image_url,catalog_image_path,render_image_path,origin,is_active,display_order,description) FROM '/path/to/product-catalog-refined.csv' CSV HEADER ENCODING 'UTF8'"

# 6. Verify
psql -U postgresql://postgres:[REF]@[HOST].supabase.co -c "SELECT COUNT(*) FROM products WHERE is_active = true;"
```

---

**All Files Located At:**
`/root/.openclaw/workspace/research/bathroom-products/`

**Ready to execute! 🎉**
