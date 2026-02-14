#!/bin/bash
set -e

# Supabase connection details
# Get these from: https://app.supabase.com/project/_/settings/api

# Load environment variables (optional)
# SUPABASE_URL="https://xyzproject.supabase.co"
SUPABASE_KEY="your-anon-key"

# Import products
echo "Importing 2180 products..."
supabase db insert --db-url "$SUPABASE_URL" --db-key "$SUPABASE_KEY" \
  --table=products \
  --file=format=values \
  --data=/root/.openclaw/workspace/research/bathroom-products/data/supabase/products.json

# Import product images
echo "Importing 2180 product images..."
supabase db insert --db-url "$SUPABASE_URL" --db-key "$SUPABASE_KEY" \
  --table=product_images \
  --file=format=values \
  --data=/root/.openclaw/workspace/research/bathroom-products/data/supabase/product_images.json

echo "✓ Import complete!"
