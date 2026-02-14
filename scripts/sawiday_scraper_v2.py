#!/usr/bin/env python3
"""
Sawiday.be Scraper V2 - Updated for current site structure
Scraps all product categories from Sawiday.be

Usage:
    python sawiday_scraper_v2.py --category kranen --limit 200
    python sawaday_scraper_v2.py --category all
"""

import json
import time
import random
import sys
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    print("❌ BeautifulSoup4 not installed. Install with:")
    print("   pip install beautifulsoup4")
    sys.exit(1)

# Sawiday.be category URLs (using subcategory pages with full listings)
CATEGORIES = {
    # Showers
    "douche": "https://www.sawiday.be/nl-be/douche/douchesets/",

    # Faucets
    "kranen": "https://www.sawiday.be/nl-be/kranen/alle-kranen/",

    # Vanities
    "wastafels": "https://www.sawiday.be/nl-be/wastafels/",

    # Mirrors
    "spiegels": "https://www.sawiday.be/nl-be/spiegels/",

    # Tiles
    "tegels": "https://www.sawiday.be/nl-be/tegels/",
}

# Target products per category (from Peter's requirements)
CATEGORY_TARGETS = {
    "douche": 50,
    "kranen": 50,
    "wastafels": 50,
    "spiegels": 50,
    "tegels": 50,
}

# User agents to rotate
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
]

# Request headers (NOTE: Don't include Accept-Encoding - it causes Sawiday to return stripped content)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'nl-NL,nl;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
}

# Rate limiting
REQUEST_DELAY = (3, 6)  # Seconds between requests (conservative)
MAX_RETRIES = 3
REQUEST_TIMEOUT = 30

