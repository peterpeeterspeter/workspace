#!/usr/bin/env python3
"""
Sawiday.be Badkamer Meubelsets Scraper
Scrapes vanity units with full specifications and multiple images
Uses requests + BeautifulSoup (no Selenium needed)
"""
import json
import time
import re
from datetime import datetime
import requests
from bs4 import BeautifulSoup

# =============================================================================
# CONFIGURATION
# =============================================================================

BASE_URL = "https://www.sawiday.be/nl-be/badkamermeubelen/meubelsets/"
OUTPUT_DIR = "/root/.openclaw/workspace/research/bathroom-products/raw"
MAX_PAGES = 30  # Safety limit
MAX_PRODUCTS = 200  # Safety limit
DELAY = 1  # Delay between page loads


# =============================================================================
# SCRAPER CLASS
# =============================================================================

class SawidayBadkamerMeubelsetsScraper:
    """Scraper for Sawiday vanity units category"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.products = []
        self.seen_urls = set()

    def extract_product_specs(self, product_soup):
        """Extract product specifications from product card"""
        specs = {
            'width': None,
            'depth': None,
            'material': None,
            'color': None,
            'features': []
        }

        # Try to extract from product name/title
        title_elem = product_soup.find(['h2', 'h3', 'a'], class_=lambda x: x and ('title' in x.lower() or 'heading' in x.lower()))
        if title_elem:
            name_text = title_elem.get_text(strip=True)
            specs = self._parse_specs_from_text(name_text)

        # Try to find spec labels/values
        for elem in product_soup.find_all(class_=lambda x: x and 'spec' in x.lower()):
            text = elem.get_text(strip=True)
            if ':' in text or 'cm' in text:
                specs['features'].append(text)

        return specs

    def _parse_specs_from_text(self, text):
        """Parse specifications from text"""
        specs = {
            'width': None,
            'depth': None,
            'material': None,
            'color': None,
            'features': []
        }

        # Extract dimensions (e.g., "60x46cm", "60 x 46 cm")
        dim_match = re.search(r'(\d+)\s*[xX]\s*(\d+(?:\.\d+)?)\s*cm', text)
        if dim_match:
            specs['width'] = float(dim_match.group(1))
            specs['depth'] = float(dim_match.group(2)) if '.' in dim_match.group(2) else float(dim_match.group(2))

        # Extract color
        text_lower = text.lower()
        if 'wit' in text_lower:
            specs['color'] = 'Wit'
        elif 'zwart' in text_lower:
            specs['color'] = 'Zwart'
        elif 'antraciet' in text_lower:
            specs['color'] = 'Antraciet'
        elif 'beton' in text_lower or ('beton' in text_lower and 'grijs' in text_lower):
            specs['color'] = 'Beton grijs'
        elif 'grijs' in text_lower:
            specs['color'] = 'Grijs'

        # Extract material
        if 'natuursteen' in text_lower:
            specs['material'] = 'Natuursteen'
        elif 'solid surface' in text_lower:
            specs['material'] = 'Solid Surface'
        elif 'hout' in text_lower:
            specs['material'] = 'Hout'

        return specs

    def extract_images(self, product_soup):
        """Extract all images from product card"""
        images = []

        for i, img in enumerate(product_soup.find_all('img', limit=6)):
            img_url = img.get('src') or img.get('data-src')

            if img_url and not any(img_url == img_data['url'] for img_data in images):
                # Determine image type based on position
                if i == 0:
                    img_type = 'front'
                elif i == 1:
                    img_type = 'side'
                elif i == len(list(product_soup.find_all('img'))) - 1:
                    img_type = 'top'
                else:
                    img_type = 'detail'

                # Get alt text
                alt = img.get('alt', '')

                # Handle relative URLs
                if img_url.startswith('//'):
                    img_url = 'https:' + img_url
                elif img_url.startswith('/'):
                    img_url = 'https://www.sawiday.be' + img_url

                images.append({
                    'url': img_url,
                    'type': img_type,
                    'alt': alt
                })

        return images

    def extract_product_data(self, product_link):
        """Extract complete product data from product link element"""
        product = {}

        # Product link/ID
        href = product_link.get('href', '')
        if href:
            product['url'] = href if href.startswith('http') else 'https://www.sawiday.be' + href

            if '/p/' in product['url']:
                # Extract product ID from URL like /nl-be/p/77580259/...
                product['product_id'] = product['url'].split('/p/')[-1].split('/')[0]
            else:
                product['product_id'] = product['url'].rstrip('/').split('/')[-1]
        else:
            product['url'] = ''
            product['product_id'] = ''

        # Name - product_link is the <a> element, get its heading h3
        name_elem = product_link.find('h3')
        if not name_elem:
            name_elem = product_link.find(['h1', 'h2', 'h4'])
        product['name'] = name_elem.get_text(strip=True) if name_elem else ''

        # Brand - extract from name or use default
        if 'Saniclass' in product['name']:
            product['brand'] = 'Saniclass'
        elif 'Mondiaz' in product['name']:
            product['brand'] = 'Mondiaz'
        else:
            product['brand'] = 'Sawiday'

        # Price - find in product link
        price_text = product_link.get_text(strip=True)
        # Extract numeric price (last occurrence of digits with comma/decimal)
        price_match = re.search(r'(\d{1,5})[.,](\d{2})\s*$', price_text)
        if price_match:
            product['price_eur'] = float(f"{price_match.group(1)}.{price_match.group(2)}")
        else:
            # Try alternative pattern
            price_match = re.search(r'(\d{1,5})[.,](\d{2})', price_text.replace('.', '').replace(',', '.'))
            if price_match:
                product['price_eur'] = float(price_match.group())
            else:
                product['price_eur'] = None

        # Specifications
        product['specifications'] = self.extract_product_specs(product_link)

        # Images
        product['images'] = self.extract_images(product_link)

        # Category
        product['category'] = 'badkamer-meubelsets'
        product['scraped_at'] = datetime.now().isoformat()

        return product

    def scrape_page(self, url):
        """Scrape a single page of products"""
        print(f"📄 Scraping {url}...")

        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Find product elements - Sawiday uses <a> tags as product containers
            product_containers = []

            # Find all product links (containing /p/)
            for a in soup.find_all('a', href=lambda x: x and '/p/' in x and '/nl-be/p/' in x):
                product_containers.append(a)

            if not product_containers:
                print(f" ⚠️ No products found")
                return 0

            products_count = 0

            # Extract data from each product
            for product_link in product_containers:
                try:
                    product = self.extract_product_data(product_link)

                    # Skip if we've seen this URL
                    if product['url'] and product['url'] not in self.seen_urls:
                        self.seen_urls.add(product['url'])
                        self.products.append(product)
                        products_count += 1

                        if len(self.products) >= MAX_PRODUCTS:
                            break

                except Exception as e:
                    print(f" ⚠️ Error extracting product: {e}")

            return products_count

        except requests.RequestException as e:
            print(f" ❌ Error fetching page: {e}")
            return 0

    def run(self):
        """Main scraping routine"""
        print("=" * 70)
        print("🇧🇪 Sawiday Badkamer Meubelsets Scraper")
        print("=" * 70)
        print(f"📂 Category: badkamer-meubelsets")
        print(f"🌐 URL: {BASE_URL}")
        print()

        page_num = 1
        consecutive_empty = 0
        current_url = BASE_URL

        while page_num <= MAX_PAGES and len(self.products) < MAX_PRODUCTS and consecutive_empty < 3:
            new_products = self.scrape_page(current_url)

            if new_products == 0:
                consecutive_empty += 1
                if consecutive_empty >= 3:
                    print(f"✅ {consecutive_empty} empty pages in a row - stopping pagination")
                    break
            else:
                consecutive_empty = 0

            print(f"   ✓ Page {page_num}: {new_products} products | Total: {len(self.products)}")

            # Find next page
            try:
                response = self.session.get(current_url, timeout=30)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')

                # Look for next page link
                next_link = None

                # Try common next page selectors
                for selector in ['a.next', 'a[rel="next"]', 'li.next a',
                                 'a[aria-label*="next"]', 'a[aria-label*="Next"]']:
                    next_elem = soup.select_one(selector)
                    if next_elem and next_elem.get('href'):
                        next_link = next_elem['href']
                        break

                # If no standard next link, use simple page increment
                if not next_link:
                    # Sawiday uses simple ?page=N pagination
                    # Just increment page number
                    if '?' in current_url:
                        # Replace page number in existing URL
                        next_link = re.sub(r'\?page=\d+', f'?page={page_num + 1}', current_url)
                    else:
                        # Add page parameter
                        next_link = f"{current_url}?page={page_num + 1}"

                if next_link:
                    if next_link.startswith('/'):
                        next_link = 'https://www.sawiday.be' + next_link

                    current_url = next_link
                    page_num += 1
                    time.sleep(DELAY)
                else:
                    print(" ℹ️ No next page link found")
                    break

            except Exception as e:
                print(f" ⚠️ Error finding next page: {e}")
                break

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
                'source': 'Sawiday.be',
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
    scraper = SawidayBadkamerMeubelsetsScraper()
    scraper.run()
