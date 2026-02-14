#!/usr/bin/env python3
"""
Batch Browser Scraper - Processes multiple URLs, scrapes all images, creates CSV
Uses OpenClaw browser tool for reliable scraping
"""
import json
import csv
import os
import sys
import re
import requests
from datetime import datetime

# Configuration
URLS_FILE = "/root/.openclaw/workspace/scrapers/urls.txt" if len(sys.argv) < 2 else sys.argv[1]
OUTPUT_DIR = "/root/.openclaw/workspace/research/bathroom-products/batch-browser-scrape"

# Default category/subcategory for all products (can be overridden per URL later)
DEFAULT_CATEGORY = "sub corner baths"
DEFAULT_SUBCATEGORY = ""

def extract_images_from_html(html_content, product_url):
    """Extract only main product images (no duplicates, no navigation)"""
    images = []

    # Get product ID from URL
    product_id = product_url.split('/')[-1].split('-')[0]

    # Pattern for static.rorix.nl URLs (Sawiday CDN)
    pattern = r'https://static\.rorix\.nl/image/[^"\s<>]+?\.(?:jpg|jpeg|png|webp)'
    matches = re.findall(pattern, html_content)

    # Filter and prioritize images
    seen_products = set()  # Track unique product images
    seen_urls = set()  # Track all seen URLs

    for match in set(matches):  # Unique URLs first
        url = match

        # Skip non-product images
        if any(x in url.lower() for x in [
            'menu_banner', 'brandlogo', 'categorieenblok', 'linkedin',
            'opengraph', 'document', 'youtube'
        ]):
            continue

        # Skip very small images (thumbnails/icons)
        if any(x in url for x in ['100x100', '105x105', '150x150']):
            continue

        # Extract product identifier from URL (unique image hash)
        # URL format: .../product/overig/SIZE/HASH.ext
        url_parts = url.split('/')
        if len(url_parts) >= 8:
            image_hash = url_parts[-1].split('.')[0]  # Get unique hash

            # Skip if we've seen this image hash before
            if image_hash in seen_products:
                continue
            seen_products.add(image_hash)

        # Skip if we've seen this exact URL
        if url in seen_urls:
            continue
        seen_urls.add(url)

        # Determine image quality preference
        # Prefer: 2000x2000 > 960x960 > 640x640 > 480x480 > 320x320
        images.append({
            'url': url,
            'type': 'product',
            'alt': ""
        })

    # Remove duplicates by keeping highest quality
    # Sort by quality (2000x2000 first)
    quality_order = ['2000x2000', '960x960', '640x640', '480x480', '320x320', '300x300', '210x210']

    # Group by image hash
    image_groups = {}
    for img in images:
        url = img['url']
        url_parts = url.split('/')
        if len(url_parts) >= 8:
            image_hash = url_parts[-1].split('.')[0]

            if image_hash not in image_groups:
                image_groups[image_hash] = []

            # Determine quality rank
            quality_rank = 999
            for i, size in enumerate(quality_order):
                if size in url:
                    quality_rank = i
                    break

            image_groups[image_hash].append({
                'url': url,
                'quality': quality_rank
            })

    # Keep only best quality from each group
    final_images = []
    for image_hash, variants in image_groups.items():
        # Sort by quality (lower is better)
        variants.sort(key=lambda x: x['quality'])
        final_images.append({
            'url': variants[0]['url'],
            'type': 'product',
            'alt': ""
        })

    return final_images

