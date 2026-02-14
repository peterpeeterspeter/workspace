#!/usr/bin/env python3
"""
Sawiday.be Universal Product Scraper - UPDATED
Uses granular subcategories from Sawiday.be structure

Usage:
    python sawiday_universal_scraper.py --category baden-vrijstaande --max-products 20
"""

import json
import time
import sys
from pathlib import Path

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    print("❌ Selenium not installed")
    sys.exit(1)

# Sawiday.be granular category URLs (from actual website structure)
CATEGORIES = {
    # BATHTUBS - Granular subcategories
    "baden-vrijstaande": "https://www.sawiday.be/nl-be/baden/vrijstaande-badens/",
    "baden-inbouw": "https://www.sawiday.be/nl-be/baden/inbouwbaden/",
    "baden-hoek": "https://www.sawiday.be/nl-be/baden/hoekbaden/",
    
    # TOILETTEN - Granular subcategories
    "toiletten-wandclosets": "https://www.sawiday.be/nl-be/toiletten/wandclosets/",
    "toiletten-staande": "https://www.sawiday.be/nl-be/toiletten/staande-closets/",
    "toiletten-inbouwsets": "https://www.sawiday.be/nl-be/toiletten/inbouwsets/",
    "toiletten-douche-wc": "https://www.sawiday.be/nl-be/toiletten/douche-wc/",
    "toiletten-dublokken": "https://www.sawiday.be/nl-be/toiletten/dublokken/",
    
    # WASTAFELS
    "wastafels-alle": "https://www.sawiday.be/nl-be/wastafels/",
    
    # DOUCHES (Showers)
    "douche-alle": "https://www.sawiday.be/nl-be/douche/",
    
    # KRAANEN (Faucets)
    "kranen-alle": "https://www.sawiday.be/nl-be/kranen/",
}

