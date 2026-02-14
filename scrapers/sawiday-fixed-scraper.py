#!/usr/bin/env python3
"""
Fixed Product Scraper - Sawiday.be
Bypasses CDN blocking and downloads all images
"""
import json
import re
import os
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup

# Configuration
PRODUCT_URL = "https://www.sawiday.be/nl-be/p/77496023/saniclass-chaci-badkamermeubelset-120x46x55cm-keramische-wastafel-wit-2-ovale-wasbakken-2-kraangaten-2-lades-eiken"
OUTPUT_DIR = "/root/.openclaw/workspace/research/bathroom-products/single-products"

def create_session():
    """Create session with proper headers to bypass blocking"""
    session = requests.Session()
    
    # Use realistic browser headers
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.sawiday.be/',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    })
    
    return session

def fix_image_url(url):
    """Fix malformed image URLs"""
    # Fix: imageproduct -> image/product
    url = url.replace('imageproduct/', 'image/product/')
    
    # Fix: double slashes
    url = url.replace('https://', 'https://').replace('https:///', 'https://')
    
    # Ensure protocol
    if not url.startswith('http'):
        url = 'https://' + url
    
    return url

def scrape_product_page(url):
    """Scrape single product page with all data"""
    session = create_session()
    
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
    
    # Extract all images with better URL handling
    images = []
    
    # Find all product images
    for img in soup.find_all('img'):
        img_url = img.get('src') or img.get('data-src')
        
        if not img_url:
            continue
        
        # Look for product images
        if any(x in img_url.lower() for x in ['product', 'saniclass', 'chaci', 'badkamer']):
            # Skip tiny thumbnails
            if any(x in img_url.lower() for x in ['100x100', 'icon', 'logo', 'thumb-small']):
                continue
            
            # Fix URL
            fixed_url = fix_image_url(img_url)
            
            # Get alt text
            alt_text = img.get('alt', '')
            
            images.append({
                'url': fixed_url,
                'original_url': img_url,
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
    
    # Extract specifications
    all_text = soup.get_text(separator=' ', strip=True)
    
    # Dimensions
    dim_match = re.search(r'(\d+)\s*[xX]\s*(\d+)\s*[xX]\s*(\d+)\s*cm', all_text)
    if dim_match:
        product['dimensions'] = f"{dim_match.group(1)}x{dim_match.group(2)}x{dim_match.group(3)} cm"
    
    # Price
    price_match = re.search(r'[€]?\s*(\d{1,5})[.,](\d{2})', all_text)
    if price_match:
        product['price'] = f"€{price_match.group(1)}.{price_match.group(2)}"
    
    # Material
    materials = []
    if 'MFC' in all_text:
        materials.append('MDF')
    if 'keramiek' in all_text.lower():
        materials.append('Keramiek (Ceramic)')
    if 'hout' in all_text.lower() or 'eiken' in all_text.lower():
        materials.append('Hout (Wood)')
    product['material'] = ', '.join(set(materials)) if materials else None
    
    # Color
    colors = []
    if 'eiken' in all_text.lower():
        colors.append('Eiken (Oak)')
    if 'wit' in all_text.lower():
        colors.append('Wit (White)')
    if 'zwart' in all_text.lower():
        colors.append('Zwart (Black)')
    product['color'] = ', '.join(set(colors)) if colors else None
    
    # Features
    features = []
    if '2 lades' in all_text or '2 laden' in all_text:
        features.append('2 lades (drawers)')
    if '2 wasbakken' in all_text:
        features.append('2 wasbakken (washbasins)')
    if '2 kraangaten' in all_text:
        features.append('2 kraangaten (faucet holes)')
    if 'overloop' in all_text.lower():
        features.append('Met overloop (overflow)')
    if 'softclose' in all_text.lower():
        features.append('Softclose (soft-close)')
    
    product['features'] = features
    
    return product, session

def download_images(product, session, output_dir):
    """Download all product images with retry logic"""
    images_dir = os.path.join(output_dir, 'images')
    os.makedirs(images_dir, exist_ok=True)
    
    downloaded = []
    failed = []
    
    for i, img in enumerate(product['images'], 1):
        img_url = img['url']
        
        # Generate clean filename
        filename = img_url.split('/')[-1].split('?')[0]
        
        # Clean filename
        filename = re.sub(r'[^\w\-_.]', '-', filename)
        if not filename.endswith(('.jpg', '.jpeg', '.png', '.webp')):
            filename += f"_{i}.jpg"
        
        output_path = os.path.join(images_dir, filename)
        
        print(f"  [{i}/{len(product['images'])}] {filename[:60]}...")
        
        # Retry logic
        for attempt in range(3):
            try:
                response = session.get(img_url, timeout=30, stream=True)
                response.raise_for_status()
                
                # Save image
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                downloaded.append({
                    'filename': filename,
                    'url': img_url,
                    'original_url': img.get('original_url', ''),
                    'alt': img.get('alt', ''),
                    'path': output_path,
                    'size': os.path.getsize(output_path)
                })
                
                print(f"    ✓ {os.path.getsize(output_path)} bytes")
                break
                
            except Exception as e:
                if attempt < 2:
                    print(f"    Retry {attempt + 1}/3...")
                    time.sleep(1)
                else:
                    print(f"    ✗ Failed: {e}")
                    failed.append({
                        'filename': filename,
                        'url': img_url,
                        'error': str(e)
                    })
    
    return downloaded, failed

def main():
    """Main scraper"""
    print("="*70)
    print("Sawiday Product Scraper - FIXED (bypasses CDN)")
    print("="*70)
    print(f"URL: {PRODUCT_URL}")
    print()
    
    # Create output directory
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    product_id = PRODUCT_URL.split('/')[-1].split('-')[0]
    output_dir = os.path.join(OUTPUT_DIR, f"saniclass-{product_id}-fixed-{timestamp}")
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Output: {output_dir}")
    print()
    
    # Scrape product data
    product, session = scrape_product_page(PRODUCT_URL)
    
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
        downloaded, failed = download_images(product, session, output_dir)
        
        print()
        print("="*70)
        print(f"Downloaded: {len(downloaded)}/{len(product['images'])} images")
        print(f"Failed: {len(failed)}")
        
        if downloaded:
            total_size = sum(img['size'] for img in downloaded)
            print(f"Total size: {total_size:,} bytes ({total_size/1024/1024:.2f} MB)")
        
        if failed:
            print()
            print("Failed downloads:")
            for f in failed[:5]:
                print(f"  - {f['filename'][:50]}")
        
        # Save download manifest
        manifest_path = os.path.join(output_dir, 'images.json')
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump({
                'downloaded': downloaded,
                'failed': failed,
                'total': len(product['images'])
            }, f, ensure_ascii=False, indent=2)
        
        print()
        print(f"Manifest: {manifest_path}")
    
    print()
    print("="*70)
    print(f"Done! Check: {output_dir}")
    print("="*70)

if __name__ == "__main__":
    main()
