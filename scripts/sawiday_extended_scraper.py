#!/usr/bin/env python3
"""
Sawiday.be Extended Scraper - All Bathroom Categories
Scraps all product categories from Sawiday.be

Usage:
    python sawiday_extended_scraper.py --category baden --limit 200
    python sawiday_extended_scraper.py --category all
"""

import json
import time
import random
import sys
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    print("❌ BeautifulSoup4 not installed. Install with:")
    print("   pip install beautifulsoup4")
    sys.exit(1)

# Sawiday.be category URLs
CATEGORIES = {
    # Bathtubs (already scraped)
    "baden": "https://www.sawiday.be/nl-be/baden/alle-baden/",

    # Toilets (already scraped)
    "toiletten": "https://www.sawiday.be/nl-be/toiletten/",

    # Missing categories - NEED TO SCRAPE
    "douche": "https://www.sawiday.be/nl-be/douche/",
    "kranen": "https://www.sawiday.be/nl-be/kranen/",
    "wastafels": "https://www.sawiday.be/nl-be/wastafels/",
    "spiegels": "https://www.sawiday.be/nl-be/spiegels/",
    "tegels": "https://www.sawiday.be/nl-be/tegels/",
}

# User agents to rotate
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
]

# Request headers
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'nl-NL,nl;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
}

# Rate limiting
REQUEST_DELAY = (2, 4)  # Seconds between requests
MAX_RETRIES = 3
REQUEST_TIMEOUT = 30

class SawidayExtendedScraper:
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

    def get_page(self, url: str, retry_count: int = 0) -> str:
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

    def scrape_category(self, category_name: str, category_url: str, limit: int = None):
        """Scrape a single category with optional limit"""
        self.log("=" * 60)
        self.log(f"🔍 Scraping category: {category_name}")
        self.log(f"URL: {category_url}")
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

            # Find product cards (adjust selector based on actual HTML structure)
            product_cards = soup.find_all('div', class_='product-item')

            if not product_cards:
                self.log(f"⚠️ No products found on page {page}")
                # Try alternative selectors
                product_cards = soup.find_all('article', class_='product')

                if not product_cards:
                    self.log(f"⚠️ No products found - trying next page or finished")
                    break

            self.log(f"📦 Found {len(product_cards)} products on page {page}")

            for card in product_cards:
                product = self.parse_product_card(card, category_name)
                if product:
                    products.append(product)

            self.log(f"✅ Page {page} complete: {len(product_cards)} products")

            # Check if limit reached
            if limit and len(products) >= limit:
                self.log(f"✅ Reached limit of {limit} products")
                break

            # Check for next page
            next_link = soup.find('a', class_='next')
            if not next_link:
                self.log(f"✅ End of category {category_name}")
                break
            else:
                category_url = urljoin(category_url, next_link.get('href'))
                page += 1
                time.sleep(random.uniform(*REQUEST_DELAY))

        self.log(f"📊 Total products in {category_name}: {len(products)}")
        return products

    def parse_product_card(self, card, category: str) -> dict:
        """Extract product data from card"""
        try:
            product = {}

            # Product name
            name_elem = card.find('h2') or card.find('h3') or card.find('a', class_='product-name')
            product['name'] = name_elem.get_text(strip=True) if name_elem else "Unknown Product"

            # Brand
            brand_elem = card.find('span', class_='brand')
            product['brand'] = brand_elem.get_text(strip=True) if brand_elem else self.extract_brand(product['name'])

            # Price
            price_elem = card.find('span', class_='price')
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                product['price'] = self.parse_price(price_text)

            # Description
            desc_elem = card.find('div', class_='description')
            product['description'] = desc_elem.get_text(strip=True) if desc_elem else ""

            # Image URL
            img_elem = card.find('img')
            product['image_url'] = img_elem.get('src') or img_elem.get('data-src') if img_elem else ""

            # Product URL
            link_elem = card.find('a', class_='product-link')
            product['product_url'] = link_elem.get('href') if link_elem else ""

            # Category
            product['category'] = category

            # Add timestamp
            product['scraped_at'] = time.strftime("%Y-%m-%d %H:%M:%S")

            return product

        except Exception as e:
            self.log(f"⚠️ Error parsing product card: {e}")
            return None

    def extract_brand(self, text: str) -> str:
        """Extract brand from product name"""
        brands = ['Villeroy & Boch', 'Geberit', 'Grohe', 'Duravit', 'Hansgrohe',
                 'Adema', 'Ideal Standard', 'Jika', 'Riho', 'Wiesbaden', 'Hotbath',
                 'Fortifura', 'Kaldewei', 'Huppe', 'Alape', 'Vola', 'Axent']

        for brand in brands:
            if brand.lower() in text.lower():
                return brand
        return "Unknown"

    def parse_price(self, text: str) -> float:
        """Parse price from text"""
        try:
            # Remove currency symbols, spaces, and convert comma to dot
            clean = text.replace('€', '').replace(',', '.').replace('  ', '').strip()
            return float(clean)
        except:
            return 0.0

    def scrape_all(self):
        """Scrape all missing categories"""
        categories_to_scrape = {
            'douche': CATEGORIES['douche'],
            'kranen': CATEGORIES['kranen'],
            'wastafels': CATEGORIES['wastafels'],
            'spiegels': CATEGORIES['spiegels'],
            'tegels': CATEGORIES['tegels'],
        }

        self.log("🚀 Starting Sawiday Extended Scraper")
        self.log("Categories to scrape:")
        for cat, url in categories_to_scrape.items():
            self.log(f"  - {cat}: {url}")
        self.log("")

        for category_name, category_url in categories_to_scrape.items():
            products = self.scrape_category(category_name, category_url)

            self.all_products.extend(products)

            # Save after each category
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_file = self.output_dir / f"sawiday-{category_name}-{timestamp}.json"

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(products, f, ensure_ascii=False, indent=2)

            self.log(f"💾 Saved {len(products)} products to {output_file}")

            # Rate limit between categories
            time.sleep(random.uniform(5, 10))

        self.log("=" * 60)

        # Save combined output
        combined_file = self.output_dir / f"sawiday-all-missing-{time.strftime('%Y%m%d_%H%M%S')}.json"

        with open(combined_file, 'w', encoding='utf-8') as f:
            json.dump(self.all_products, f, ensure_ascii=False, indent=2)

        self.log("=" * 60)
        self.log(f"✅ SCRAPING COMPLETE")
        self.log(f"Total products scraped: {len(self.all_products)}")
        self.log(f"Combined output: {combined_file}")

def main():
    if len(sys.argv) < 2:
        print("Gebruik: python sawiday_extended_scraper.py --category <categorie>")
        print("\nBeschikbare categorieën:")
        for cat in CATEGORIES.keys():
            print(f"  - {cat}")
        print("\nOpties:")
        print("  --category <naam>   Categorie om te scrapen (baden, douche, kranen, wastafels, spiegels, tegels, all)")
        print("  --limit <aantal>   Maximaal aantal producten om te scrapen (default: onbeperkt)")
        print("\nVoorbeeld:")
        print("  python sawiday_extended_scraper.py --category douche --limit 200")
        sys.exit(1)

    category = sys.argv[2] if sys.argv[1] == '--category' else 'all'
    limit = None
    if len(sys.argv) > 3 and sys.argv[3] == '--limit':
        try:
            limit = int(sys.argv[4])
        except ValueError:
            print(f"❌ Error: --limit moet een getal zijn")
            sys.exit(1)

    scraper = SawidayExtendedScraper(category)

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
