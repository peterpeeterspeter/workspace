#!/usr/bin/env python3
"""
Sawiday.be Bathtub Scraper
Automated extraction of product data from Sawiday.be bathroom categories

Usage:
    python sawiday_scraper.py --category baden
    python sawiday_scraper.py --category alle  # All categories
    python sawiday_scraper.py --export json --output products.json

Output:
    research/bathroom-products/products/raw/sawiday-bathtubs-{timestamp}.json
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
    "alle": "https://www.sawiday.be/nl-be/baden/alle-baden/",
    "vrijstaande": "https://www.sawiday.be/nl-be/baden/vrijstaande-baden/",
    "inbouw": "https://www.sawiday.be/nl-be/baden/inbouwbaden/",
    "half-vrijstaande": "https://www.sawiday.be/nl-be/baden/half-vrijstaande-baden/",
    "hoek": "https://www.sawiday.be/nl-be/baden/hoekbaden/",
    "whirlpool": "https://www.sawiday.be/nl-be/baden/whirlpool-baden/",
    "douche": "https://www.sawiday.be/nl-be/baden/bad-douche-combinatie/",
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
    'Accept-Language': 'nl-NL,nl;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
}

# Rate limiting
REQUEST_DELAY = (2, 4)  # Seconds between requests
MAX_RETRIES = 3

class SawidayScraper:
    def __init__(self, category: str = 'alle', export_format: str = 'json'):
        self.category = category
        self.export_format = export_format
        self.products = []
        self.session_count = 0
        
        # Output directory
        self.output_dir = Path(f"/root/.openclaw/workspace/research/bathroom-products/products/raw")
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
                response = urlopen(request, timeout=30)
                
                if response.status == 200:
                    return response.read()
                elif response.status == 429:
                    self.log(f"Rate limited (attempt {attempt + 1}/{MAX_RETRIES})")
                    if attempt < MAX_RETRIES - 1:
                        time.sleep(random.uniform(5, 10))
                    else:
                        return None
                else:
                    self.log(f"HTTP {response.status} on attempt {attempt + 1}")
                    if attempt < MAX_RETRIES - 1:
                        time.sleep(random.uniform(2, 5))
                    else:
                        return None
                        
            except HTTPError as e:
                self.log(f"Network error: {e}")
                if retry_count < MAX_RETRIES - 1:
                    time.sleep(random.uniform(3, 7))
                else:
                    return None
            except Exception as e:
                self.log(f"Unexpected error: {e}")
                if retry_count < MAX_RETRIES - 1:
                    time.sleep(random.uniform(2, 4))
                else:
                    return None

    def parse_product_card(self, soup, base_url: str) -> dict:
        """Extract product data from a product card"""
        try:
            card = soup.find('div', class_='product-card')
            if not card:
                return None
                
            product = {}
            
            # Product name
            name_elem = card.find('h2', class_='product-card__title')
            product['name'] = name_elem.get_text(strip=True) if name_elem else "Unknown Product"
            
            # Brand (usually in description or title)
            brand_elem = card.find('span', class_='brand')
            product['brand'] = brand_elem.get_text(strip=True) if brand_elem else self.extract_brand(name_elem)
            
            # Price
            price_elem = card.find('span', class_='price')
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                product['price_eur'] = self.parse_price(price_text)
            
            # Features list
            features = []
            feature_list = card.find('ul', class_='product-card__features')
            if feature_list:
                for li in feature_list.find_all('li'):
                    feature_text = li.get_text(strip=True)
                    if feature_text:
                        features.append(feature_text)
            product['features'] = features
            
            # Product URL
            link_elem = card.find('a', class_='product-card__link')
            if link_elem:
                href = link_elem.get('href')
                if href:
                    product['url'] = urljoin(base_url, href) if not href.startswith('http') else href
            
            # Image URL
            img_elem = card.find('img')
            if img_elem:
                src = img_elem.get('src')
                if src:
                    product['image_url'] = urljoin(base_url, src) if not src.startswith('http') else src
            
            # Popularity score (based on position in listing)
            product['popularity_score'] = 101 - self.total_products  # Earlier = more popular
            
            self.total_products += 1
            
            return product
            
        except Exception as e:
            self.log(f"Error parsing product card: {e}")
            return None

    def extract_brand(self, text: str) -> str:
        """Extract brand name from product text"""
        brands = ['Villeroy & Boch', 'Duravit', 'Riho', 'Bette', 'Kaldewei', 
                  'Viega', 'Hansgrohe', 'Grohe', 'Laufen', 'Roca', 
                  'Geberit', 'Keramag', 'Jakuzzi', 'Badformat', 'Sawiday']
        
        text_upper = text.upper()
        for brand in brands:
            if brand.upper() in text_upper:
                return brand
        return 'Unknown'

    def parse_price(self, price_text: str) -> float:
        """Parse Dutch price to EUR float"""
        try:
            # Remove common Dutch price formatting
            price_text = price_text.replace('€', '').replace('.', '').replace(',', '.')
            
            # Extract number
            import re
            match = re.search(r'(\d+[.,]\d*)', price_text)
            if match:
                return float(match.group(1))
        except:
            return None

    def scrape_category(self, category_url: str):
        """Scrape all pages in a category"""
        self.log(f"Starting category: {category_url}")
        
        base_url = "https://www.sawiday.be"
        page_content = self.get_page(category_url)
        
        if not page_content:
            self.log(f"Failed to fetch category page")
            return
        
        soup = BeautifulSoup(page_content, 'html.parser')
        
        # Check for pagination
        pagination = soup.find('div', class_='pagination')
        page_count = 0
        
        while True:
            self.log(f"Scraping page {page_count + 1}...")
            
            # Parse all product cards on this page
            products = soup.find_all('div', class_='product-card')
            
            for product_card in products:
                product = self.parse_product_card(product_card, base_url)
                if product:
                    self.products.append(product)
                    self.log(f"  Found: {product['name'][:50]}...{product.get('brand', '')}")
            
            self.total_pages += 1
            page_count += 1
            
            # Check for next page
            next_link = soup.find('a', class_='pagination__link--next')
            if not next_link or 'disabled' in str(next_link.get('class', '')):
                break
            
            if next_link and 'disabled' not in str(next_link.get('class', '')):
                next_url = urljoin(base_url, next_link['href'])
                self.log(f"Next page: {next_url}")
                
                # Be polite - longer delay for pagination
                time.sleep(random.uniform(3, 6))
                
                page_content = self.get_page(next_url)
                if not page_content:
                    self.log(f"Failed to fetch next page")
                    break
                    
                soup = BeautifulSoup(page_content, 'html.parser')
            
            # Save progress incrementally
            if page_count % 5 == 0:
                self.save_progress()
        
        self.log(f"Category complete: {len(self.products)} products found")

    def save_progress(self):
        """Save progress to allow resumption"""
        progress_file = self.output_dir / f".sawiday-progress-{self.category}"
        with open(progress_file, 'w') as f:
            json.dump({
                'category': self.category,
                'total_pages': self.total_pages,
                'total_products': len(self.products),
                'last_update': time.strftime("%Y-%m-%d %H:%M:%S")
            }, f, indent=2)
        
        # Also save products incrementally
        products_file = self.output_dir / f"sawiday-bathtubs-{int(time.time())}.json"
        with open(products_file, 'w', encoding='utf-8') as f:
            json.dump(self.products, f, ensure_ascii=False, indent=2)
        
        self.session_count += 1

    def export_final(self):
        """Export final results"""
        filename = f"sawiday-bathtubs-{int(time.time())}"
        
        if self.export_format == 'json':
            output_file = self.output_dir / f"{filename}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'category': self.category,
                    'source': 'Sawiday.be',
                    'scraped_at': time.strftime("%Y-%m-%d %H:%M:%S"),
                    'total_products': len(self.products),
                    'products': self.products
                }, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ Exported {len(self.products)} products to:")
        print(f"   {output_file}")
        return output_file

    def run(self):
        """Main scraping logic"""
        import argparse
        
        parser = argparse.ArgumentParser(description="Scrape Sawiday.be bathroom products")
        parser.add_argument('--category', choices=list(CATEGORIES.keys()),
                       default='alle',
                       help='Category to scrape (default: alle)')
        parser.add_argument('--export', choices=['json', 'csv'],
                       default='json',
                       help='Export format (default: json)')
        parser.add_argument('--output', type=str,
                       help='Output filename (default: timestamped)')
        parser.add_argument('--delay', type=float, default=3.0,
                       help='Delay between requests in seconds (default: 3.0)')
        
        args = parser.parse_args()
        
        # Update global delay from args
        global REQUEST_DELAY
        REQUEST_DELAY = args.delay
        
        print(f"""
