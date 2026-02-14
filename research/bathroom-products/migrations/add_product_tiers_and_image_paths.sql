-- Add product tiers and image path columns
ALTER TABLE products ADD COLUMN price_tier text NOT NULL DEFAULT 'premium';
ALTER TABLE products ADD COLUMN price_low numeric;
ALTER TABLE products ADD COLUMN price_high numeric;
ALTER TABLE products ADD COLUMN catalog_image_path text;
ALTER TABLE products ADD COLUMN render_image_path text;
ALTER TABLE products ADD COLUMN description text NOT NULL DEFAULT '';

-- Backfill price_tier for existing 25 products (set to premium)
UPDATE products
SET price_tier = 'premium'
WHERE price_tier IS NULL;

-- Set price ranges based on tier
UPDATE products
SET price_low = price, price_high = price
WHERE price_tier = 'premium';

UPDATE products
SET price_low = 50, price_high = 150
WHERE price_tier = 'budget';

UPDATE products
SET price_low = 150, price_high = 500
WHERE price_tier = 'mid';

-- Create index for tier filtering
CREATE INDEX idx_products_tier_category ON products(price_tier, category);
