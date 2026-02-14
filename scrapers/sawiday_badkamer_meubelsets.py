#!/usr/bin/env python3
"""
Sawiday.be Badkamer Meubelsets Scraper
Scrapes vanity units with full specifications and multiple images
Category: https://www.sawiday.be/nl-be/badkamermeubelen/meubelsets/
"""
import json
import time
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# =============================================================================
# CONFIGURATION
# =============================================================================

BASE_URL = "https://www.sawiday.be/nl-be/badkamermeubelen/meubelsets/"
OUTPUT_DIR = "/root/.openclaw/workspace/research/bathroom-products/products/raw"
HEADLESS = True  # Set to False to see browser
MAX_PAGES = 30  # Safety limit
MAX_PRODUCTS = 200  # Safety limit
DELAY = 2  # Delay between page loads


# =============================================================================
# SCRAPER CLASS
# =============================================================================

class SawidayMeubelsetsScraper:
    """Scraper for Sawiday vanity units category"""

    def __init__(self, headless=True):
        self.headless = headless
        self.products = []
        self.seen_urls = set()

        # Setup Chrome options
        options = Options()
        if headless:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-extensions')

        self.driver = webdriver.Chrome(options=options)
        self.driver.set_page_load_timeout(60)

    def extract_product_specs(self, product_element):
        """Extract product specifications from product card"""
        specs = {
            'width': None,
            'depth': None,
            'material': None,
            'color': None,
            'features': []
        }

        try:
            # Extract name (contains specs)
            name_elem = product_element.find_element(By.CSS_SELECTOR, "h2.heading, a.product-title")
            if name_elem:
                name_text = name_elem.text.strip()
                specs = self._parse_specs_from_name(name_text)
        except:
            pass

        # Try to find spec labels/values
        try:
            spec_elements = product_element.find_elements(By.CSS_SELECTOR, ".specs, .spec")
            for spec in spec_elements:
                text = spec.text.strip()
                if ':' in text or 'cm' in text:
                    specs['features'].append(text)
        except:
            pass

        return specs

    def _parse_specs_from_name(self, name_text):
        """Parse specifications from product name"""
        specs = {
            'width': None,
            'depth': None,
            'material': None,
            'color': None,
            'features': []
        }

        # Extract dimensions (e.g., "60x46x55cm")
        dim_match = re.search(r'(\d+)\s*x\s*(\d+(?:\.\d+)?)\s*cm', name_text)
        if dim_match:
            specs['width'] = float(dim_match.group(1))
            specs['depth'] = float(dim_match.group(2)) if '.' in dim_match.group(2) else float(dim_match.group(2))

        # Extract color/material
        if 'wit' in name_text.lower():
            specs['color'] = 'Wit'
        elif 'zwart' in name_text.lower():
            specs['color'] = 'Zwart'
        elif 'antraciet' in name_text.lower():
            specs['color'] = 'Antraciet'
        elif 'beton' in name_text.lower():
            specs['color'] = 'Beton grijs'
        elif 'grijs' in name_text.lower():
            specs['color'] = 'Grijs'

        if 'natuursteen' in name_text.lower():
            specs['material'] = 'Natuursteen'
        elif 'solid surface' in name_text.lower():
            specs['material'] = 'Solid Surface'
        elif 'hout' in name_text.lower():
            specs['material'] = 'Hout'

        return specs

    def extract_images(self, product_element):
        """Extract all images from product card"""
        images = []

        try:
            # Find all images in product card
            img_elements = product_element.find_elements(By.CSS_SELECTOR, "img.product-image")

            for i, img_elem in enumerate(img_elements[:6]):  # Max 6 images
                img_url = img_elem.get_attribute('src')

                if img_url and img_url not in [img['url'] for img in images]:
                    # Determine image type based on position/index
                    if i == 0:
                        img_type = 'front'
                    elif i == 1:
                        img_type = 'side'
                    elif i == len(img_elements) - 1:
                        img_type = 'top'
                    else:
                        img_type = 'detail'

                    # Get alt text
                    alt = img_elem.get_attribute('alt') or ''

                    images.append({
                        'url': img_url,
                        'type': img_type,
                        'alt': alt
                    })
        except:
            pass

        return images

    def extract_product_data(self, product_element):
        """Extract complete product data from product element"""
        product = {}

        # Product link/ID
        try:
            link_elem = product_element.find_element(By.CSS_SELECTOR, "a.product-link")
            product['url'] = link_elem.get_attribute('href')
            if '/p/' in product['url']:
                product['product_id'] = product['url'].split('/p/')[-1]
        except:
            product['url'] = ''
            product['product_id'] = ''

        # Name
        try:
            name_elem = product_element.find_element(By.CSS_SELECTOR, "h2.heading, a.product-title")
            product['name'] = name_elem.text.strip()
        except:
            product['name'] = ''

        # Brand
        try:
            brand_elem = product_element.find_element(By.CSS_SELECTOR, ".brand")
            product['brand'] = brand_elem.text.strip()
        except:
            product['brand'] = 'Unknown'

        # Price
        try:
            price_elem = product_element.find_element(By.CSS_SELECTOR, ".price, .product-price")
            price_text = price_elem.text.strip()
            # Extract numeric price
            price_match = re.search(r'[\d.,]+', price_text.replace('.', '').replace(',', '.'))
            if price_match:
                product['price_eur'] = float(price_match.group())
            else:
                product['price_eur'] = None
        except:
            product['price_eur'] = None

        # Specifications
        product['specifications'] = self.extract_product_specs(product_element)

        # Images
        product['images'] = self.extract_images(product_element)

        # Category
        product['category'] = 'badkamer-meubelsets'
        product['scraped_at'] = datetime.now().isoformat()

        return product

    def wait_for_products(self):
        """Wait for products to load on page"""
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div.product"),
                    By.CSS_SELECTOR, "a.product-link"
                )
            )
        except TimeoutException:
            print("  ⏱ Timeout waiting for products")

    def scrape_page(self, page_num=1):
        """Scrape a single page of products"""
        print(f"📄 Scraping page {page_num}...")

        self.wait_for_products()

        # Find all product elements
        product_links = self.driver.find_elements(By.CSS_SELECTOR, "a.product-link")

        if not product_links:
            print(f"  ⚠️ No products found on page {page_num}")
            return []

        # Extract data from each product
        for link in product_links:
            url = link.get_attribute('href')
            if url and url not in self.seen_urls:
                self.seen_urls.add(url)
                try:
                    # Scroll to element
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", link)
                    time.sleep(0.3)

                    # Extract product data
                    product = self.extract_product_data(link)
                    self.products.append(product)
                except Exception as e:
                    print(f"  ⚠️ Error extracting product: {e}")

        return len(product_links)

    def run(self):
        """Main scraping routine"""
        print("=" * 70)
        print("🇧 Sawiday Badkamer Meubelsets Scraper")
        print("=" * 70)
        print(f"📂 Category: badkamer-meubelsets")
        print(f"🌐 URL: {BASE_URL}")
        print(f"🔧 Headless: {self.headless}")
        print()

        try:
            # Navigate to category
            print(f"📍 Navigating to {BASE_URL}...")
            self.driver.get(BASE_URL)
            time.sleep(3)

            page_num = 1
            consecutive_empty = 0

            while page_num <= MAX_PAGES and len(self.products) < MAX_PRODUCTS:
                new_products = self.scrape_page(page_num)
                consecutive_empty = 0 if new_products > 0 else consecutive_empty + 1

                if new_products == 0:
                    consecutive_empty += 1
                    if consecutive_empty >= 3:
                        print(f"✅ {consecutive_empty} empty pages in a row - stopping pagination")
                        break
                else:
                    consecutive_empty = 0

                print(f"   ✓ Page {page_num}: {new_products} products | Total: {len(self.products)}")
                page_num += 1

                # Check for next page
                if page_num <= MAX_PAGES and len(self.products) < MAX_PRODUCTS and consecutive_empty < 3:
                    try:
                        next_link = self.driver.find_element(By.CSS_SELECTOR, "a.next")
                        if next_link:
                            self.driver.execute_script("arguments[0].scrollIntoView(true);", next_link)
                            time.sleep(1)
                            self.driver.get(next_link.get_attribute('href'))
                            time.sleep(2)
                    except:
                        print("  ⚠️ No next page link found")
                        break

        except Exception as e:
            print(f"❌ Error during scraping: {e}")

        finally:
            self.driver.quit()
            print()

        # Save results
        self.save_results()

    def save_results(self):
        """Save scraped products to JSON file"""
        if not self.products:
            print("❌ No products to save")
            return

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"sawiday-badkamer-meubelsets-{timestamp}.json"

        output_path = f"{OUTPUT_DIR}/{filename}"

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'category': 'badkamer-meubelsets',
                'source': 'Sawiday.be (browser)',
                'scraped_at': datetime.now().isoformat(),
                'total_products': len(self.products),
                'products': self.products
            }, f, ensure_ascii=False, indent=2)

        print(f"\n✅ Saved {len(self.products)} products to {filename}")
        print(f"   Location: {output_path}")

        # Print summary
        print(f"\n📊 SUMMARY")
        print(f"   Category: badkamer-meubelsets")
        print(f"   Products: {len(self.products)}")
        print(f"   File: {filename}")


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    import sys

    # Parse arguments
    headless = '--headless' in sys.argv

    scraper = SawidayMeubelsetsScraper(headless=headless)
    scraper.run()
