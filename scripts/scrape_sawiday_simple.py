#!/usr/bin/env python3
"""
Simple Sawiday.be scraper - Extract product links from category pages
Then scrape individual product pages for full data

Usage:
    python scrape_sawiday_simple.py --category douche --limit 200
"""

import json
import time
import sys
import subprocess
from pathlib import Path
from urllib.parse import urljoin, urlparse

# Categories to scrape
CATEGORIES = {
    'douche': 'https://www.sawiday.be/nl-be/douche/',
    'kranen': 'https://www.sawiday.be/nl-be/kranen/',
    'wastafels': 'https://www.sawiday.be/nl-be/wastafels/',
    'spiegels': 'https://www.sawiday.be/nl-be/spiegels/',
    'tegels': 'https://www.sawiday.be/nl-be/tegels/',
}

class SimpleSawidayScraper:
    def __init__(self):
        """Initialize scraper"""
        self.all_products = []

        # Output directory
        self.output_dir = Path("/root/.openclaw/workspace/research/bathroom-products/products/raw")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def log(self, message: str):
        """Log message with timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")

    def extract_product_links(self, html: str, base_url: str) -> list:
        """Extract product URLs from HTML"""
        import re

        # Sawiday product URLs follow pattern: /nl-be/p/{id}/{slug}
        pattern = r'href="(/nl-be/p/\d+/[^"]+)"'
        matches = re.findall(pattern, html)

        # Deduplicate and convert to absolute URLs
        unique_urls = set()
        for match in matches:
            absolute_url = urljoin(base_url, match)
            unique_urls.add(absolute_url)

        return list(unique_urls)

    def scrape_product_page(self, product_url: str, category: str) -> dict:
        """Scrape individual product page"""
        try:
            # Use browser tool via subprocess
            result = subprocess.run(
                ['openclaw', 'browser', 'open', product_url],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                self.log(f"⚠️ Failed to open {product_url}")
                return None

            # For now, just extract basic info from URL
            # (Full HTML parsing would require more complex browser interaction)
            url_path = urlparse(product_url).path
            parts = url_path.split('/')

            if len(parts) >= 5:
                product_id = parts[3]
                slug = parts[4]

                # Extract brand from slug if possible
                brand = "Unknown"
                for known_brand in ['Fortifura', 'GROHE', 'Hansgrohe', 'Villeroy',
                                   'Geberit', 'Duravit', 'Adema', 'Ideal']:
                    if known_brand.lower() in slug.lower():
                        brand = known_brand
                        break

                return {
                    'id': product_id,
                    'name': slug.replace('-', ' ').title(),
                    'brand': brand,
                    'category': category,
                    'url': product_url,
                    'scraped_at': time.strftime("%Y-%m-%d %H:%M:%S")
                }

        except Exception as e:
            self.log(f"❌ Error scraping product: {e}")

        return None

    def scrape_category(self, category_name: str, category_url: str, limit: int = None):
        """Scrape a category"""
        self.log("=" * 60)
        self.log(f"🔍 Scraping category: {category_name}")
        self.log(f"URL: {category_url}")
        self.log(f"Limit: {limit if limit else 'onbeperkt'}")
        self.log("=" * 60)

        # First, get category page to find product links
        self.log(f"📄 Fetching category page...")

        # Use curl to get HTML
        try:
            result = subprocess.run(
                ['curl', '-s', category_url],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                self.log(f"❌ Failed to fetch category page")
                return []

            html = result.stdout

            # Extract product links
            product_links = self.extract_product_links(html, category_url)
            self.log(f"📦 Found {len(product_links)} product links")

            if not product_links:
                self.log(f"⚠️ No products found")
                return []

            # Apply limit
            if limit:
                product_links = product_links[:limit]

            self.log(f"📝 Scraping {len(product_links)} products...")

            products = []
            for i, link in enumerate(product_links, 1):
                if i % 10 == 0:
                    self.log(f"  Progress: {i}/{len(product_links)}")

                product = self.scrape_product_page(link, category_name)
                if product:
                    products.append(product)

                # Small delay to be nice
                time.sleep(0.5)

            self.log(f"✅ Scraped {len(products)} products")
            return products

        except Exception as e:
            self.log(f"❌ Error scraping category: {e}")
            return []

    def scrape_all(self, limit: int = None):
        """Scrape all categories"""
        self.log("🚀 Starting Simple Sawiday Scraper")

        for category_name, category_url in CATEGORIES.items():
            products = self.scrape_category(category_name, category_url, limit)

            if not products:
                continue

            self.all_products.extend(products)

            # Save after each category
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_file = self.output_dir / f"sawiday-{category_name}-{timestamp}.json"

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(products, f, ensure_ascii=False, indent=2)

            self.log(f"💾 Saved {len(products)} products to {output_file}")

            # Delay between categories
            time.sleep(2)

        # Save combined
        if self.all_products:
            combined_file = self.output_dir / f"sawiday-all-{time.strftime('%Y%m%d_%H%M%S')}.json"

            with open(combined_file, 'w', encoding='utf-8') as f:
                json.dump(self.all_products, f, ensure_ascii=False, indent=2)

            self.log("=" * 60)
            self.log(f"✅ SCRAPING COMPLETE")
            self.log(f"Total products scraped: {len(self.all_products)}")
            self.log(f"Combined output: {combined_file}")

def main():
    if len(sys.argv) < 2:
        print("Gebruik: python scrape_sawiday_simple.py --category <categorie>")
        print("\nBeschikbare categorieën:")
        for cat in CATEGORIES.keys():
            print(f"  - {cat}")
        print("\nOpties:")
        print("  --category <naam>   Categorie om te scrapen")
        print("  --limit <aantal>   Maximaal aantal producten (default: onbeperkt)")
        sys.exit(1)

    category = sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == '--category' else 'all'
    limit = None

    if len(sys.argv) > 3 and sys.argv[3] == '--limit':
        try:
            limit = int(sys.argv[4])
        except ValueError:
            print(f"❌ Error: --limit moet een getal zijn")
            sys.exit(1)

    scraper = SimpleSawidayScraper()

    if category == 'all':
        scraper.scrape_all(limit)
    elif category in CATEGORIES:
        products = scraper.scrape_category(category, CATEGORIES[category], limit)

        if products:
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
