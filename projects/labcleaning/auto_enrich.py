#!/usr/bin/env python3
"""
Auto-enrich suppliers using Brave Search API
"""

import json
import time
import subprocess
import re
from pathlib import Path

DATA_DIR = Path("/root/.openclaw/workspace/projects/labcleaning")
API_KEY = "BSAg8bt2ZJtOI9zGl3lFTkFPQw5I0Ar"

def brave_search(query, count=5):
    """Search using Brave Search API"""
    try:
        cmd = [
            'curl', '-s',
            f'https://api.search.brave.com/res/v1/web/search?q={query}&count={count}',
            '-H', f'X-Subscription-Token: {API_KEY}',
            '-H', 'Accept: application/json'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0:
            return json.loads(result.stdout)
        return None
    except Exception as e:
        print(f"Search error: {e}")
        return None

def extract_emails(text):
    """Extract email addresses from text"""
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return list(set(re.findall(pattern, text, re.IGNORECASE)))

def extract_phones(text):
    """Extract phone numbers from text"""
    patterns = [
        r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',  # 555-123-4567
        r'\b\(\d{3}\)[-.\s]?\d{3}[-.\s]?\d{4}\b',  # (555) 123-4567
        r'\b\d{3}[-.\s]?\d{4}\b'  # 555-1234
    ]
    phones = []
    for pattern in patterns:
        phones.extend(re.findall(pattern, text))
    return list(set(phones))

def search_company_contact_info(company_name, website):
    """Search for contact information"""
    info = {
        'emails': [],
        'phones': [],
        'address': None,
        'description': None
    }
    
    # Search queries
    queries = [
        f'"{company_name}" contact email phone',
        f'"{company_name}" headquarters address',
        f'site:{website} contact',
        f'"{company_name}" laboratory cleaning services contact'
    ]
    
    for query in queries[:2]:  # Limit to 2 searches
        results = brave_search(query, count=3)
        
        if results and 'web' in results:
            for result in results['web'].get('results', []):
                # Extract from title and description
                text = f"{result.get('title', '')} {result.get('description', '')}"
                
                emails = extract_emails(text)
                phones = extract_phones(text)
                
                info['emails'].extend(emails)
                info['phones'].extend(phones)
                
                # Try to fetch the page for more details
                if 'url' in result:
                    page_info = fetch_page_info(result['url'])
                    if page_info:
                        info['emails'].extend(page_info.get('emails', []))
                        info['phones'].extend(page_info.get('phones', []))
                        if page_info.get('address'):
                            info['address'] = page_info['address']
        
        time.sleep(2)  # Rate limiting
    
    # Clean and deduplicate
    info['emails'] = list(set([e for e in info['emails'] if '@' in e]))
    info['phones'] = list(set(info['phones']))
    
    return info

def fetch_page_info(url):
    """Fetch page and extract contact info"""
    try:
        cmd = ['curl', '-s', '-L', '-m', '10', url]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0:
            html = result.stdout
            return {
                'emails': extract_emails(html),
                'phones': extract_phones(html)
            }
    except:
        pass
    return None

# Load enriched data
with open(DATA_DIR / "lab_cleaning_services_enriched.json", 'r') as f:
    services = json.load(f)

# Find companies that still need enrichment
needs_enrichment = [s for s in services if not s.get('address') or not s.get('emails')]

print(f"🔍 Auto-enriching {len(needs_enrichment)} companies...")
print(f"✅ Already enriched: {len(services) - len(needs_enrichment)}")
print()

# Enrich top 10 most important companies first
for i, company in enumerate(needs_enrichment[:10], 1):
    print(f"{i}. Searching: {company['name']}")
    
    # Skip if already has email and address
    if company.get('emails') and company.get('address'):
        print(f"   ✅ Already has contact info")
        continue
    
    info = search_company_contact_info(company['name'], company['url'])
    
    if info['emails']:
        existing = company.get('emails', [])
        for email in info['emails']:
            if email not in existing:
                existing.append(email)
        company['emails'] = existing
        print(f"   ✅ Found {len(info['emails'])} emails")
    
    if info['phones']:
        existing = company.get('phones', [])
        for phone in info['phones']:
            if phone not in existing:
                existing.append(phone)
        company['phones'] = existing
        print(f"   ✅ Found {len(info['phones'])} phone numbers")
    
    if info['address']:
        company['address'] = info['address']
        print(f"   ✅ Found address")
    
    company['auto_enriched_at'] = time.strftime("%Y-%m-%dT%H:%M:%S")
    time.sleep(1)  # Rate limiting

# Save auto-enriched data
with open(DATA_DIR / "lab_cleaning_services_enriched.json", 'w') as f:
    json.dump(services, f, indent=2)

print("\n✅ Auto-enrichment complete!")

# Show final statistics
print(f"\n📊 Final enrichment statistics:")
print(f"  Companies with addresses: {len([s for s in services if s.get('address')])}/{len(services)}")
print(f"  Companies with emails: {len([s for s in services if s.get('emails')])}/{len(services)}")
print(f"  Companies with phones: {len([s for s in services if s.get('phones')])}/{len(services)}")
print(f"  Companies with social media: {len([s for s in services if s.get('social_media')])}/{len(services)}")
