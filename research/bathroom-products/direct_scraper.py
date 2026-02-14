#!/usr/bin/env python3
"""Direct scraper for Sawiday - 5 products per brand per subcategory"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from collections import defaultdict
from datetime import datetime

def get_product_links(category_url):
    """Get all product links from a category."""
    links = set()

    try:
        # Try first 3 pages
        for page in range(1, 4):
            url = f"{category_url}?page={page}" if page > 1 else category_url

            print(f"  Page {page}: ", end='', flush=True)
            response = requests.get(url, timeout=15)
            if response.status_code != 200:
                print(f"❌ {response.status_code}")
                break

            soup = BeautifulSoup(response.content, 'html.parser')
            page_links = soup.find_all('a', href=re.compile(r'/nl-be/p/\d+/'))

            new_count = 0
            for link in page_links:
                href = link.get('href', '')
                if href.startswith('/nl-be/p/') and href not in links:
                    links.add(href)
                    new_count += 1

            print(f"{new_count} new (total: {len(links)})")

            if new_count == 0:
                break  # No new products, stop

            time.sleep(1)

    except Exception as e:
        print(f"  Error: {e}")

    return list(links)

def scrape_product(product_url):
    """Extract basic product data."""
    try:
        response = requests.get(product_url, timeout=10)
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.content, 'html.parser')

        # Try to find product name
        name = ""
        for selector in ['h3.product-title', 'h1', 'h2', '[class*="product-title"]']:
            elem = soup.select_one(selector)
            if elem:
                name = elem.get_text(strip=True)
                break

        # Try to find brand
        brand = ""
        for attr in ['data-ec-brand', 'data-brand']:
            elem = soup.find(attrs={attr: True})
            if elem:
                brand = elem.get(attr, '').strip()
                break

        # Try meta tag
        if not brand:
            meta = soup.find('meta', property='product:brand')
            if meta:
                brand = meta.get('content', '').strip()

        # If no brand, guess from name
        if not brand and name:
            known_brands = ['Villeroy & Boch', 'Duravit', 'Geberit', 'Grohe', 'Hansgrohe',
                           'Zeza', 'Kohler', 'Laufen', 'Viega', 'Keuco', 'Burgbad', 'Roca']
            for known in known_brands:
                if known.lower() in name.lower():
                    brand = known
                    break

        # Price
        price = 0
        for attr in ['data-ec-price', 'data-price']:
            elem = soup.find(attrs={attr: True})
            if elem:
                try:
                    price = float(elem.get(attr, 0))
                except:
                    pass
                break

        # Images
        images = []
        for link in soup.find_all('a', attrs={'data-fancybox': True}):
            href = link.get('href', '')
            if href and 'http' in href:
                images.append(href)

        return {
            'url': product_url,
            'name': name,
            'brand': brand or 'Unknown',
            'price': price,
            'images': images[:5]
        }

    except Exception as e:
        print(f"    Error: {e}")
        return None

def save_results(results, filename):
    """Save results to JSON file."""
    filepath = f"/root/.openclaw/workspace/research/bathroom-products/{filename}"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"    💾 Saved: {filename}")
    return filepath

def main():
    # Categories to scrape
    categories = {
        "Baden": [
            "https://www.sawiday.be/nl-be/baden/vrijstaande-baden/",
            "https://www.sawiday.be/nl-be/baden/half-vrijstaande-baden/",
            "https://www.sawiday.be/nl-be/baden/hoekbaden/",
            "https://www.sawiday.be/nl-be/baden/inbouwbaden/",
        ],
        "Douche": [
            "https://www.sawiday.be/nl-be/douche/",
            "https://www.sawiday.be/nl-be/douche/douchewanden/",
            "https://www.sawiday.be/nl-be/douche/inloopdouches/",
        ],
        "Kranen": [
            "https://www.sawiday.be/nl-be/kranen/alle-kranen/",
            "https://www.sawiday.be/nl-be/kranen/wastafelkranen/",
            "https://www.sawiday.be/nl-be/kranen/douchekranen/",
        ],
        "Toiletten": [
            "https://www.sawiday.be/nl-be/toiletten/",
            "https://www.sawiday.be/nl-be/toiletten/hangtoiletten/",
            "https://www.sawiday.be/nl-be/toiletten/staande-toiletten/",
        ],
        "Wastafels": [
            "https://www.sawiday.be/nl-be/wastafels/",
            "https://www.sawiday.be/nl-be/wastafels/inbouw-wastafels/",
        ],
        "Spiegels": [
            "https://www.sawiday.be/nl-be/spiegels/alle-spiegels/",
            "https://www.sawiday.be/nl-be/spiegels/spiegels-met-verlichting/",
        ]
    }

    all_results = {}
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    print("="*70)
    print("🚀 SAWIDAY SMART SCRAPER")
    print("="*70)
    print("Collecting 5 products per brand per subcategory")
    print("Saving: 1 file per category + 1 file per subcategory")
    print("="*70)

    for category, subcategories in categories.items():
        print(f"\n{'='*70}")
        print(f"📂 CATEGORY: {category}")
        print(f"{'='*70}")

        all_results[category] = {}

        for subcat_url in subcategories:
            subcat_name = subcat_url.rstrip('/').split('/')[-2]
            print(f"\n  📁 {subcat_name}")

            # Get product links
            product_links = get_product_links(subcat_url)

            if not product_links:
                print(f"    ❌ No products")
                continue

            # Scrape products
            print(f"  Scraping {len(product_links)} products...")
            products_by_brand = defaultdict(list)

            for i, link in enumerate(product_links[:50], 1):
                url = f"https://www.sawiday.be{link}"
                print(f"    {i}/{min(len(product_links), 50)} ", end='', flush=True)

                product = scrape_product(url)
                if product and product.get('name'):
                    brand = product['brand']
                    products_by_brand[brand].append(product)
                    print(f"✓ {brand} - {product['name'][:30]}")
                else:
                    print(f"✗")

                time.sleep(0.5)

            # Limit to 5 per brand
            brands_limited = {}
            for brand, prods in products_by_brand.items():
                brands_limited[brand] = prods[:5]

            # Save subcategory result immediately
            if brands_limited:
                all_results[category][subcat_name] = brands_limited
                subcat_filename = f"{category}_{subcat_name}_5perbrand_{timestamp}.json"
                save_results(brands_limited, subcat_filename)

            time.sleep(2)

        # Save category result after all subcategories complete
        if all_results[category]:
            category_filename = f"{category}_5perbrand_{timestamp}.json"
            save_results(all_results[category], category_filename)

    # Save complete results
    master_filename = f"sawiday_ALL_5perbrand_{timestamp}.json"
    save_results(all_results, master_filename)

    # Summary
    print("\n" + "="*70)
    print("✅ SCRAPING COMPLETE")
    print("="*70)
    print(f"Master file: {master_filename}\n")

    total_products = 0
    for cat, subcats in all_results.items():
        print(f"{cat}:")
        for subcat, brands in subcats.items():
            for brand, prods in brands.items():
                count = len(prods)
                total_products += count
                print(f"  {subcat} / {brand}: {count} products")
        print()

    print(f"{'='*70}")
    print(f"TOTAL PRODUCTS: {total_products}")
    print(f"{'='*70}")

if __name__ == "__main__":
    main()
