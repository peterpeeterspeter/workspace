#!/usr/bin/env python3
"""
Aggressive enrichment for lab cleaning suppliers
Add more companies and find detailed information
"""

import json
import time
import subprocess
import re
from pathlib import Path

DATA_DIR = Path("/root/.openclaw/workspace/projects/labcleaning")
API_KEY = "BSAg8bt2ZJtOI9zGl3lFTkFPQw5I0Ar"

def brave_search(query, count=10):
    """Search using Brave Search API"""
    try:
        encoded_query = query.replace(' ', '+')
        cmd = [
            'curl', '-s',
            f'https://api.search.brave.com/res/v1/web/search?q={encoded_query}&count={count}',
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
        r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',
        r'\b\(\d{3}\)[-.\s]?\d{3}[-.\s]?\d{4}\b',
        r'\b\d{3}[-.\s]?\d{4}\b'
    ]
    phones = []
    for pattern in patterns:
        phones.extend(re.findall(pattern, text))
    return list(set(phones))

def discover_new_companies():
    """Find new lab cleaning companies via search"""
    new_companies = []
    
    search_queries = [
        'laboratory cleaning services USA',
        'lab decontamination companies United States',
        'biosafety cabinet cleaning services',
        'laboratory waste management companies',
        'lab sterilization service providers',
        'pharmaceutical lab cleaning contractors',
        'medical laboratory cleaning services USA',
        'research facility cleaning companies',
        'laboratory decommissioning services',
        'scientific equipment cleaning services'
    ]
    
    print("🔍 Discovering new companies...")
    
    for query in search_queries:
        print(f"  Searching: {query}")
        results = brave_search(query, count=10)
        
        if results and 'web' in results:
            for result in results['web'].get('results', []):
                title = result.get('title', '')
                url = result.get('url', '')
                description = result.get('description', '')
                
                # Extract company name from title
                company_name = title.split('|')[0].split('-')[0].strip()
                
                # Filter out irrelevant results
                skip_keywords = ['how to', 'guide', 'tips', 'best practices', 'pdf', 'course']
                if any(keyword in title.lower() for keyword in skip_keywords):
                    continue
                
                new_companies.append({
                    'name': company_name,
                    'url': url,
                    'description': description,
                    'type': 'cleaning_service',
                    'services': [],
                    'emails': [],
                    'phones': [],
                    'discovered_at': time.strftime("%Y-%m-%dT%H:%M:%S")
                })
        
        time.sleep(2)
    
    return new_companies

def enrich_company_details(company):
    """Deep enrichment for a single company"""
    name = company['name']
    website = company['url']
    
    info = {
        'emails': [],
        'phones': [],
        'address': None,
        'social_media': {},
        'certifications': [],
        'service_areas': [],
        'coverage': [],
        'year_established': None,
        'employee_count': None,
        'annual_revenue': None,
        'clients': [],
        'specializations': []
    }
    
    # Search for detailed information
    queries = [
        f'"{name}" contact address phone email',
        f'"{name}" laboratory cleaning services',
        f'site:{website} about us contact',
        f'"{name}" Better Business Bureau',
        f'"{name}" reviews ratings laboratory',
        f'"{name}" certifications ISO'
    ]
    
    for query in queries:
        results = brave_search(query, count=5)
        
        if results and 'web' in results:
            for result in results['web'].get('results', []):
                text = f"{result.get('title', '')} {result.get('description', '')}"
                
                # Extract contact info
                emails = extract_emails(text)
                phones = extract_phones(text)
                info['emails'].extend(emails)
                info['phones'].extend(phones)
                
                # Look for social media
                if 'linkedin.com' in result.get('url', ''):
                    info['social_media']['linkedin'] = result['url']
                
                # Look for certifications
                cert_keywords = ['ISO', 'CLIA', 'CAP', 'OSHA', 'EPA', 'DEA']
                for cert in cert_keywords:
                    if cert in text:
                        info['certifications'].append(cert)
        
        time.sleep(1.5)
    
    # Try to fetch contact page
    if website:
        try:
            contact_urls = [
                f"{website}/contact",
                f"{website}/about",
                f"{website}/contact-us"
            ]
            
            for contact_url in contact_urls:
                cmd = ['curl', '-s', '-L', '-m', '8', contact_url]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    html = result.stdout
                    info['emails'].extend(extract_emails(html))
                    info['phones'].extend(extract_phones(html))
                    
                    # Look for address patterns
                    address_pattern = r'\d+\s+[A-Z][a-z]+\s+(?:St|Ave|Blvd|Rd|Lane|Road|Drive|Way)[\w\s,]+(?:\d{5})?'
                    addresses = re.findall(address_pattern, html)
                    if addresses and not info['address']:
                        info['address'] = addresses[0]
                
                time.sleep(1)
        except:
            pass
    
    # Clean and deduplicate
    info['emails'] = list(set([e for e in info['emails'] if '@' in e and not e.endswith('.png') and not e.endswith('.jpg')]))
    info['phones'] = list(set(info['phones']))
    info['certifications'] = list(set(info['certifications']))
    
    return info

