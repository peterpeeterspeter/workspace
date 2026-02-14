#!/usr/bin/env python3
"""
Batch Product Scraper
Scrapes multiple product URLs, downloads all images, creates CSV
"""
import json
import csv
import re
import os
from datetime import datetime
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

# Configuration
URLS_FILE = "/root/.openclaw/workspace/scrapers/urls.txt"  # One URL per line
OUTPUT_DIR = "/root/.openclaw/workspace/research/bathroom-products/batch-scrape"
IMAGES_DIR = os.path.join(OUTPUT_DIR, "images")

def scrape_product_page(url):
    """Scrape single product page with all data"""
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    print(f"  Fetching: {url}")
    try:
        response = session.get(url, timeout=30)
        response.raise_for_status()
    except Exception as e:
        print(f"  ERROR fetching {url}: {e}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    product = {
        'url': url,
        'scraped_at': datetime.now().isoformat()
    }
    
    # Product name
    name_elem = soup.find('h1')
    if name_elem:
        product['name'] = name_elem.get_text(strip=True)
    
    # Extract price
    price_elem = soup.find('span', class_='price') or soup.find('div', class_='price')
    if price_elem:
        product['price'] = price_elem.get_text(strip=True)
    else:
        # Try to find price in text
        all_text = soup.get_text(separator=' ', strip=True)
        price_match = re.search(r'[€e]?\s*[\d.,]+\d{2}', all_text)
        if price_match:
            product['price'] = price_match.group(0)
    
    # Extract description
    desc_elem = soup.find('div', class_='description') or soup.find('div', class_='product-description')
    if desc_elem:
        product['description'] = desc_elem.get_text(strip=True)[:500]  # First 500 chars
    
    # Extract ALL images
    images = []
    for img in soup.find_all('img'):
        img_url = img.get('src') or img.get('data-src')
        
        if not img_url:
            continue
        
        # Skip small icons/thumbnails
        if any(x in img_url.lower() for x in ['icon', 'logo', 'thumb-small', '16x16', '32x32']):
            continue
        
        # Get high-res URL
        high_res_url = img_url
        
        # Convert to absolute URL
        if not high_res_url.startswith('http'):
            high_res_url = urljoin(url, high_res_url)
        
        # Get alt text
        alt_text = img.get('alt', '')
        
        images.append({
            'url': high_res_url,
            'alt': alt_text
        })
    
    # Remove duplicates
    seen_urls = set()
    unique_images = []
    for img in images:
        if img['url'] not in seen_urls:
            seen_urls.add(img['url'])
            unique_images.append(img)
    
    product['images'] = unique_images
    product['image_count'] = len(unique_images)
    
    # Extract dimensions from text
    all_text = soup.get_text(separator=' ', strip=True)
    dim_match = re.search(r'(\d+)\s*[xX]\s*(\d+)\s*[xX]\s*(\d+)\s*cm', all_text)
    if dim_match:
        product['dimensions'] = f"{dim_match.group(1)}x{dim_match.group(2)}x{dim_match.group(3)} cm"
    
    # Extract category from URL
    url_parts = url.split('/')
    if len(url_parts) > 3:
        product['category'] = url_parts[3]
    
    return product

def download_images(product, product_dir):
    """Download all product images"""
    images_dir = os.path.join(product_dir, 'images')
    os.makedirs(images_dir, exist_ok=True)
    
    downloaded = []
    
    for i, img in enumerate(product['images'], 1):
        img_url = img['url']
        
        # Generate filename
        # Try to get extension from URL
        parsed = urlparse(img_url)
        ext = os.path.splitext(parsed.path)[1]
        if not ext or ext not in ['.jpg', '.jpeg', '.png', '.webp']:
            ext = '.jpg'
        
        filename = f"image_{i:03d}{ext}"
        output_path = os.path.join(images_dir, filename)
        
        print(f"    Downloading {i}/{len(product['images'])}: {filename}")
        
        try:
            response = requests.get(img_url, timeout=30, stream=True)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            downloaded.append({
                'filename': filename,
                'url': img_url,
                'alt': img.get('alt', ''),
                'local_path': output_path
            })
            
        except Exception as e:
            print(f"      ERROR: {e}")
    
    return downloaded

def main():
    """Main batch scraper"""
    print("="*70)
    print("Batch Product Scraper")
    print("="*70)
    print()
    
    # Read URLs
    if not os.path.exists(URLS_FILE):
        print(f"ERROR: URLs file not found: {URLS_FILE}")
        print(f"Please create {URLS_FILE} with one URL per line")
        return
    
    with open(URLS_FILE, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]
    
    print(f"Found {len(urls)} URLs to process")
    print()
    
    # Create output directories
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    batch_dir = os.path.join(OUTPUT_DIR, f"batch-{timestamp}")
    os.makedirs(batch_dir, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)
    
    print(f"Output directory: {batch_dir}")
    print()
    
    # Process all URLs
    all_products = []
    successful = 0
    failed = 0
    
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] Processing...")
        
        # Scrape product
        product = scrape_product_page(url)
        
        if not product:
            failed += 1
            continue
        
        # Create product directory
        product_id = product.get('name', f'product_{i}').replace(' ', '-').replace('/', '-')[:50]
        product_dir = os.path.join(batch_dir, product_id)
        os.makedirs(product_dir, exist_ok=True)
        
        # Download images
        if product['images']:
            print(f"    Found {len(product['images'])} images")
            downloaded = download_images(product, product_dir)
            product['downloaded_images'] = len(downloaded)
            product['local_image_paths'] = [d['local_path'] for d in downloaded]
        else:
            product['downloaded_images'] = 0
            product['local_image_paths'] = []
        
        # Save product JSON
        json_path = os.path.join(product_dir, 'product.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(product, f, ensure_ascii=False, indent=2)
        
        print(f"    Saved: {json_path}")
        print()
        
        all_products.append(product)
        successful += 1
    
    # Create CSV with all product data
    csv_path = os.path.join(batch_dir, 'products.csv')
    
    # Flatten data for CSV
    fieldnames = [
        'name', 'url', 'price', 'category', 'dimensions', 
        'description', 'image_count', 'downloaded_images',
        'scraped_at'
    ]
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for product in all_products:
            row = {field: product.get(field, '') for field in fieldnames}
            writer.writerow(row)
    
    print("="*70)
    print(f"COMPLETE!")
    print(f"  Processed: {len(urls)} URLs")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    print(f"  Total images scraped: {sum(p['image_count'] for p in all_products)}")
    print(f"  Total images downloaded: {sum(p['downloaded_images'] for p in all_products)}")
    print()
    print(f"CSV: {csv_path}")
    print(f"Products: {batch_dir}")
    print("="*70)

if __name__ == "__main__":
    main()
