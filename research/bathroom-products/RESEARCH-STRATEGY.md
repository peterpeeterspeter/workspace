# Bathroom Products Research Strategy

## Goal
Research 50 most popular products per category (toilets, bathtubs, showers) across European brands with prices.

## Categories
1. **Toilets (50 products)**
2. **Bathtubs (50 products)**
3. **Showers (50 products)**

## Target Markets
- Netherlands (primary)
- Germany
- Belgium
- France
- Austria

## Major EU Retailers to Scrape

### Netherlands
- Hornbach (blocking access)
- Bauhaus (may block)
- Karwei (no)
- Praxis (no)
- Gamma (no)
- Beter Bed (specialty)
- Badkamp (specialty)
- Saniweb (Cloudflare)
- Sanitair (NL)
- Douche (specialty)

### Germany
- Hornbach DE
- Obi
- Bauhaus
- Toom Baumarkt

### France
- ManoMano
- Leroy Merlin
- B&Q (UK, may not ship to EU)

### Cross-Border / Online
- Amazon.de/FR/NL
- eBay
- Idealo (price comparison)
- Zoeko (NL price comparison)

## Product Data Required per Product
```json
{
  "name": "Product Name",
  "brand": "Brand Name",
  "category": "toilet|bathtub|shower",
  "price_eur": 299,
  "retailer": "Store Name",
  "url": "https://...",
  "image_url": "https://...",
  "features": ["feature1", "feature2"],
  "popularity_score": 1-50,
  "ean": "optional EAN code"
}
```

## Scraping Challenges Identified
1. **Cloudflare protection** - Most major sites block automated access
2. **JavaScript rendering** - Many sites require JS for product lists
3. **Session management** - Products loaded dynamically
4. **Rate limiting** - Need delays between requests

## Alternative Data Sources
1. **Price comparison sites** - May have APIs or be less protected
2. **Affiliate feeds** - Some programs offer product feeds
3. **Manufacturer catalogs** - Direct from brands (Duravit, Villeroy & Boch, Geberit)
4. **Marketplace aggregators** - Amazon, eBay (easier scraping)

## Execution Strategy

### Phase 1: Manufacturer Direct Research (Most Reliable)
- Duravit (DE) - Already have data from previous research
- Villeroy & Boch (DE/FR)
- Geberit (CH/DE)
- Keramag (DE)
- Laufen (CH)
- ROCA (ES)

### Phase 2: Price Aggregator Scraping
- Ideal.nl
- Beslist.nl
- Amazon.nl/de
- Google Shopping results

### Phase 3: Supplement with Retailer Data
- Use browser automation for 2-3 key retailers per country
- Manual data entry fallback if scraping blocked

## Output Format

### File 1: Product Lists
`/root/.openclaw/workspace/research/bathroom-products/products/raw/`
- `toilets-top50.json`
- `bathtubs-top50.json`
- `showers-top50.json`

### File 2: Image URLs
`/root/.openclaw/workspace/research/bathroom-products/images/`
- `toilets-images.csv`
- `bathtubs-images.csv`
- `showers-images.csv`

### File 3: Metadata
`/root/.openclaw/workspace/research/bathroom-products/metadata/`
- Brand statistics
- Price ranges per category
- Popularity metrics