def find_competitor_pricing():
    """Find pricing information from competitors"""
    pricing_info = []
    
    queries = [
        'laboratory cleaning services pricing cost',
        'lab decontamination service prices',
        'biosafety cabinet certification cost',
        'laboratory waste disposal pricing'
    ]
    
    for query in queries:
        results = brave_search(query, count=5)
        
        if results and 'web' in results:
            for result in results['web'].get('results', []):
                pricing_info.append({
                    'query': query,
                    'title': result.get('title', ''),
                    'url': result.get('url', ''),
                    'snippet': result.get('description', '')
                })
        
        time.sleep(2)
    
    return pricing_info

# Load existing enriched data
try:
    with open(DATA_DIR / "lab_cleaning_services_enriched.json", 'r') as f:
        services = json.load(f)
except:
    with open(DATA_DIR / "lab_cleaning_services.json", 'r') as f:
        services = json.load(f)

print(f"📊 Starting with {len(services)} companies")

# Discover new companies
new_companies = discover_new_companies()
print(f"\n✅ Discovered {len(new_companies)} new companies")

# Enrich existing companies that need more data
print(f"\n🔍 Enriching existing companies...")
companies_to_enrich = [s for s in services if not s.get('address') or not s.get('emails')]

for i, company in enumerate(companies_to_enrich[:15], 1):
    print(f"  {i}. Enriching: {company['name']}")
    
    details = enrich_company_details(company)
    
    if details['emails']:
        existing = company.get('emails', [])
        for email in details['emails']:
            if email not in existing:
                existing.append(email)
        company['emails'] = existing
        print(f"     ✅ Found {len(details['emails'])} emails")
    
    if details['phones']:
        existing = company.get('phones', [])
        for phone in details['phones']:
            if phone not in existing:
                existing.append(phone)
        company['phones'] = existing
        print(f"     ✅ Found {len(details['phones'])} phone numbers")
    
    if details['address']:
        company['address'] = details['address']
        print(f"     ✅ Found address")
    
    if details['social_media']:
        if not company.get('social_media'):
            company['social_media'] = {}
        company['social_media'].update(details['social_media'])
        print(f"     ✅ Found social media")
    
    if details['certifications']:
        company['certifications'] = details['certifications']
        print(f"     ✅ Found certifications: {', '.join(details['certifications'])}")
    
    company['deep_enriched_at'] = time.strftime("%Y-%m-%dT%H:%M:%S")
    time.sleep(2)

# Merge new companies
all_companies = services + new_companies

# Remove duplicates by URL
seen_urls = set()
unique_companies = []
for company in all_companies:
    if company['url'] not in seen_urls:
        seen_urls.add(company['url'])
        unique_companies.append(company)

print(f"\n📊 Total unique companies: {len(unique_companies)}")

# Find pricing information
print(f"\n💰 Finding pricing information...")
pricing_data = find_competitor_pricing()

# Save enriched database
with open(DATA_DIR / "lab_cleaning_services_master.json", 'w') as f:
    json.dump(unique_companies, f, indent=2)

# Save pricing data
with open(DATA_DIR / "market_pricing_data.json", 'w') as f:
    json.dump(pricing_data, f, indent=2)

# Generate statistics
stats = {
    'total_companies': len(unique_companies),
    'newly_discovered': len(new_companies),
    'with_emails': len([s for s in unique_companies if s.get('emails')]),
    'with_phones': len([s for s in unique_companies if s.get('phones')]),
    'with_addresses': len([s for s in unique_companies if s.get('address')]),
    'with_social_media': len([s for s in unique_companies if s.get('social_media')]),
    'with_certifications': len([s for s in unique_companies if s.get('certifications')]),
    'generated_at': time.strftime("%Y-%m-%dT%H:%M:%S")
}

with open(DATA_DIR / "enrichment_statistics.json", 'w') as f:
    json.dump(stats, f, indent=2)

print(f"\n✅ Deep enrichment complete!")
print(f"\n📊 Final Statistics:")
print(f"  Total Companies: {stats['total_companies']}")
print(f"  New Discovered: {stats['newly_discovered']}")
print(f"  With Emails: {stats['with_emails']} ({stats['with_emails']/stats['total_companies']*100:.1f}%)")
print(f"  With Phones: {stats['with_phones']} ({stats['with_phones']/stats['total_companies']*100:.1f}%)")
print(f"  With Addresses: {stats['with_addresses']} ({stats['with_addresses']/stats['total_companies']*100:.1f}%)")
print(f"  With Social Media: {stats['with_social_media']} ({stats['with_social_media']/stats['total_companies']*100:.1f}%)")
print(f"  With Certifications: {stats['with_certifications']} ({stats['with_certifications']/stats['total_companies']*100:.1f}%)")
