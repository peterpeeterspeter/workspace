#!/usr/bin/env python3
"""
Simple Sawiday Scraper - collects 5 products per brand per subcategory
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from datetime import datetime
from collections import defaultdict

class SimpleSawidayScraper:
    def __init__(self):
        self.base_url = "https://www.sawiday.be"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

        # Categories to scrape (based on actual site URLs)
        self.categories = {
            "Baden": [
                "/nl-be/baden/alle-baden/",
                "/nl-be/baden/vrijstaande-baden/",
                "/nl-be/baden/half-vrijstaande-baden/",
                "/nl-be/baden/hoekbaden/",
                "/nl-be/baden/inbouwbaden/",
            ],
            "Douche": [
                "/nl-be/douche/",
                "/nl-be/douche/douchewanden/",
                "/nl-be/douche/inloopdouches/",
                "/nl-be/douche/douchebakken/",
            ],
            "Kranen": [
                "/nl-be/kranen/alle-kranen/",
                "/nl-be/kranen/wastafelkranen/",
                "/nl-be/kranen/douchekranen/",
                "/nl-be/kranen/badkranen/",
            ],
            "Toiletten": [
                "/nl-be/toiletten/alle-toiletten/",
                "/nl-be/toiletten/hangtoiletten/",
                "/nl-be/toiletten/staande-toiletten/",
                "/nl-be/toiletten/douche-wc/",
            ],
            "Wastafels": [
                "/nl-be/wastafels/",
                "/nl-be/wastafels/inbouw-wastafels/",
                "/nl-be/wastafels/opbouw-wastafels/",
            ],
            "Spiegels": [
                "/nl-be/spiegels/alle-spiegels/",
                "/nl-be/spiegels/spiegels-met-verlichting/",
                "/nl-be/spiegels/spiegelkasten/",
            ]
        }

        self.results = {}

    def get_product_links(self, category_url, max_products=50):
        """Get product links from a category page."""
        product_urls = []

        # Add base URL if needed
        if not category_url.startswith('http'):
            category_url = self.base_url + category_url

        try:
            # Try multiple pages
            for page in range(1, 6):  # Max 5 pages
                url = f"{category_url}?page={page}" if page > 1 else category_url
                print(f"      Fetching page {page}...")

                response = self.session.get(url, timeout=15)
                if response.status_code != 200:
                    print(f"        Status {response.status_code}")
                    continue

                soup = BeautifulSoup(response.content, 'html.parser')

                # Extract all product links (pattern: /nl-be/p/XXXXXXXX/)
                links = soup.find_all('a', href=re.compile(r'/nl-be/p/\d+/'))

                new_urls = []
                for link in links:
                    href = link.get('href', '')
                    if href and href not in product_urls:
                        full_url = self.base_url + href
                        new_urls.append(full_url)

                if not new_urls:
                    print(f"        No new products on page {page}")
                    if page == 1:
                        break
                    continue

                product_urls.extend(new_urls)
                print(f"        Found {len(new_urls)} products (total: {len(product_urls)})")

                if len(product_urls) >= max_products:
                    break

                time.sleep(1)

        except Exception as e:
            print(f"      Error: {e}")

        return product_urls

    def scrape_product(self, product_url):
        """Scrape product details."""
        try:
            response = self.session.get(product_url, timeout=15)
            if response.status_code != 200:
                return None

            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract product data
            product = {
                "url": product_url,
                "name": "",
                "brand": "",
                "price": 0,
                "images": []
            }

            # Product name (h3.product-title or similar)
            title_elem = soup.find('h3', class_='product-title')
            if title_elem:
                product['name'] = title_elem.get_text(strip=True)

            # Brand (from data-ec-brand attribute or meta tags)
            brand_elem = soup.find(attrs={'data-ec-brand': True})
            if brand_elem:
                product['brand'] = brand_elem.get('data-ec-brand', '').strip()

            # Or try to find brand in meta tags
            if not product['brand']:
                meta_brand = soup.find('meta', property='product:brand')
                if meta_brand:
                    product['brand'] = meta_brand.get('content', '').strip()

            # Price (from data-ec-price or price elements)
            price_elem = soup.find(attrs={'data-ec-price': True})
            if price_elem:
                price_str = price_elem.get('data-ec-price', '0')
                try:
                    product['price'] = float(price_str)
                except:
                    pass

            # Images (from fancybox links)
            for img_link in soup.find_all('a', attrs={'data-fancybox': True}):
                href = img_link.get('href', '')
                if href and 'http' in href:
                    product['images'].append(href)

            # Limit images to 5
            product['images'] = product['images'][:5]

            # Only return if we have at least a name or brand
            if product['name'] or product['brand']:
                return product

        except Exception as e:
            print(f"        Error scraping product: {e}")

        return None

    def scrape_subcategory(self, category_name, subcategory_url):
        """Scrape a subcategory and group by brand."""
        print(f"\n  📁 {subcategory_url.split('/')[-2]}")

        # Get product links
        product_urls = self.get_product_links(subcategory_url, max_products=50)

        if not product_urls:
            print(f"    ❌ No products found")
            return {}

        # Scrape products
        print(f"    Scraping {len(product_urls)} products...")
        products_by_brand = defaultdict(list)

        for i, url in enumerate(product_urls[:50], 1):
            print(f"      {i}/{len(product_urls[:50])} ", end='')

            product = self.scrape_product(url)
            if product:
                brand = product.get('brand', 'Unknown').strip()
                if not brand:
                    # Try to extract from name
                    name = product.get('name', '')
                    for known in ['Zeza', 'Villeroy & Boch', 'Duravit', 'Geberit', 'Grohe', 'Hansgrohe']:
                        if known.lower() in name.lower():
                            brand = known
                            break
                    if not brand:
                        brand = 'Unknown'

                products_by_brand[brand].append(product)
                print(f"✓ {brand} - {product.get('name', 'Unknown')[:40]}")
            else:
                print(f"✗ Failed")

            time.sleep(0.5)

        # Limit to 5 products per brand
        brands_limited = {}
        for brand, products in products_by_brand.items():
            brands_limited[brand] = products[:5]

        return brands_limited

    def scrape_all(self):
        """Scrape all categories."""
        print("🚀 Starting Sawiday Scraper")
        print("="*70)

        for category, subcategories in self.categories.items():
            print(f"\n{'='*70}")
            print(f"📂 CATEGORY: {category}")
            print(f"{'='*70}")

            self.results[category] = {}

            for subcategory_url in subcategories:
                brands = self.scrape_subcategory(category, subcategory_url)

                if brands:
                    subcategory_name = subcategory_url.split('/')[-2].replace('-', ' ').title()
                    self.results[category][subcategory_name] = brands

                time.sleep(2)  # Be polite

        return self.results

    def save_results(self):
        """Save results to JSON."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"/root/.openclaw/workspace/research/bathroom-products/sawiday_scraped_{timestamp}.json"

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

        print(f"\n{'='*70}")
        print(f"✅ Saved to: {filename}")
        print(f"{'='*70}")

        # Print summary
        total_products = 0
        for category, subcats in self.results.items():
            print(f"\n{category}:")
            for subcat, brands in subcats.items():
                for brand, products in brands.items():
                    count = len(products)
                    total_products += count
                    print(f"  {subcat} / {brand}: {count} products")

        print(f"\n{'='*70}")
        print(f"TOTAL PRODUCTS: {total_products}")
        print(f"{'='*70}")

        return filename

def main():
    scraper = SimpleSawidayScraper()
    scraper.scrape_all()
    scraper.save_results()

if __name__ == "__main__":
    main()
