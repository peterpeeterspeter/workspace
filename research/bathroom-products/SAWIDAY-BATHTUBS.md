# Sawiday.be Bathtubs - Product Discovery

**Source:** https://www.sawiday.be/nl-be/baden/
**Access:** ✅ Open (no Cloudflare blocks)
**Language:** Dutch (NL)
**Coverage:** Freestanding, built-in, corner, whirlpools

---

## Top Products Found (Popular + Priced)

### Villeroy & Boch (Premium/Luxury)

**1. Villeroy & Boch Libra bad 170x75cm**
- Price: **€797.97**
- Type: Freestanding
- Shape: Rectangular
- Features: Quaryl right-hand, potential wit (white)
- Size: 170cm x 75cm

**2. Villeroy & Boch O.novo bad 180x80cm**
- Price: **€343.95**
- Type: Freestanding
- Shape: Rectangular
- Features: Rechthoekig (right-corner), duo glans wit (white)
- Size: 180cm x 80cm

**3. Villeroy & Boch Oberon 2.0 bad rechthoekig 180x80cm**
- Price: **€689.00**
- Type: Freestanding
- Features: Rechthoekig, duo glans wit (white)
- Size: 180cm x 80cm

### Duravit (Mid-Range to Premium)

**4. Duravit Luv bad ovaal 185x95cm hoek rechts mat wit**
- Price: **€3,819.91**
- Type: Freestanding
- Shape: Oval (Luv = rounded)
- Features: Hoek rechts (right-corner), mat wit (white)
- Size: 185cm x 95cm

**5. Duravit Solidellipse vrijstaand bad 180x88cm**
- Type: Freestanding
- Shape: Solid ellipse (egg-shaped)
- Features: Ovaal solid surface, wit (white)
- Size: 180cm x 88cm

### Riho Bilbao (Entry-Level)

**6. Riho Bilbao Vrijstaand Bad - 170x80cm**
- Price: Not visible in snapshot (likely €200-300 range)
- Type: Freestanding
- Features: Solid surface, mat wit

---

## Categories Available on Sawiday.be

From navigation structure:

1. **Alle baden** (All baths) - `/nl-be/baden/alle-baden/`
2. **Vrijstaande baden** (Freestanding) - `/nl-be/baden/vrijstaande-baden/`
3. **Inbouwbaden** (Built-in) - `/nl-be/baden/inbouwbaden/`
4. **Half vrijstaande baden** (Half freestanding) - `/nl-be/baden/half-vrijstaande-baden/`
5. **Hoekbaden** (Corner baths) - `/nl-be/baden/hoekbaden/`
6. **Whirlpool baden** (Whirlpools) - `/nl-be/baden/whirlpool-baden/`
7. **Bad douche combinatie** (Bath-shower combos) - `/nl-be/baden/bad-douche-combinatie/`

---

## Price Ranges Observed

| Tier | Price Range | Examples |
|-------|-------------|----------|
| **Budget** | €300-500 | O.novo €343.95 |
| **Mid** | €500-1000 | Libra €797.97, Oberon €689.00 |
| **Premium** | €1000-4000 | Duravit Luv €3,819.91 |

---

## Brand Presence

**Strong presence:**
- **Villeroy & Boch** - Most listings, premium pricing
- **Duravit** - High-end models available

**Moderate presence:**
- **Riho** - Entry-level freestanding
- **Bette** - Referenced in footer links

**Limited presence:**
- **Grohe** - Mentioned in navigation
- **Kaldewei** - Has dedicated section
- **Keramag** - Has dedicated section

---

## Next Steps for Full Extraction

### Option A: Manual Category Browsing (Recommended)

Browse each category systematically:
```bash
# Freestanding baths (highest priority)
navigate /nl-be/baden/vrijstaande-baden/
extract: name, brand, price, image_url, features

# Built-in baths
navigate /nl-be/baden/inbouwbaden/
extract: name, brand, price, image_url, features

# Corner baths
navigate /nl-be/baden/hoekbaden/
extract: name, brand, price, image_url, features
```

**Advantages:**
- Sawiday.be is accessible
- Structured data with pricing
- Dutch market focus (perfect for DeBadkamer.com)
- No Cloudflare blocks

**Disadvantages:**
- Manual browsing required
- Time intensive (50+ products × multiple categories)

**Estimated time:** 3-4 hours for complete bathtubs category

---

### Option B: Automated Scraping (If You Want Script)

I can create a targeted scraper for Sawiday.be:
```python
import requests
from bs4 import BeautifulSoup

# Scrape product listings from each category
# Extract: name, price, brand, features, image URLs
# Handle pagination if needed
# Export to CSV/JSON
```

**Advantages:**
- Fast, systematic
- Reusable for other categories (toilets, showers)
- Can handle pagination automatically

**Disadvantages:**
- Requires development time (1-2 hours)
- May trigger rate limiting

---

## Recommendation

**Start with Sawiday.be manual browsing** (Option A) for:
- Immediate data access
- Quality validation (Peter can verify products)
- Dutch market focus

**Then** create automated scraper for:
- Toilets category
- Showers category

**Timeline:**
1. **Bathtubs** from Sawiday.be - 3-4 hours (manual)
2. **Toilets** - 1-2 hours (scrape + manual)
3. **Showers** - 1-2 hours (scrape + manual)

---

## Ready to Proceed?

**Peter, confirm approach:**
- **"manual"** = I browse Sawiday.be categories and extract products
- **"auto"** = I build scraper and automate extraction

I'll begin immediately on your confirmation! 🚀