class SawidayUniversalScraper:
    def __init__(self, category: str):
        self.category = category
        self.products = []
        self.driver = None
        
        # Output directory
        self.output_dir = Path(f"/root/.openclaw/workspace/research/bathroom-products/products/raw")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def init_driver(self):
        """Initialize Chrome driver with headless option"""
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        
    def log(self, message: str):
        """Log message with timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def extract_brand_from_name(self, name: str) -> str:
        """Extract brand from product name"""
        brands = ['Geberit', 'Villeroy & Boch', 'Villeroy-Boch', 'Duravit', 'Grohe',
                  'Hansgrohe', 'Laufen', 'Roca', 'Ideal Standard', 'Jika', 'Wiesbaden',
                  'Plieger', 'Nemo', 'Gustavsberg', 'Villeroy & Boch',
                  'Crosswater', 'Hotbath', 'Fortifura', 'Adema', 'Sanicomp',
                  'Pressalit', 'Porcher', 'Schwab', 'Tiger', 'Bette', 'Kaldewei',
                  'Viega', 'Loewe', 'Alcaplast', 'Heimeier', 'Keuco']
        
        name_upper = name.upper()
        for brand in brands:
            if brand.upper() in name_upper or brand.replace('&', ' ').upper() in name_upper:
                return brand
        return 'Unknown'
    
    def parse_price(self, price_text: str) -> float:
        """Parse Dutch price to float"""
        try:
            import re
            match = re.search(r'(\d+[.,]\d*)', price_text.replace('€', '').replace('.', '').replace(',', '.'))
            return float(match.group(1)) if match else None
        except:
            return None
    
    def extract_products_from_page(self):
        """Extract products from current page"""
        try:
            # Wait for page to load - products are links with href containing "/nl-be/p/"
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/nl-be/p/')]"))
            )
            
            # Find all product links
            product_links = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/nl-be/p/')]")
            self.log(f"Found {len(product_links)} product links on this page")
            
            for link in product_links:
                try:
                    # Skip non-product links (check if it has a heading)
                    try:
                        heading = link.find_element(By.TAG_NAME, "h3")
                    except:
                        continue  # Skip if no h3 heading (not a product)
                    
                    product = {}
                    
                    # Product name from h3
                    product['name'] = heading.text.strip() if heading else "Unknown"
                    
                    # Extract brand from name
                    product['brand'] = self.extract_brand_from_name(product['name'])
                    
                    # Product URL
                    href = link.get_attribute('href')
                    product['url'] = href
                    
                    # Extract product ID from URL
                    if href and '/p/' in href:
                        product_id = href.split('/p/')[1].split('/')[0]
                        product['product_id'] = product_id
                    
                    # Price from text content
                    full_text = link.text
                    product['price_eur'] = self.parse_price(full_text)
                    
                    # Try to get image
                    try:
                        img_elem = link.find_element(By.TAG_NAME, "img")
                        product['image_url'] = img_elem.get_attribute('src') if img_elem else None
                    except:
                        product['image_url'] = None
                    
                    # Map to main category for database
                    product['category'] = self.map_category(self.category)
                    
                    self.products.append(product)
                    self.log(f"  ✓ {product['name'][:50]}... {product['brand']}")
                    
                except Exception as e:
                    self.log(f"  Error extracting product: {e}")
                    continue
                    
        except Exception as e:
            self.log(f"Error waiting for products: {e}")
    
    def map_category(self, sawiday_category: str) -> str:
        """Map Sawiday category to main database category"""
        category_map = {
            # Bathtubs
            "baden-vrijstaande": "Bathtub",
            "baden-inbouw": "Bathtub",
            "baden-hoek": "Bathtub",
            
            # Toilets
            "toiletten-wandclosets": "Toilet",
            "toiletten-staande": "Toilet",
            "toiletten-inbouwsets": "Toilet",
            "toiletten-douche-wc": "Toilet",
            "toiletten-dublokken": "Toilet",
            
            # Vanities
            "wastafels-alle": "Vanity",
            
            # Showers
            "douche-alle": "Shower",
            
            # Faucets
            "kranen-alle": "Faucet"
        }
        
        return category_map.get(sawiday_category, "Unknown")
    
    def scrape_category(self, max_products: int = 50, max_pages: int = 20):
        """Scrape all pages in a category using URL parameter pagination"""
        category_url = CATEGORIES.get(self.category)
        if not category_url:
            self.log(f"Invalid category: {self.category}")
            return
        
        self.init_driver()
        
        try:
            page_num = 1
            consecutive_zero_pages = 0
            seen_urls = set()
            
            while True:
                # Build URL with page parameter
                if page_num == 1:
                    url = category_url
                else:
                    url = f"{category_url}?page={page_num}"
                
                self.log(f"Navigating to: {url}")
                self.driver.get(url)
                
                # Wait for page to load
                time.sleep(3)
                
                # Count products before scraping
                product_count_before = len(self.products)
                
                self.log(f"Scraping page {page_num}...")
                self.extract_products_from_page()
                
                # Check for duplicate URLs
                new_products = len(self.products) - product_count_before
                if new_products == 0:
                    consecutive_zero_pages += 1
                    self.log(f"No new products found on page {page_num}, stopping")
                    break
                
                # Move to next page
                page_num += 1
                
                # Save progress every 5 pages
                if page_num % 5 == 0:
                    self.save_progress()
                
                # Safety limits
                if page_num > max_pages:
                    self.log(f"Reached safety limit of {max_pages} pages")
                    break
                
                if len(self.products) >= max_products:
                    self.log(f"✅ Reached target of {max_products} products")
                    break
            
            # Save final results
            output_file = self.export_final()
            
            print(f"\n✅ Scraping complete!")
            print(f"   Category: {self.category}")
            print(f"   Total pages: {page_num - 1}")
            print(f"   Products: {len(self.products)}")
            print(f"   Output: {output_file}")
            
            return output_file
            
        finally:
            if self.driver:
                self.driver.quit()
    
    def save_progress(self):
        """Save incremental progress"""
        progress_file = self.output_dir / f".sawiday-progress-{self.category}"
        with open(progress_file, 'w') as f:
            json.dump({
                'category': self.category,
                'product_count': len(self.products),
                'last_update': time.strftime("%Y-%m-%d %H:%M:%S")
            }, f, indent=2)
        
        # Also save products
        products_file = self.output_dir / f"sawiday-{self.category}-{int(time.time())}.json"
        with open(products_file, 'w', encoding='utf-8') as f:
            json.dump({
                'category': self.category,
                'source': 'Sawiday.be (browser)',
                'scraped_at': time.strftime("%Y-%m-%d %H:%M:%S"),
                'total_products': len(self.products),
                'products': self.products
            }, f, ensure_ascii=False, indent=2)
    
    def export_final(self):
        """Export final results"""
        filename = f"sawiday-{self.category}-{int(time.time())}"
        output_file = self.output_dir / f"{filename}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'category': self.category,
                'source': 'Sawiday.be (browser)',
                'scraped_at': time.strftime("%Y-%m-%d %H:%M:%S"),
                'total_products': len(self.products),
                'products': self.products
            }, f, ensure_ascii=False, indent=2)
        
        return output_file

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Scrape Sawiday.be product categories")
    parser.add_argument('--category', required=True,
                       help='Granular category (e.g., baden-vrijstaande, toiletten-wandclosets)')
    parser.add_argument('--max-products', type=int, default=50,
                       help='Maximum products to collect (default: 50)')
    parser.add_argument('--max-pages', type=int, default=20,
                       help='Maximum pages to scrape (default: 20)')
    
    args = parser.parse_args()
    
    print(f"""
╔════════════════════════════════════╗
║   Sawiday Universal Scraper - UPDATED  ║
║   Granular Subcategories          ║
║                                     ║
║  Category: {args.category.upper():<20}                ║
╚════════════════════════════════════════╝
""")
    
    scraper = SawidayUniversalScraper(category=args.category)
    
    try:
        scraper.scrape_category(max_products=args.max_products, max_pages=args.max_pages)
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
