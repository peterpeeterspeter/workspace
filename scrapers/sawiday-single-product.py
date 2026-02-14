#!/usr/bin/env python3
"""
Single Product Scraper - Sawiday.be
Scrapes complete product page with all images
"""
import json
import re
import os
from datetime import datetime
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

# Configuration
PRODUCT_URL = "https://www.sawiday.be/nl-be/p/77496023/saniclass-chaci-badkamermeubelset-120x46x55cm-keramische-wastafel-wit-2-ovale-wasbakken-2-kraangaten-2-lades-eiken"
OUTPUT_DIR = "/root/.openclaw/workspace/research/bathroom-products/single-products"

def scrape_product_page(url):
    """Scrape single product page with all data"""
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    print(f"Fetching: {url}")
    response = session.get(url, timeout=30)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    product = {
        'url': url,
        'scraped_at': datetime.now().isoformat()
    }
    
    # Product name
    name_elem = soup.find('h1')
    if name_elem:
        product['name'] = name_elem.get_text(strip=True)
    
    # Extract all images
    images = []
    
    # Method 1: Find all product images
    for img in soup.find_all('img'):
        img_url = img.get('src') or img.get('data-src')
        
        if img_url and ('product' in img_url.lower() or 'saniclass' in img_url.lower()):
            # Skip small thumbnails
            if any(x in img_url.lower() for x in ['icon', 'logo', 'thumb-small']):
                continue
            
            # Get high-res version if available
            high_res_url = img_url.replace('/400x400/', '/overig/').replace('/product/overig/', 'product/overig/')
            
            # Get alt text
            alt_text = img.get('alt', '')
            
            images.append({
                'url': high_res_url if high_res_url.startswith('http') else f"https://www.sawiday.be{high_res_url}",
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
    print(f"  Found {len(unique_images)} unique images")
    
    # Extract specifications from text
    all_text = soup.get_text(separator=' ', strip=True)
    
    # Look for dimension patterns
    dim_match = re.search(r'(\d+)\s*[xX]\s*(\d+)\s*[xX]\s*(\d+)\s*cm', all_text)
    if dim_match:
        product['dimensions'] = f"{dim_match.group(1)}x{dim_match.group(2)}x{dim_match.group(3)} cm"
    
    # Extract price
    price_match = re.search(r'[€e]?\s*[\d.,]+\d{2}', all_text)
    if price_match:
        product['price'] = price_match.group(0)
    
    # Extract material
    if 'MFC' in all_text:
        product['material'] = 'MFC'
    elif 'hout' in all_text.lower():
        product['material'] = 'Hout'
    elif 'keramiek' in all_text.lower():
        product['material'] = 'Keramiek'
    
    # Extract color
    if 'eiken' in all_text.lower():
        product['color'] = 'Eiken (Oak)'
    elif 'wit' in all_text.lower():
        product['color'] = 'Wit (White)'
    elif 'zwart' in all_text.lower():
        product['color'] = 'Zwart (Black)'
    
    # Extract features
    features = []
    if '2 lades' in all_text:
        features.append('2 lades')
    if '2 wasbakken' in all_text:
        features.append('2 wasbakken')
    if '2 kraangaten' in all_text:
        features.append('2 kraangaten')
    if 'overloop' in all_text.lower():
        features.append('Met overloop')
    
    product['features'] = features
    
    return product

def download_images(product, output_dir):
    """Download all product images"""
    images_dir = os.path.join(output_dir, 'images')
    os.makedirs(images_dir, exist_ok=True)
    
    downloaded = []
    
    for i, img in enumerate(product['images'], 1):
        img_url = img['url']
        
        # Generate filename from URL
        filename = img_url.split('/')[-1].split('?')[0]
        if not filename.endswith(('.jpg', '.jpeg', '.png', '.webp')):
            filename += f"_{i}.jpg"
        
        output_path = os.path.join(images_dir, filename)
        
        print(f"  Downloading {i}/{len(product['images'])}: {filename}")
        
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
                'path': output_path
            })
            
        except Exception as e:
            print(f"    Error: {e}")
    
    return downloaded

def main():
    """Main scraper"""
    print("="*70)
    print("Sawiday Product Scraper - Single Product")
    print("="*70)
    print(f"URL: {PRODUCT_URL}")
    print()
    
    # Create output directory
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    product_id = PRODUCT_URL.split('/')[-1].split('-')[0]
    output_dir = os.path.join(OUTPUT_DIR, f"saniclass-{product_id}-{timestamp}")
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Output: {output_dir}")
    print()
    
    # Scrape product data
    product = scrape_product_page(PRODUCT_URL)
    
    # Save product JSON
    json_path = os.path.join(output_dir, 'product.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(product, f, ensure_ascii=False, indent=2)
    
    print(f"Saved: {json_path}")
    print(f"Images: {len(product['images'])}")
    print()
    
    # Download images
    if product['images']:
        print("Downloading images...")
        downloaded = download_images(product, output_dir)
        
        # Save download manifest
        manifest_path = os.path.join(output_dir, 'images.json')
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(downloaded, f, ensure_ascii=False, indent=2)
        
        print(f"Downloaded: {len(downloaded)}/{len(product['images'])} images")
        print(f"Saved: {manifest_path}")
    
    print()
    print("="*70)
    print(f"Done! Check: {output_dir}")
    print("="*70)

if __name__ == "__main__":
    main()
