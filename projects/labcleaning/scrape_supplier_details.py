#!/usr/bin/env python3
"""
Enhanced Lab Supplier Scraper with Firecrawl
Fetches detailed information from lab supplier websites
"""

import json
import time
import re
import requests
from datetime import datetime
from urllib.parse import urljoin, urlparse
import subprocess
import os

# Output directory
OUTPUT_DIR = "/root/.openclaw/workspace/projects/labcleaning"

def fetch_page_firecrawl(url, max_chars=30000):
    """Fetch page content using Firecrawl web_fetch"""
    try:
        # Call OpenClaw's web_fetch via subprocess
        # We'll write a wrapper script that calls the tool

        # For now, we'll use a simpler approach with curl if web_fetch isn't available
        cmd = f'curl -s -L -A "Mozilla/5.0" --max-time 15 "{url}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=20)

        if result.returncode == 0 and result.stdout:
            return {
                'url': url,
                'status': 200,
                'content': result.stdout[:max_chars],
                'length': len(result.stdout)
            }

        return None
    except Exception as e:
        print(f"  ❌ Error fetching {url}: {e}")
        return None

def extract_emails(text):
    """Extract email addresses from text"""
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)
    # Filter out common false positives
    valid_emails = [e for e in emails if not any(x in e for x in ['example.com', 'test.com', 'localhost'])]
    return list(set(valid_emails))  # Remove duplicates

def extract_phones(text):
    """Extract phone numbers from text"""
    # Match various US phone formats
    phone_patterns = [
        r'\(\d{3}\)\s*\d{3}[-.\s]?\d{4}',  # (123) 456-7890
        r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',   # 123-456-7890
        r'\d{3}[-.\s]?\d{4}',                # 123-4567 (local)
    ]

    phones = []
    for pattern in phone_patterns:
        phones.extend(re.findall(pattern, text))

    # Clean up phone numbers
    cleaned_phones = []
    for phone in phones:
        # Remove common false positives
        if len(re.findall(r'\d', phone)) >= 7:  # At least 7 digits
            cleaned_phones.append(phone)

    return list(set(cleaned_phones))

def extract_addresses(text):
    """Extract US addresses from text"""
    # Simple pattern for street addresses
    # This is a basic implementation - could be enhanced
    address_pattern = r'\d+\s+[A-Z][a-z]+\s+(?:St|Street|Ave|Avenue|Rd|Road|Blvd|Boulevard|Dr|Drive|Ln|Lane|Way|Court|Ct|Pl|Place)\b'

    addresses = re.findall(address_pattern, text, re.IGNORECASE)
    return list(set(addresses))

def clean_html(html_content):
    """Clean HTML tags and extract text"""
    # Remove script and style tags
    html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)

    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', html_content)

    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()

    return text

def scrape_supplier_details(supplier):
    """Scrape detailed information from a supplier website"""
    print(f"\n  🔍 Scraping: {supplier['name']}")

    url = supplier['url']
    result = fetch_page_firecrawl(url)

    if not result:
        print(f"    ⚠️  Could not fetch page")
        return supplier

    # Extract content
    content = result.get('content', '')

    # Clean HTML to get text
    text = clean_html(content)

    # Extract information
    emails = extract_emails(text)
    phones = extract_phones(text)
    addresses = extract_addresses(text)

    # Update supplier with scraped data
    supplier.update({
        'scraped_at': datetime.now().isoformat(),
        'status': result.get('status'),
        'emails': emails[:5],  # Limit to first 5
        'phones': phones[:5],  # Limit to first 5
        'addresses': addresses[:3],  # Limit to first 3
        'page_title': extract_title(content),
        'meta_description': extract_meta_description(content),
        'has_contact_page': has_contact_page(content),
        'has_about_page': has_about_page(content)
    })

    print(f"    ✅ Emails: {len(emails)}, Phones: {len(phones)}, Addresses: {len(addresses)}")

    # Rate limiting
    time.sleep(2)

    return supplier

def extract_title(html):
    """Extract page title"""
    match = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()[:100]
    return ''

def extract_meta_description(html):
    """Extract meta description"""
    match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']', html, re.IGNORECASE)
    if not match:
        match = re.search(r'<meta[^>]*content=["\']([^"\']+)["\'][^>]*name=["\']description["\']', html, re.IGNORECASE)
    if match:
        return match.group(1).strip()[:200]
    return ''

def has_contact_page(html):
    """Check if contact page is linked"""
    contact_keywords = ['contact', 'contacts', 'about/contact', 'contact-us']
    html_lower = html.lower()
    return any(keyword in html_lower for keyword in contact_keywords)

def has_about_page(html):
    """Check if about page is linked"""
    about_keywords = ['about', 'about-us', 'company', 'overview']
    html_lower = html.lower()
    return any(keyword in html_lower for keyword in about_keywords)

def main():
    """Main scraping function"""
    print("🔬 Enhanced Lab Supplier Scraper with Firecrawl")
    print("=" * 60)

    # Load existing suppliers
    json_file = f"{OUTPUT_DIR}/lab_suppliers.json"

    if not os.path.exists(json_file):
        print(f"❌ Error: {json_file} not found")
        print("Run scrape_lab_suppliers.py first")
        return

    with open(json_file, 'r') as f:
        suppliers = json.load(f)

    print(f"📋 Loaded {len(suppliers)} suppliers")
    print(f"⏰ Started at: {datetime.now().isoformat()}")

    # Scrape details for each supplier
    enhanced_suppliers = []

    for i, supplier in enumerate(suppliers, 1):
        print(f"\n[{i}/{len(suppliers)}] {supplier['name']}")

        try:
            enhanced = scrape_supplier_details(supplier)
            enhanced_suppliers.append(enhanced)

            # Save progress every 10 suppliers
            if i % 10 == 0:
                progress_file = f"{OUTPUT_DIR}/suppliers_progress_{i}.json"
                with open(progress_file, 'w') as f:
                    json.dump(enhanced_suppliers, f, indent=2)
                print(f"  💾 Progress saved to {progress_file}")

        except Exception as e:
            print(f"  ❌ Error: {e}")
            enhanced_suppliers.append(supplier)  # Keep original

    # Save enhanced data
    enhanced_file = f"{OUTPUT_DIR}/lab_suppliers_enhanced.json"
    with open(enhanced_file, 'w') as f:
        json.dump(enhanced_suppliers, f, indent=2)

    print(f"\n✅ Enhanced supplier data saved to {enhanced_file}")

    # Save summary
    summary = {
        'total_suppliers': len(enhanced_suppliers),
        'with_emails': sum(1 for s in enhanced_suppliers if s.get('emails')),
        'with_phones': sum(1 for s in enhanced_suppliers if s.get('phones')),
        'with_addresses': sum(1 for s in enhanced_suppliers if s.get('addresses')),
        'scraped_at': datetime.now().isoformat()
    }

    summary_file = f"{OUTPUT_DIR}/scrape_summary.json"
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"\n📊 Summary:")
    print(f"   Total suppliers: {summary['total_suppliers']}")
    print(f"   With emails: {summary['with_emails']}")
    print(f"   With phones: {summary['with_phones']}")
    print(f"   With addresses: {summary['with_addresses']}")
    print(f"\n✅ Done! Files saved to {OUTPUT_DIR}/")

if __name__ == "__main__":
    main()
