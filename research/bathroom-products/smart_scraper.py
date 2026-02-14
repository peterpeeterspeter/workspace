#!/usr/bin/env python3
"""
Smart Scraper for Sawiday.be
Collects 5 products per brand per subcategory from each main category.

Structure:
- Category (e.g., Baden)
  - Subcategory (e.g., Vrijstaande baden)
    - Brand (e.g., Villeroy & Boch)
      - 5 products
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import os
from datetime import datetime
from urllib.parse import urljoin, urlparse
import re

class SmartSawidayScraper:
    def __init__(self):
        self.base_url = "https://www.sawiday.be"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

        # Define main categories and their subcategories
        self.categories = {
            "Baden": {
                "url": "/nl-be/categorie/baden/alle-baden",
                "subcategories": [
                    "vrijstaande-baden",
                    "inbouwbaden",
                    "hoekbaden",
                    "douchebaden",
                    "zitbaden",
                    "half-vrijstaande-baden"
                ]
            },
            "Douche": {
                "url": "/nl-be/categorie/douche",
                "subcategories": [
                    "douchewanden",
                    "inloopdouches",
                    "douchebakken",
                    "douchecabines",
                    "douchekranen",
                    "regendouches"
                ]
            },
            "Kranen": {
                "url": "/nl-be/categorie/kranen",
                "subcategories": [
                    "wastafelkranen",
                    "douchekranen",
                    "badkranen",
                    "thermostaatkranen",
                    "keukenkranen"
                ]
            },
            "Toiletten": {
                "url": "/nl-be/categorie/toiletten",
                "subcategories": [
                    "hangtoiletten",
                    "staande-toiletten",
                    "douche-wc",
                    "toiletten-sets",
                    "compacte-toiletten"
                ]
            },
            "Wastafels": {
                "url": "/nl-be/categorie/wastafels",
                "subcategories": [
                    "inbouw-wastafels",
                    "opbouw-wastafels",
                    "wastafelbladen",
                    "fonteinen"
                ]
            },
            "Spiegels": {
                "url": "/nl-be/categorie/spiegels",
                "subcategories": [
                    "spiegels-met-verlichting",
                    "spiegels-zonder-verlichting",
                    "spiegelkasten",
                    "vergrootspiegels"
                ]
            }
        }

        self.results = {
            "scraped_at": datetime.now().isoformat(),
            "categories": {}
        }

    def get_subcategory_url(self, main_category, subcategory):
        """Build full URL for a subcategory."""
        # Try different URL patterns
        patterns = [
            f"/nl-be/categorie/{main_category.lower()}/{subcategory}",
            f"/nl-be/{subcategory}",
            f"/nl-be/categorie/{subcategory}"
        ]

        for pattern in patterns:
            url = urljoin(self.base_url, pattern)
            try:
                response = self.session.get(url, timeout=10)
                if response.status_code == 200:
                    return url
            except:
                continue

        return None

    def extract_products_from_page(self, url, seen_urls=None):
        """Extract product links from a listing page."""
        if seen_urls is None:
            seen_urls = set()

        products = []

        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all product links (various selectors)
            selectors = [
                'a.product-card__link',
                'a.product-item',
                'a[href*="/p/"]',
                'a.product-link',
                '.product a[href]'
            ]

            all_links = []
            for selector in selectors:
                links = soup.select(selector)
                all_links.extend(links)

            for link in all_links:
                href = link.get('href', '')
                if '/p/' in href and href not in seen_urls:
                    full_url = urljoin(self.base_url, href)
                    products.append(full_url)
                    seen_urls.add(href)

        except Exception as e:
            print(f"  Error extracting products: {e}")

        return products

    def scrape_product_details(self, product_url):
        """Scrape detailed information from a product page."""
        try:
            response = self.session.get(product_url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract product data
            data = {
                "url": product_url,
                "name": "",
                "brand": "",
                "price": 0,
                "description": "",
                "images": [],
                "specifications": {},
                "availability": ""
            }

            # Product name
            name_selectors = [
                'h1.product-detail__title',
                'h1.product-name',
                'h1[class*="product"]',
                '.product-title'
            ]
            for selector in name_selectors:
                elem = soup.select_one(selector)
                if elem:
                    data["name"] = elem.get_text(strip=True)
                    break

            # Brand (often in breadcrumbs or product info)
            brand_selectors = [
                '.brand-name',
                '.product-brand',
                '[class*="brand"]'
            ]
            for selector in brand_selectors:
                elem = soup.select_one(selector)
                if elem:
                    data["brand"] = elem.get_text(strip=True)
                    break

            # Price
            price_selectors = [
                '.price',
                '.product-price',
                '[class*="price"]'
            ]
            for selector in price_selectors:
                elem = soup.select_one(selector)
                if elem:
                    price_text = elem.get_text(strip=True)
                    # Extract numeric price
                    price_match = re.search(r'[\d.,]+', price_text)
                    if price_match:
                        price_str = price_match.group().replace('.', '').replace(',', '.')
                        try:
                            data["price"] = float(price_str)
                        except:
                            pass
                    break

            # Description
            desc_selectors = [
                '.product-description',
                '.description',
                '[class*="description"]'
            ]
            for selector in desc_selectors:
                elem = soup.select_one(selector)
                if elem:
                    data["description"] = elem.get_text(strip=True)
                    break

            # Images
            img_selectors = [
                'img.product-image',
                'img[class*="product"]',
                '.product-gallery img'
            ]
            for selector in img_selectors:
                imgs = soup.select(selector)
                for img in imgs[:5]:  # Max 5 images
                    src = img.get('src', '') or img.get('data-src', '')
                    if src and 'http' in src:
                        data["images"].append(src)

            # Availability
            avail_selectors = [
                '.availability',
                '[class*="stock"]',
                '[class*="availability"]'
            ]
            for selector in avail_selectors:
                elem = soup.select_one(selector)
                if elem:
                    data["availability"] = elem.get_text(strip=True)
                    break

            return data

        except Exception as e:
            print(f"    Error scraping product {product_url}: {e}")
            return None

    def group_by_brand(self, products):
        """Group products by brand."""
        brands = {}
        for product in products:
            if not product:
                continue

            brand = product.get("brand", "Unknown").strip()
            if not brand:
                # Try to extract brand from product name
                name = product.get("name", "")
                for known_brand in ["Villeroy & Boch", "Duravit", "Geberit", "Grohe", "Hansgrohe",
                                   "Kohler", "Laufen", "Viega", "Keuco", "Burgbad", "Roca"]:
                    if known_brand.lower() in name.lower():
                        brand = known_brand
                        break

            if brand not in brands:
                brands[brand] = []
            brands[brand].append(product)

        return brands

    def scrape_subcategory(self, main_category, subcategory):
        """Scrape all brands in a subcategory, getting 5 products per brand."""
        print(f"\n  Scraping subcategory: {subcategory}")

        # Build URL
        url = self.get_subcategory_url(main_category, subcategory)
        if not url:
            print(f"    ❌ Could not find URL for {subcategory}")
            return {}

        print(f"    URL: {url}")

        # Get all product URLs from this subcategory
        seen_urls = set()
        product_urls = []

        # Try multiple pages
        for page in range(1, 6):  # Max 5 pages
            page_url = f"{url}?page={page}" if page > 1 else url
            print(f"    Checking page {page}...")
            urls = self.extract_products_from_page(page_url, seen_urls)

            if not urls:
                print(f"      No products on page {page}")
                if page == 1:
                    break  # No products at all
                else:
                    continue  # Try next page

            product_urls.extend(urls)
            print(f"      Found {len(urls)} products")

            # Stop if we have enough products
            if len(product_urls) >= 100:
                print(f"      Reached 100 products, stopping")
                break

            time.sleep(1)  # Be polite

        if not product_urls:
            print(f"    ❌ No products found for {subcategory}")
            return {}

        print(f"    Total products found: {len(product_urls)}")

        # Scrape product details
        products = []
        print(f"    Scraping product details...")
        for i, product_url in enumerate(product_urls[:50], 1):  # Max 50 products per subcategory
            print(f"      {i}/{min(len(product_urls), 50)}: ", end='')
            product_data = self.scrape_product_details(product_url)
            if product_data:
                products.append(product_data)
                print(f"✓ {product_data.get('name', 'Unknown')[:40]}")
            time.sleep(0.5)  # Be polite

        if not products:
            print(f"    ❌ No product details scraped")
            return {}

        # Group by brand
        brands = self.group_by_brand(products)
        print(f"    Found {len(brands)} brands")

        # Take 5 products per brand
        brands_limited = {}
        for brand, brand_products in brands.items():
            brands_limited[brand] = brand_products[:5]
            print(f"      {brand}: {len(brand_products)} products → keeping 5")

        return brands_limited

    def scrape_all(self):
        """Scrape all categories, subcategories, and brands."""
        for category, data in self.categories.items():
            print(f"\n{'='*60}")
            print(f"CATEGORY: {category}")
            print(f"{'='*60}")

            self.results["categories"][category] = {}

            for subcategory in data["subcategories"]:
                brands = self.scrape_subcategory(category, subcategory)

                if brands:
                    self.results["categories"][category][subcategory] = brands

                time.sleep(2)  # Be polite between subcategories

        return self.results

    def save_results(self, filename=None):
        """Save results to JSON file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"sawiday_smart_scrape_{timestamp}.json"

        filepath = os.path.join(
            "/root/.openclaw/workspace/research/bathroom-products",
            filename
        )

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

        print(f"\n✅ Results saved to: {filepath}")
        return filepath

def main():
    scraper = SmartSawidayScraper()

    print("🚀 Starting Smart Sawiday Scraper")
    print("="*60)
    print("Collecting 5 products per brand per subcategory...")
    print("="*60)

    results = scraper.scrape_all()
    filepath = scraper.save_results()

    # Print summary
    print("\n" + "="*60)
    print("SCRAPING SUMMARY")
    print("="*60)

    total_products = 0
    for category, subcategories in results["categories"].items():
        print(f"\n{category}:")
        for subcategory, brands in subcategories.items():
            for brand, products in brands.items():
                count = len(products)
                total_products += count
                print(f"  {subcategory} / {brand}: {count} products")

    print(f"\n{'='*60}")
    print(f"TOTAL PRODUCTS: {total_products}")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