def scrape_product_with_requests(url):
    """Scrape product using requests + BeautifulSoup (fallback)"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"    ERROR with requests: {e}")
        return None

def extract_category_from_url(url):
    """Extract category and subcategory from URL or product name"""
    from urllib.parse import urlparse
    
    # Default values
    category = "unknown"
    subcategory = "unknown"
    
    # Extract from URL path
    path_parts = url.split('/')
    
    # Try to get from breadcrumb or navigation in HTML later
    # For now, extract from URL structure or set defaults
    
    return category, subcategory

def scrape_product(url, output_dir, category=None, subcategory=None):
    """Scrape single product"""
    print(f"  Scraping: {url}")

    # Try requests method first
    html_content = scrape_product_with_requests(url)

    if not html_content:
        return None

    # Extract product name from HTML
    name_match = re.search(r'<h1[^>]*>(.+?)</h1>', html_content, re.DOTALL)
    name = name_match.group(1).strip() if name_match else "Unknown"

    # Extract price
    price_match = re.search(r'[€e]\s*[\d.,]+\d{2}', html_content)
    price = price_match.group(0) if price_match else ""

    # Extract description (first 500 chars of text content)
    desc_match = re.search(r'<div[^>]*class="[^"]*description[^"]*"[^>]*>(.+?)</div>', html_content, re.DOTALL | re.IGNORECASE)
    description = re.sub(r'<[^>]+>', '', desc_match.group(1)).strip()[:500] if desc_match else ""

    # Extract images
    images = extract_images_from_html(html_content, url)

    # Use provided category/subcategory or extract from URL
    if not category or not subcategory:
        cat, subcat = extract_category_from_url(url)
        category = category or cat
        subcategory = subcategory or subcat

    product = {
        'url': url,
        'name': re.sub(r'<[^>]+>', '', name).strip(),
        'price': price,
        'category': category,
        'subcategory': subcategory,
        'description': re.sub(r'\s+', ' ', description).strip(),
        'image_count': len(images),
        'images': images,
        'scraped_at': datetime.now().isoformat()
    }

    print(f"    Found {len(images)} images")
    return product

def download_images(product, product_dir):
    """Download all product images"""
    images_dir = os.path.join(product_dir, 'images')
    os.makedirs(images_dir, exist_ok=True)

    downloaded = []

    for i, img in enumerate(product['images'], 1):
        img_url = img['url']

        # Generate filename
        ext = '.jpg'
        if '.png' in img_url:
            ext = '.png'
        elif '.webp' in img_url:
            ext = '.webp'

        filename = f"image_{i:03d}{ext}"
        output_path = os.path.join(images_dir, filename)

        print(f"    Downloading {i}/{len(product['images'])}: {filename}")

        try:
            # Add headers to bypass hotlink protection
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://www.sawiday.be/'
            }

            response = requests.get(img_url, headers=headers, timeout=30, stream=True)
            response.raise_for_status()

            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            downloaded.append({
                'filename': filename,
                'url': img_url,
                'path': output_path
            })

        except Exception as e:
            print(f"      ERROR: {e}")

    return downloaded

def main():
    """Main batch scraper"""
    print("="*70)
    print("Batch Browser Scraper")
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

    # Create output directory
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    batch_dir = os.path.join(OUTPUT_DIR, f"batch-{timestamp}")
    os.makedirs(batch_dir, exist_ok=True)

    print(f"Output: {batch_dir}")
    print()

    # Process all URLs
    all_products = []
    successful = 0
    failed = 0

    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] Processing...")

        # Scrape product with defaults
        product = scrape_product(url, batch_dir, DEFAULT_CATEGORY, DEFAULT_SUBCATEGORY)

        if not product:
            failed += 1
            continue

        # Create product directory
        product_id = product.get('name', f'product_{i}').replace(' ', '-').replace('/', '-')[:50]
        product_dir = os.path.join(batch_dir, product_id)
        os.makedirs(product_dir, exist_ok=True)

        # Download images
        if product['images']:
            downloaded = download_images(product, product_dir)
            product['downloaded_images'] = len(downloaded)
            product['local_image_paths'] = [d['path'] for d in downloaded]
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

    fieldnames = [
        'name', 'url', 'price', 'category', 'subcategory',
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
    print(f"  Total images found: {sum(p['image_count'] for p in all_products)}")
    print(f"  Total images downloaded: {sum(p['downloaded_images'] for p in all_products)}")
    print()
    print(f"CSV: {csv_path}")
    print(f"Products: {batch_dir}")
    print("="*70)

if __name__ == "__main__":
    main()
