# Feature Requests - Bathroom Products Project

This file captures user-requested capabilities and desired features for the bathroom products research and transformation pipeline work.

---

## [FEAT-20250213-001] image_downloader

**Logged**: 2025-02-13T17:49:00Z
**Priority**: medium
**Status**: pending
**Area**: utilities

### Requested Capability
Automated image downloader for bathroom product images

### User Context
Transformation pipeline generates `image_download_list.txt` with 152 images (catalog + render pairs). Currently need manual download. Images are high-resolution (2000x2000px) from sawiday.be CDN.

Images need to be:
- Downloaded to `raw-images/` directory
- Organized by product ID
- Renamed with descriptive names (product-model.jpg)
- Optimized for web use (catalog-ready)

### Complexity Estimate
medium

### Suggested Implementation
Create `download_images.py` script:
1. Parse `image_download_list.txt` (format: `product_id|type|url`)
2. Download images with proper User-Agent headers
3. Save to `raw-images/{product_id}/{type}.jpg`
4. Handle errors (404s, timeouts) with retries
5. Add progress bar and concurrent downloads (10-20 concurrent)

Optional: Add resize/optimize step for catalog-ready versions.

### Metadata
- Frequency: first_time
- Related Features: transform_data.py (generates download list)

---

## [FEAT-20250213-002] supabase_importer

**Logged**: 2025-02-13T17:49:00Z
**Priority**: high
**Status**: pending
**Area**: database

### Requested Capability
Supabase database importer for bathroom products CSV

### User Context
Transformation pipeline generates `bathroom_products_import.csv` with 80 products. Need to import into Supabase database for:
- Product catalog website
- Gemini Pro training dataset
- Search and filtering

Database schema needs:
- Products table (id, category, brand, name, price, tier, images)
- Categories table (for normalization)
- Indexes for search

### Complexity Estimate
medium

### Suggested Implementation
Create `import_supabase.py` script:
1. Read CSV with proper type handling
2. Validate data (required fields, price ranges)
3. Connect to Supabase (credentials from .env or CLI args)
4. Create tables if not exist (idempotent schema)
5. Batch insert products (handle duplicates by product_id)
6. Update foreign keys (categories)
7. Verify row count matches CSV

### Metadata
- Frequency: first_time
- Related Features: transform_data.py (generates CSV)

---

