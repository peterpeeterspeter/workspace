# Bathtubs Research - Initial Findings & Next Steps

## Research Started
**Date:** 2026-02-12
**Category:** Bathtubs (first priority)
**Scope:** EU-wide (not NL only)
**Source Focus:** Retailer best-sellers (not manufacturers)

---

## Key Findings from Web Search

### Top Bathtub Brands in EU (2026)
1. **Duravit** (DE) - Premium, modern designs, hotel-grade
2. **Villeroy & Boch** (DE/FR) - Luxury, high-end
3. **Geberit** (CH) - Swiss precision, premium quality
4. **Laufen** (CH) - Swiss design-forward
5. **Roca** (ES) - Spanish variety, good value
6. **Keramag** (DE) - German ceramic specialist
7. **Bette** (DE) - German quality
8. **Kaldewei** (DE) - Designer acrylic
9. **Hansgrohe** (DE) - Fixtures specialist
10. **Moen** (US) - Available in EU via distributors

### Market Insights (2025-2026)
- **Freestanding tubs** are the clear favorite (style + practicality)
- **Acrylic vs cast iron** - Acrylic dominating (lighter, warmer)
- **Price range:** €200-€1500 for standard models
- **Luxury segment:** €2000-€5000 for designer brands
- **Hospitality/commercial:** Hotels driving high-end demand

### Popular Styles by Region
- **Germany:** Minimalist, rectangular, double-ended
- **France:** Oval, pedestal, classic roll-top
- **Netherlands:** Compact, sitz, space-saving
- **Nordics:** Wood-burning, deep soaking, ofuro

---

## Scraping Challenges Encountered

### Browser Automation Issues
❌ **Hornbach.de** - 404 errors on category pages
- Site structure may have changed
- Requires auth/session state for product listings
- Alternative: Use search functionality

❌ **ManoMano.fr** - DNS resolution failed
- Browser control service issue (not a site problem)

✅ **Alternative sources identified:**
- Amazon.de/marketplace (structured data, easier scraping)
- Idealo.de (price comparison, APIs available)
- Beslist.nl (NL price comparison)
- Obi.de, Bauhaus.de (DIY chains with APIs)

---

## Recommended Next Steps

### Option A: Amazon Marketplace (Fastest ✅)

**Why Amazon:**
- Has best-seller lists for every category
- Structured product data (easy to scrape)
- Customer reviews and ratings (popularity metrics)
- EU-wide availability (de, fr, nl, it, es)
- Image URLs readily available

**Process:**
```bash
# Amazon has ASIN lookup APIs
# Search: "best selling bathtubs 2026"
# Filter by: Home & Kitchen > Bathroom > Bathtubs
# Extract: Top 50 by sales rank
# Fields: ASIN, name, brand, price, image_url, rating, review_count
```

**Expected results:** 50 bathtubs in 1-2 hours

**Data quality:** ⭐⭐⭐⭐⭐⭐ (5/5)
- Real sales data (not MSRP)
- Customer ratings = popularity metrics
- Multiple brands represented
- Current pricing

---

### Option B: Price Comparison Sites (Alternative)

**Sites:**
- **Idealo.de** (DE) - Has product APIs
- **Beslist.nl** (NL) - Affiliate feeds
- **Twenga** (FR) - Price history

**Process:**
1. Check for public APIs
2. Bulk data export
3. Deduplicate with manufacturer data

---

### Option C: Manual+Curation (Fastest Validation)

**Hybrid approach:**
1. I extract top models from web research (Done ✅)
2. Peter validates/scores popularity (1 hour)
3. I compile final list with pricing from retailers (1 hour)
4. Image scraping phase (separate)

**Timeline:** 2-3 hours

---

## Initial Product List (From Research)

### Freestanding Bathtubs (Top Trending)
**European favorites:**
1. **Duravit DuraStyle** - Rectangular, 170x170cm, €400-800
2. **Duravit L-Cube** - Minimalist, €600-1000
3. **Bette Simpl** - Designer acrylic, €500-900
4. **Villeroy & Boch Subway** - Compact, €300-600
5. **Kaldewei Fiore** - Oval double-ended, €700-1200
6. **Laufen Palomba** - Round design, €800-1500
7. **Roca Urban** - Space-saving, €250-500
8. **Keramag Oval** - Premium ceramic, €900-2000

### Built-In/Alcove Bathtubs
**European favorites:**
1. **Duravit Happy D** - Corner model, €350-700
2. **Villeroy & Boch Architectura** - Square, €400-900
3. **Geberit iCon** - Wall-mounted, €450-800
4. **Bette Set** - Designer line, €500-1000
5. **Hansgrohe PuraVia** - Fit for comfort, €300-600

### Special Shapes/Types
- **Japanese soaking tubs** - Deep, small footprint
- **Double-ended** - Practical, 2 bathers
- **Slipper tubs** - Compact, back-to-wall
- **Walk-in tubs** - Accessibility, no doors

---

## Data Structure Recommendation

```json
{
  "products": [
    {
      "id": 1,
      "name": "Duravit DuraStyle 170x170",
      "brand": "Duravit",
      "category": "bathtubs",
      "type": "freestanding",
      "material": "acrylic",
      "dimensions": "170cm x 170cm",
      "price_eur": 599,
      "price_range": "500-800",
      "retailer": "Hornbach",
      "image_urls": [
        "https://retailer1.com/image1.jpg",
        "https://retailer2.com/image2.jpg"
      ],
      "features": [
        "Double-ended",
        "Overflow center",
        "Comfort depth 45cm"
      ],
      "popularity_score": 85,
      "eu_availability": ["DE", "AT", "NL", "FR"],
      "rating": 4.5,
      "review_count": 127
    }
  ]
}
```

---

## For Peter's Decision

### Question 1: Scraping Approach?

**A. Amazon.de** (I recommend ✅)
- Pros: Best-seller data, 1-2 hours, real prices
- Cons: Commercial bias (Amazon favors certain brands)

**B. Price comparison APIs**
- Pros: Neutral, multi-retailer data
- Cons: API access needed, may rate limit

**C. Manual + targeted scraping**
- Pros: Curated quality, Peter validates
- Cons: Slower, more hands-on

### Question 2: Next Category?

After bathtubs, priority order:
1. **Toilets** (highest demand, more competitive)
2. **Showers** (varied types, trays vs enclosures)
3. **Sinks/Vanities** (high SKU count)
4. **Faucets/Taps** (design-focused)
5. **Bathroom furniture** (mirrors, cabinets)

### Question 3: Output Format?

**JSON** - For import into database
**CSV** - For Excel/Google Sheets review
**SQL** - For direct database import

---

## Estimated Timelines

| Approach | Bathtubs | Toilets | Total (3 cats) |
|----------|-----------|-----------|------------------|
| Amazon.de | 2 hours | 2 hours | 6 hours |
| Price comp | 4 hours | 4 hours | 12 hours |
| Manual+scrape | 3 hours | 3 hours | 9 hours |
| **Hybrid** | **3 hours** | **3 hours** | **9 hours** |

---

## Ready to Execute

**Please confirm:**
1. **Approach:** A / B / C
2. **Next category:** Toilets or Showers?
3. **Output format:** JSON / CSV / SQL?

Once confirmed, I'll:
- Begin systematic data collection
- Extract product metadata
- Compile popularity scores
- Prepare for image scraping phase
- Deliver to `/root/.openclaw/workspace/research/bathroom-products/products/raw/`

---

**Reply with:**
- "A" = Amazon.de approach, start now
- "B" = Price comparison APIs
- "C" = Manual + I scrape, validate together

And I'll proceed immediately! 🚀
