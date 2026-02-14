#!/usr/bin/env python3
"""
Sawiday.be scraper for specific subcategories
Target: 50 douchesets, 25 complete-douchecabines, 10 infrarood, 10 stoomcabines
"""

import json
import os
import time
from pathlib import Path

# Firecrawl API
try:
    from firecrawl import FirecrawlApp
except ImportError:
    print("❌ Firecrawl not installed. Install with:")
    print("   pip install firecrawl-py")
    exit(1)

# Firecrawl API key
API_KEY = "fc-728da301284d4082a2c6b4069bf29f06"

# Specific subcategories Peter wants
SUBCATEGORIES = {
    "douchesets": {
        "url": "https://www.sawiday.be/nl-be/douche/douchesets/",
        "limit": 50
    },
    "complete-douchecabines": {
        "url": "https://www.sawiday.be/nl-be/douche/complete-douchecabines/",
        "limit": 25
    },
    "infrarood-douchepaneel": {
        "url": "https://www.sawiday.be/nl-be/douche/infrarood-douchepaneel/",
        "limit": 10
    },
    "stoomcabines": {
        "url": "https://www.sawiday.be/nl-be/douche/stoomcabines/",
        "limit": 10
    }
}

class SawidayScraper:
    def __init__(self, api_key: str):
        """Initialize scraper"""
        self.app = FirecrawlApp(api_key=api_key)
        self.all_products = []

        # Output directory
        self.output_dir = Path("/root/.openclaw/workspace/research/bathroom-products/products/raw")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def log(self, message: str):
        """Log message with timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")

    def scrape_subcategory(self, name: str, url: str, limit: int):
        """Scrape a subcategory"""
        self.log("=" * 60)
        self.log(f"🔍 Scraping: {name}")
        self.log(f"URL: {url}")
        self.log(f"Limit: {limit}")
        self.log("=" * 60)

        try:
            # Use Firecrawl to scrape the page
            self.log(f"📄 Fetching with Firecrawl...")
            
            # Try the v1 API first
            scrape_result = self.app.scrape(
                url,
                params={
                    'formats': ['markdown', 'extract'],
                    'onlyMainContent': True
                }
            )

            if not scrape_result or 'error' in scrape_result:
                self.log(f"❌ Firecrawl error: {scrape_result.get('error', 'Unknown error')}")
                return []

            # Get markdown content
            markdown = scrape_result.get('markdown', '')
            self.log(f"📄 Markdown received: {len(markdown)} characters")

            # Parse products from markdown
            products = self.parse_products_from_markdown(markdown, name, limit)
            self.log(f"✅ Parsed {len(products)} products")

            return products

        except Exception as e:
            self.log(f"❌ Error scraping {name}: {e}")
            return []

    def parse_products_from_markdown(self, markdown: str, category: str, limit: int) -> list:
        """Parse products from markdown content"""
        products = []
        lines = markdown.split('\n')

        current_product = {}
        product_count = 0

        for line in lines:
            line = line.strip()

            # Check for product headings (usually ### or #### followed by product name)
            if line.startswith('###') or line.startswith('####'):
                # Save previous product if exists
                if current_product and 'name' in current_product:
                    products.append(current_product)
                    product_count += 1

                    # Check limit
                    if limit and product_count >= limit:
                        self.log(f"✅ Reached limit of {limit} products")
                        break

                # Start new product
                current_product = {
                    'name': line.lstrip('#').strip(),
                    'category': category,
                    'scraped_at': time.strftime("%Y-%m-%d %H:%M:%S")
                }

            # Check for price (patterns like €819,99 or 819,99)
            elif '€' in line or (',' in line and any(c.isdigit() for c in line)):
                if current_product:
                    # Extract price
                    price_text = line.replace('€', '').replace(',', '.').strip()
                    try:
                        price = float(''.join(c for c in price_text if c.isdigit() or c == '.'))
                        current_product['price'] = price
                    except:
                        pass

            # Check for brand (common brands)
            elif any(brand.lower() in line.lower() for brand in [
                'Fortifura', 'GROHE', 'Hansgrohe', 'Villeroy & Boch',
                'Geberit', 'Duravit', 'Adema', 'Ideal Standard',
                'Jika', 'Riho', 'Wiesbaden', 'Hotbath'
            ]):
                if current_product:
                    # Extract brand
                    for brand in ['Fortifura', 'GROHE', 'Hansgrohe', 'Villeroy & Boch',
                                   'Geberit', 'Duravit', 'Adema', 'Ideal Standard',
                                   'Jika', 'Riho', 'Wiesbaden', 'Hotbath']:
                        if brand.lower() in line.lower():
                            current_product['brand'] = brand
                            break

        # Don't forget the last product
        if current_product and 'name' in current_product:
            products.append(current_product)

        self.log(f"📊 Parsed {len(products)} products from markdown")
        return products

    def scrape_all(self):
        """Scrape all subcategories"""
        self.log("🚀 Starting Sawiday scraper for specific subcategories")

        for name, config in SUBCATEGORIES.items():
            products = self.scrape_subcategory(
                name,
                config['url'],
                config['limit']
            )

            if not products:
                continue

            self.all_products.extend(products)

            # Save after each subcategory
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_file = self.output_dir / f"sawiday-{name}-{timestamp}.json"

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(products, f, ensure_ascii=False, indent=2)

            self.log(f"💾 Saved {len(products)} products to {output_file}")

            # Small delay between subcategories
            time.sleep(2)

        # Save combined output
        if self.all_products:
            combined_file = self.output_dir / f"sawiday-douche-{time.strftime('%Y%m%d_%H%M%S')}.json"

            with open(combined_file, 'w', encoding='utf-8') as f:
                json.dump(self.all_products, f, ensure_ascii=False, indent=2)

            self.log("=" * 60)
            self.log(f"✅ SCRAPING COMPLETE")
            self.log(f"Total products scraped: {len(self.all_products)}")
            self.log(f"Combined output: {combined_file}")
        else:
            self.log("⚠️ No products scraped across all subcategories")

def main():
    scraper = SawidayScraper(api_key=API_KEY)
    scraper.scrape_all()

if __name__ == '__main__':
    main()