class SawidayScraperV2:
    def __init__(self, category: str = 'all'):
        self.category = category
        self.all_products = []

        # Output directory
        self.output_dir = Path("/root/.openclaw/workspace/research/bathroom-products/products/raw")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Progress tracking
        self.total_pages = 0
        self.total_products = 0

    def log(self, message: str):
        """Log message with timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")

    def get_page(self, url: str, retry_count: int = 0) -> bytes:
        """Fetch page with retry logic"""
        for attempt in range(MAX_RETRIES):
            try:
                # Random user agent
                headers = HEADERS.copy()
                headers['User-Agent'] = random.choice(USER_AGENTS)

                request = Request(url, headers=headers)
                response = urlopen(request, timeout=REQUEST_TIMEOUT)

                if response.status == 200:
                    return response.read()
                elif response.status == 429:
                    self.log(f"⏳ Rate limited (attempt {attempt + 1}/{MAX_RETRIES})")
                    if attempt < MAX_RETRIES - 1:
                        time.sleep(random.uniform(5, 10))
                        continue
                else:
                    self.log(f"❌ HTTP {response.status} on attempt {attempt + 1}")
                    if attempt < MAX_RETRIES - 1:
                        time.sleep(random.uniform(2, 5))
                    else:
                        return None

            except HTTPError as e:
                self.log(f"❌ Network error: {e}")
                if retry_count < MAX_RETRIES - 1:
                    time.sleep(random.uniform(3, 7))
                else:
                    return None
            except Exception as e:
                self.log(f"❌ Error: {e}")
                if retry_count < MAX_RETRIES - 1:
                    time.sleep(random.uniform(2, 4))
                else:
                    return None
        return None

    def scrape_category(self, category_name: str, category_url: str, limit: int = None, target: int = None):
        """Scrape a single category with optional limit and target"""
        self.log("=" * 60)
        self.log(f"🔍 Scraping category: {category_name}")
        self.log(f"URL: {category_url}")
        if target:
            self.log(f"Target: {target} products")
        self.log(f"Limit: {limit if limit else 'onbeperkt'}")
        self.log("=" * 60)

        products = []
        page = 1

        while True:
            self.log(f"📄 Page {page}: {category_url}")

            html = self.get_page(category_url)
            if not html:
                self.log(f"⚠️ Failed to fetch page {page}")
                break

            soup = BeautifulSoup(html, 'html.parser')

            # Find product tiles (updated selector)
            product_tiles = soup.find_all('div', class_='product-tile-container')

            if not product_tiles:
                self.log(f"⚠️ No products found on page {page}")
                # End of pagination
                break

            self.log(f"📦 Found {len(product_tiles)} products on page {page}")

            for tile in product_tiles:
                product = self.parse_product_tile(tile, category_name)
                if product:
                    products.append(product)

            self.log(f"✅ Page {page} complete: {len(product_tiles)} products")

            # Check if target or limit reached BEFORE fetching next page
            if target and len(products) >= target:
                self.log(f"✅ Reached target of {target} products for {category_name}")
                break
            if limit and len(products) >= limit:
                self.log(f"✅ Reached limit of {limit} products")
                break

            # Only look for next page if we haven't reached target
            if not ((target and len(products) >= target) or (limit and len(products) >= limit)):
                # Check for next page (Sawiday uses ?page=N format)
            pagination = soup.find('ul', class_='pagination')
            if pagination:
                # Look for next page link (data-page attribute greater than current page)
                found_next = False
                page_nums_found = []
                for li in pagination.find_all('li', class_='pag-item'):
                    page_num = li.get('data-page')
                    if page_num:
                        page_nums_found.append(page_num)
                    link = li.find('a')
                    if page_num and link:
                        try:
                            page_int = int(page_num)
                            if page_int == page + 1:  # Next page
                                # Build next URL by adding ?page=N
                                if '?' in category_url:
                                    # Remove existing query string and add new page
                                    base_url = category_url.split('?')[0]
                                    next_url = f"{base_url}?page={page_int}"
                                else:
                                    next_url = f"{category_url}?page={page_int}"
                                self.log(f"  🔗 Found next page: {page_int}")
                                category_url = next_url
                                page = page_int
                                found_next = True
                                break
                        except ValueError:
                            pass
                
                self.log(f"  📋 Pagination pages found: {page_nums_found[:5]}")
                
                if found_next:
                    self.log(f"⏳ Waiting {REQUEST_DELAY[0]}-{REQUEST_DELAY[1]}s before next page...")
                    time.sleep(random.uniform(*REQUEST_DELAY))
                else:
                    self.log(f"✅ End of category {category_name}")
                    break
            else:
                self.log(f"✅ End of category {category_name}")
                break

        self.log(f"📊 Total products in {category_name}: {len(products)}")
        return products

    def parse_product_tile(self, tile, category: str) -> dict:
        """Extract product data from tile"""
        try:
            product = {}

            # Product link element (has most data attributes)
            link_elem = tile.find('a', class_='product-tile')
            if not link_elem:
                link_elem = tile.find('a', href=lambda x: x and '/nl-be/p/' in x)

            if not link_elem:
                return None

            # Product URL
            product['product_url'] = urljoin("https://www.sawiday.be", link_elem.get('href', ''))

            # Product name (from data attribute or text)
            product['name'] = link_elem.get('data-name', '') or link_elem.get('data-ec-name', '')
            if not product['name']:
                # Try to find h3
                h3 = tile.find('h3')
                if h3:
                    product['name'] = h3.get_text(strip=True)
                else:
                    product['name'] = "Unknown Product"

            # Brand (from data attribute)
            product['brand'] = link_elem.get('data-ec-brand', '') or self.extract_brand(product['name'])

            # Price (from data attribute or text)
            price_text = link_elem.get('data-price', '') or link_elem.get('data-ec-price', '')
            if price_text:
                product['price'] = self.parse_price(price_text)
            else:
                # Try to find price element
                price_elem = tile.find(['span', 'div', 'p'], class_=lambda x: x and 'price' in str(x).lower())
                if price_elem:
                    price_text = price_elem.get_text(strip=True)
                    product['price'] = self.parse_price(price_text)
                else:
                    product['price'] = 0.0

            # Description (try to find it)
            desc_elem = tile.find('p', class_=lambda x: x and 'description' in str(x).lower())
            product['description'] = desc_elem.get_text(strip=True) if desc_elem else product['name']

            # Image URL
            img_elem = tile.find('img')
            if img_elem:
                product['image_url'] = img_elem.get('src') or img_elem.get('data-src') or ''
            else:
                # Try picture element
                picture = tile.find('picture')
                if picture:
                    source = picture.find('source')
                    if source:
                        product['image_url'] = source.get('srcset', '').split()[0] if source.get('srcset') else ''
                    else:
                        img_in_picture = picture.find('img')
                        if img_in_picture:
                            product['image_url'] = img_in_picture.get('src', '')

            # Category
            product['category'] = category

            # Product ID (from data attribute)
            product['sawiday_id'] = link_elem.get('data-test-product-id', '') or link_elem.get('data-id', '')

            # Add timestamp
            product['scraped_at'] = time.strftime("%Y-%m-%d %H:%M:%S")

            return product

        except Exception as e:
            self.log(f"⚠️ Error parsing product tile: {e}")
            return None

    def extract_brand(self, text: str) -> str:
        """Extract brand from product name"""
        brands = ['Villeroy & Boch', 'Geberit', 'Grohe', 'GROHE', 'Duravit', 'Hansgrohe', 'HANS GROHE',
                 'Adema', 'Ideal Standard', 'Jika', 'Riho', 'Wiesbaden', 'Hotbath',
                 'Fortifura', 'Kaldewei', 'Huppe', 'Alape', 'Vola', 'Axent',
                 'Dornbracht', 'Crosswater', 'Quooker', 'Paffoni', 'Clou',
                 'Hansa', 'Heimeier', 'Kludi', 'Neoperl', 'Schell',
                 'Villeroy & Boch', 'Ivy', 'Brauer', 'Best Design', 'Plieger']

        for brand in brands:
            if brand.lower() in text.lower():
                return brand
        return "Unknown"

    def parse_price(self, text: str) -> float:
        """Parse price from text"""
        try:
            # Remove currency symbols, spaces, and convert comma to dot
            clean = text.replace('€', '').replace(',', '.').replace('  ', '').strip()
            # Extract first number found
            match = re.search(r'\d+\.?\d*', clean)
            if match:
                return float(match.group())
            return 0.0
        except:
            return 0.0

    def scrape_all(self):
        """Scrape all categories"""
        self.log("🚀 Starting Sawiday Scraper V2")
        self.log("Categories to scrape:")
        for cat, url in CATEGORIES.items():
            self.log(f"  - {cat}: {url}")
        self.log("")

        for category_name, category_url in CATEGORIES.items():
            target = CATEGORY_TARGETS.get(category_name)
            products = self.scrape_category(category_name, category_url, target=target)

            self.all_products.extend(products)

            # Save after each category
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_file = self.output_dir / f"sawiday-{category_name}-{timestamp}.json"

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(products, f, ensure_ascii=False, indent=2)

            self.log(f"💾 Saved {len(products)} products to {output_file}")

            # Rate limit between categories
            if category_name != list(CATEGORIES.keys())[-1]:
                self.log(f"⏳ Waiting 10s before next category...")
                time.sleep(10)

        self.log("=" * 60)

        # Save combined output
        combined_file = self.output_dir / f"sawiday-all-{time.strftime('%Y%m%d_%H%M%S')}.json"

        with open(combined_file, 'w', encoding='utf-8') as f:
            json.dump(self.all_products, f, ensure_ascii=False, indent=2)

        self.log("=" * 60)
        self.log(f"✅ SCRAPING COMPLETE")
        self.log(f"Total products scraped: {len(self.all_products)}")
        self.log(f"Combined output: {combined_file}")

def main():
    if len(sys.argv) < 2:
        print("Gebruik: python sawaday_scraper_v2.py --category <categorie>")
        print("\nBeschikbare categorieën:")
        for cat in CATEGORIES.keys():
            print(f"  - {cat}")
        print("\nOpties:")
        print("  --category <naam>   Categorie om te scrapen (douche, kranen, wastafels, spiegels, tegels, all)")
        print("  --limit <aantal>   Maximaal aantal producten om te scrapen (default: onbeperkt)")
        print("\nVoorbeeld:")
        print("  python sawaday_scraper_v2.py --category kranen --limit 200")
        sys.exit(1)

    category = sys.argv[2] if sys.argv[1] == '--category' else 'all'
    limit = None
    if len(sys.argv) > 3 and sys.argv[3] == '--limit':
        try:
            limit = int(sys.argv[4])
        except ValueError:
            print(f"❌ Error: --limit moet een getal zijn")
            sys.exit(1)

    scraper = SawidayScraperV2(category)

    if category == 'all':
        scraper.scrape_all()
    elif category in CATEGORIES:
        products = scraper.scrape_category(category, CATEGORIES[category], limit)
    else:
        print(f"❌ Unknown category: {category}")
        print(f"Available: {', '.join(CATEGORIES.keys())}")
        sys.exit(1)

if __name__ == '__main__':
    main()