╔════════════════════════════════════╗
║     Sawiday.be Scraper                 ║
║                                        ║
║  Category: {args.category.upper():<20}              ║
║  Export: {args.export.upper():<10}               ║
╚══════════════════════════════════════╝
""")
        
        # Get category URL
        category_url = CATEGORIES.get(args.category)
        if not category_url:
            self.log(f"Invalid category: {args.category}")
            return
        
        # Scrape the category
        self.scrape_category(category_url)
        
        # Export results
        if self.products:
            output_file = self.export_final()
            print(f"\n📊 Statistics:")
            print(f"   Category: {args.category}")
            print(f"   Products found: {len(self.products)}")
            print(f"   Pages scraped: {self.total_pages}")
            
            # Price summary
            prices = [p.get('price_eur') for p in self.products if p.get('price_eur')]
            if prices:
                print(f"   Price range: €{min(prices):.2f} - €{max(prices):.2f}")
            
            # Brand summary
            brands = {}
            for p in self.products:
                brand = p.get('brand', 'Unknown')
                brands[brand] = brands.get(brand, 0) + 1
            
            if brands:
                print(f"   Top brands: {dict(sorted(brands.items(), key=lambda x: x[1], reverse=True,)[:5])}")
        else:
            self.log("No products found")
        
        return output_file

def main():
    scraper = SawidayScraper()
    try:
        output = scraper.run()
        
        print(f"\n✅ Scraping complete!")
        print(f"📁 Output: {output}")
        
        if output:
            print(f"\n💡 Next steps:")
            print(f"   1. Review: cat {output}")
            print(f"   2. Add missing fields if needed")
            print(f"   3. Run image scraper: python scrape_images.py --input {output}")
            print(f"   4. Import into DeBadkamer database")
        
    except KeyboardInterrupt:
        print("\n⚠️  Scraping interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
