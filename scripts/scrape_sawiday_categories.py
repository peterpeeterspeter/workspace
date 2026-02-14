#!/usr/bin/env python3
"""
Sawiday.be Category Scraper using Firecrawl API
Scraps all product data from category pages using Firecrawl

Usage:
    python scrape_sawiday_categories.py --category douche --limit 200
    python scrape_sawiday_categories.py --category all
"""

import json
import time
import sys
from pathlib import Path
from urllib.parse import urljoin

# Firecrawl API
try:
    from firecrawl import FirecrawlApp
except ImportError:
    print("❌ Firecrawl not installed. Install with:")
    print("   pip install firecrawl-py")
    sys.exit(1)

# Categories to scrape
CATEGORIES = {
    'douche': 'https://www.sawiday.be/nl-be/douche/',
    'kranen': 'https://www.sawiday.be/nl-be/kranen/',
    'wastafels': 'https://www.sawiday.be/nl-be/wastafels/',
    'spiegels': 'https://www.sawiday.be/nl-be/spiegels/',
    'tegels': 'https://www.sawiday.be/nl-be/tegels/',
}

class SawidayFirecrawlScraper:
    def __init__(self, api_key: str = None):
        """Initialize Firecrawl scraper"""
        if not api_key:
            # Try to get from environment
            import os
            api_key = os.environ.get('FIRECRAWL_API_KEY')

        if not api_key:
            print("❌ No Firecrawl API key found")
            print("Set FIRECRAWL_API_KEY environment variable or pass api_key parameter")
            sys.exit(1)

        self.app = FirecrawlApp(api_key=api_key)
        self.all_products = []

        # Output directory
        self.output_dir = Path("/root/.openclaw/workspace/research/bathroom-products/products/raw")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def log(self, message: str):
        """Log message with timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")

    def scrape_category(self, category_name: str, category_url: str, limit: int = None):
        """Scrape a category using Firecrawl"""
        self.log("=" * 60)
        self.log(f"🔍 Scraping category: {category_name}")
        self.log(f"URL: {category_url}")
        self.log(f"Limit: {limit if limit else 'onbeperkt'}")
        self.log("=" * 60)

        # Use Firecrawl to scrape the page
        try:
            self.log(f"📄 Fetching page with Firecrawl...")
            scrape_result = self.app.scrape(
                category_url,
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

            # Extract structured data if available
            extracted = scrape_result.get('extract', {})

            # Parse products from markdown
            products = self.parse_markdown_products(markdown, category_name, limit)
            self.log(f"✅ Parsed {len(products)} products")

            return products

        except Exception as e:
            self.log(f"❌ Error scraping {category_name}: {e}")
            return []

    def parse_markdown_products(self, markdown: str, category: str, limit: int = None) -> list:
        """Parse products from markdown content"""
        products = []

        # Split by lines
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

    def scrape_all(self, limit: int = None):
        """Scrape all categories"""
        self.log("🚀 Starting Sawiday Scraper with Firecrawl")
        self.log("Categories to scrape:")
        for cat, url in CATEGORIES.items():
            self.log(f"  - {cat}: {url}")
        self.log()

        for category_name, category_url in CATEGORIES.items():
            products = self.scrape_category(category_name, category_url, limit)

            if not products:
                self.log(f"⚠️ No products found for {category_name}")
                continue

            self.all_products.extend(products)

            # Save after each category
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_file = self.output_dir / f"sawiday-{category_name}-{timestamp}.json"

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(products, f, ensure_ascii=False, indent=2)

            self.log(f"💾 Saved {len(products)} products to {output_file}")

            # Small delay between categories
            time.sleep(2)

        # Save combined output
        if self.all_products:
            combined_file = self.output_dir / f"sawiday-all-{time.strftime('%Y%m%d_%H%M%S')}.json"

            with open(combined_file, 'w', encoding='utf-8') as f:
                json.dump(self.all_products, f, ensure_ascii=False, indent=2)

            self.log("=" * 60)
            self.log(f"✅ SCRAPING COMPLETE")
            self.log(f"Total products scraped: {len(self.all_products)}")
            self.log(f"Combined output: {combined_file}")
        else:
            self.log("⚠️ No products scraped across all categories")

def main():
    if len(sys.argv) < 2:
        print("Gebruik: python scrape_sawiday_categories.py --category <categorie>")
        print("\nBeschikbare categorieën:")
        for cat in CATEGORIES.keys():
            print(f"  - {cat}")
        print("\nOpties:")
        print("  --category <naam>   Categorie om te scrapen (douche, kranen, wastafels, spiegels, tegels, all)")
        print("  --limit <aantal>   Maximaal aantal producten om te scrapen (default: onbeperkt)")
        print("\nVoorbeeld:")
        print("  python scrape_sawiday_categories.py --category douche --limit 200")
        sys.exit(1)

    category = sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == '--category' else 'all'
    limit = None

    if len(sys.argv) > 3 and sys.argv[3] == '--limit':
        try:
            limit = int(sys.argv[4])
        except ValueError:
            print(f"❌ Error: --limit moet een getal zijn")
            sys.exit(1)

    scraper = SawidayFirecrawlScraper()

    if category == 'all':
        scraper.scrape_all(limit)
    elif category in CATEGORIES:
        products = scraper.scrape_category(category, CATEGORIES[category], limit)

        if products:
            # Save results
            output_dir = Path("/root/.openclaw/workspace/research/bathroom-products/products/raw")
            output_dir.mkdir(parents=True, exist_ok=True)

            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_file = output_dir / f"sawiday-{category}-{timestamp}.json"

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(products, f, ensure_ascii=False, indent=2)

            print(f"\n✅ Saved {len(products)} products to {output_file}")
    else:
        print(f"❌ Unknown category: {category}")
        print(f"Available: {', '.join(CATEGORIES.keys())}")
        sys.exit(1)

if __name__ == '__main__':
    main()
