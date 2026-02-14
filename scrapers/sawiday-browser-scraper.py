#!/usr/bin/env python3
"""
Final Product Scraper - Sawiday.be (Browser-based)
Uses browser automation to reliably extract ALL images
"""
import json
import os
import sys
import subprocess
import re
from datetime import datetime

# Configuration
PRODUCT_URL = sys.argv[1] if len(sys.argv) > 1 else "https://www.sawiday.be/nl-be/p/77496023/saniclass-chaci-badkamermeubelset-120x46x55cm-keramische-wastafel-wit-2-ovale-wasbakken-2-kraangaten-2-laden-eiken"
OUTPUT_DIR = "/root/.openclaw/workspace/research/bathroom-products/single-products"

def extract_images_from_html(html_content):
    """Extract all image URLs from HTML"""
    images = []
    
    # Find all image URLs in the HTML
    # Pattern for static.rorix.nl URLs
    pattern = r'https://static\.rorix\.nl/image/[^"\s<>]+?\.(?:jpg|jpeg|png|webp)'
    matches = re.findall(pattern, html_content)
    
    for match in set(matches):  # Unique only
        # Clean up URL
        url = match
        
        # Get alt text from context (if available)
        alt = ""
        
        # Determine image type
        img_type = "detail"
        if "2000x2000" in url:
            img_type = "thumbnail"
        elif "480x480" in url:
            img_type = "large"
        elif "105x105" in url:
            img_type = "medium"
        elif "150x150" in url:
            img_type = "larger"
        elif "400x400" in url:
            img_type = "product"
        
        images.append({
            'url': url,
            'type': img_type,
            'alt': alt
        })
    
    return images

def main():
    """Main scraper using browser automation"""
    print("="*70)
    print("Sawiday Product Scraper - BROWSER-BASED")
    print("="*70)
    print(f"URL: {PRODUCT_URL}")
    print()
    
    # Create output directory
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    product_id = PRODUCT_URL.split('/')[-1].split('-')[0]
    output_dir = os.path.join(OUTPUT_DIR, f"saniclass-{product_id}-browser-{timestamp}")
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Output: {output_dir}")
    print()
    
    # Use browser tool to get page HTML
    print("Getting page HTML via browser...")
    result = subprocess.run([
        '/root/.local/share/pnpm/openclaw', 'browser', 'snapshot',
        '--profile', 'openclaw',
        '--depth', '5',
        '--maxChars', '50000',
        '--compact', 'false',
        f"--targetUrl={PRODUCT_URL}"
    ], capture_output=True, text=True, timeout=60)
    
    if result.returncode != 0:
        print(f"Error getting page: {result.stderr}")
        return
    
    # Parse HTML to extract images
    html_content = result.stdout
    
    print("Extracting images from HTML...")
    images = extract_images_from_html(html_content)
    
    print(f"Found {len(images)} unique images")
    print()
    
    # Save product data
    product = {
        'url': PRODUCT_URL,
        'scraped_at': datetime.now().isoformat(),
        'name': product_id.replace('-', ' ').title(),
        'images': images,
        'image_count': len(images)
    }
    
    json_path = os.path.join(output_dir, 'product.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(product, f, ensure_ascii=False, indent=2)
    
    print(f"Saved: {json_path}")
    print(f"Images: {len(images)}")
    print()
    
    # Save image URLs to file for download
    urls_file = os.path.join(output_dir, 'image-urls.txt')
    with open(urls_file, 'w', encoding='utf-8') as f:
        for img in images:
            f.write(f"{img['url']}\n")
    
    print(f"Image URLs saved: {urls_file}")
    print()
    print("="*70)
    print(f"Done! {len(images)} images ready for download")
    print(f"Location: {output_dir}")
    print("="*70)
    print()
    print("Next step: Download images using wget or curl")
    print(f"Example: wget -i {urls_file}")

if __name__ == "__main__":
    main()
