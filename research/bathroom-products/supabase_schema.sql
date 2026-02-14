-- Supabase Table Schema for Sawiday Products
-- Run this first before importing data

-- Create products table
CREATE TABLE IF NOT EXISTS products (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(500) NOT NULL,
  brand VARCHAR(200) NOT NULL,
  price DECIMAL(10, 2) NOT NULL DEFAULT 0,
  category VARCHAR(100) NOT NULL,  -- English: Bathtub, Shower, Faucet, Toilet, Vanity, Lighting
  subcategory VARCHAR(200),  -- e.g., vrijstaande-baden, wastafelkranen
  price_tier VARCHAR(50) NOT NULL DEFAULT 'budget',  -- budget, economy, premium, luxury
  url TEXT UNIQUE NOT NULL,  -- Deduplication key
  primary_image_url TEXT,  -- First/best image (prefer 2000x2000)
  images JSONB,  -- Array of all image URLs
  category_nl VARCHAR(100),  -- Original Dutch category
  scraped_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
CREATE INDEX IF NOT EXISTS idx_products_brand ON products(brand);
CREATE INDEX IF NOT EXISTS idx_products_price_tier ON products(price_tier);
CREATE INDEX IF NOT EXISTS idx_products_price ON products(price);
CREATE INDEX IF NOT EXISTS idx_products_category_brand ON products(category, brand);
CREATE INDEX IF NOT EXISTS idx_products_images ON products USING GIN(images);

-- Enable full-text search on product names
CREATE INDEX IF NOT EXISTS idx_products_name_fts ON products USING GIN(to_tsvector('english', name));

-- Trigger for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_products_updated_at
  BEFORE UPDATE ON products
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- Comments for documentation
COMMENT ON TABLE products IS 'Bathroom products scraped from Sawiday.be';
COMMENT ON COLUMN products.category IS 'English category: Bathtub, Shower, Faucet, Toilet, Vanity, Lighting';
COMMENT ON COLUMN products.images IS 'JSONB array of all product image URLs';
COMMENT ON COLUMN products.primary_image_url IS 'Primary/best image (prefer 2000x2000 from CDN)';
COMMENT ON COLUMN products.price_tier IS 'Auto-calculated tier: budget, economy, premium, luxury (percentile-based)';
COMMENT ON COLUMN products.url IS 'Product URL for deduplication (UNIQUE constraint)';

-- Example query to search products
-- SELECT name, brand, price, category, price_tier, primary_image_url
-- FROM products
-- WHERE category = 'Bathtub' AND price_tier = 'luxury'
-- ORDER BY price DESC;
