#!/usr/bin/env python3
"""
Deep enrichment of existing companies only
Focus: phone numbers, emails, websites, specializations
No new company discovery
"""

import json
import time
import subprocess
import re
from pathlib import Path
from urllib.parse import urlparse

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
        print(f"    Search error: {e}")
        return None

def fetch_page(url, timeout=8):
    """Fetch webpage content"""
    try:
        cmd = ['curl', '-s', '-L', '-m', str(timeout), url]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout+2)
        if result.returncode == 0:
            return result.stdout
        return None
    except:
        return None

def extract_emails(text):
    """Extract email addresses from text"""
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(pattern, text, re.IGNORECASE)
    # Filter out common false positives
    exclude = ['.png', '.jpg', '.gif', '.css', '.js', '.svg', '.ico', 'example@', 'test@', 'noreply@']
    valid = [e for e in emails if not any(ex in e.lower() for ex in exclude)]
    return list(set(valid))

def extract_phones(text):
    """Extract phone numbers from text"""
    phones = []

    # US formats
    patterns = [
        r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',  # 555-123-4567
        r'\b\(\d{3}\)[-.\s]?\d{3}[-.\s]?\d{4}\b',  # (555) 123-4567
        r'\b\+?1[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',  # +1 555-123-4567
        r'\b\+?1[-.\s]?\(\d{3}\)[-.\s]?\d{3}[-.\s]?\d{4}\b',  # +1 (555) 123-4567
        r'\b\d{3}[-.\s]?\d{4}\b',  # 555-1234
    ]

    for pattern in patterns:
        found = re.findall(pattern, text)
        phones.extend(found)

    return list(set(phones))

def extract_services(text, company_name):
    """Extract service specializations from text"""
    services = []

    # Lab cleaning service keywords
    service_keywords = [
        'biosafety cabinet cleaning', 'biosafety cabinet certification',
        'laboratory decontamination', 'lab decontamination',
        'chemical fume hood cleaning', 'fume hood certification',
        'laboratory decommissioning', 'lab decommissioning',
        'medical waste disposal', 'biohazard waste disposal',
        'sharps disposal', 'pharmaceutical waste',
        'laboratory cleaning', 'lab cleaning services',
        'sterilization services', 'autoclave services',
        'cleanroom cleaning', 'controlled environment cleaning',
        'laboratory relocation', 'lab relocation',
        'equipment decontamination', 'equipment cleaning',
        'biological safety', 'containment laboratory',
        'CLIA waiver', 'CLIA certification',
        'OSHA compliance', 'EPA compliance',
        'laboratory testing', 'analytical testing',
        'environmental monitoring', 'air quality testing',
        'surface testing', 'ATP testing',
        'gas monitoring', 'chemical monitoring'
    ]

    text_lower = text.lower()
    for keyword in service_keywords:
        if keyword in text_lower:
            if keyword not in services:
                services.append(keyword)

    return services

def clean_phone(phone):
    """Clean phone number format"""
    # Remove all non-numeric except +
    phone = re.sub(r'[^\d+]', '', phone)
    # Add +1 if US number without country code
    if phone and phone[0] == '1' and len(phone) == 11:
        phone = '+' + phone
    elif phone and phone[0] != '+' and len(phone) == 10:
        phone = '+1' + phone
    return phone

def enrich_company(company):
    """Deep enrich a single company"""
    name = company['name']
    website = company.get('url', '')

    print(f"  📋 {name}")

    # Initialize new fields
    if 'emails' not in company:
        company['emails'] = []
    if 'phones' not in company:
        company['phones'] = []
    if 'services' not in company:
        company['services'] = []
    if 'specializations' not in company:
        company['specializations'] = []

    all_emails = set(company.get('emails', []))
    all_phones = set(company.get('phones', []))
    all_services = set(company.get('services', []))

    # Step 1: Search for contact page
    print(f"    🔍 Searching for contact information...")

    contact_queries = [
        f'"{name}" contact phone email',
        f'"{name}" contact us phone',
        f'"{name}" customer service phone',
        f'site:{website} contact' if website else f'"{name}" contact information',
    ]

    for query in contact_queries:
        results = brave_search(query, count=5)

        if results and 'web' in results:
            for result in results['web'].get('results', []):
                # Extract from title and description
                text = f"{result.get('title', '')} {result.get('description', '')}"

                emails = extract_emails(text)
                phones = extract_phones(text)

                all_emails.update(emails)
                all_phones.update(phones)

                # Try to fetch the contact page
                result_url = result.get('url', '')
                if result_url and ('contact' in result_url.lower() or 'about' in result_url.lower()):
                    content = fetch_page(result_url)
                    if content:
                        page_emails = extract_emails(content)
                        page_phones = extract_phones(content)
                        page_services = extract_services(content, name)

                        all_emails.update(page_emails)
                        all_phones.update(page_phones)
                        all_services.update(page_services)

                        print(f"      ✅ Fetched {len(page_emails)} emails, {len(page_phones)} phones from {result_url[:50]}...")

        time.sleep(1.5)

    # Step 2: Fetch main website pages
    if website:
        print(f"    🌐 Crawling website...")

        pages_to_check = [
            website,
            f"{website}/contact",
            f"{website}/contact-us",
            f"{website}/about",
            f"{website}/about-us",
            f"{website}/services",
        ]

        for page_url in pages_to_check:
            content = fetch_page(page_url)
            if content:
                page_emails = extract_emails(content)
                page_phones = extract_phones(content)
                page_services = extract_services(content, name)

                all_emails.update(page_emails)
                all_phones.update(page_phones)
                all_services.update(page_services)

                if page_emails or page_phones:
                    print(f"      ✅ Found {len(page_emails)} emails, {len(page_phones)} phones on {page_url.split('/')[-1][:30]}")

            time.sleep(1)

    # Step 3: Search for service specializations
    print(f"    🎯 Finding specializations...")

    if not all_services:
        service_queries = [
            f'"{name}" services laboratory',
            f'"{name}" lab cleaning services',
            f'"{name}" biosafety cabinet',
            f'"{name}" laboratory decontamination',
            f'"{name}" waste management',
        ]

        for query in service_queries:
            results = brave_search(query, count=3)

            if results and 'web' in results:
                for result in results['web'].get('results', []):
                    text = f"{result.get('title', '')} {result.get('description', '')}"
                    services = extract_services(text, name)
                    all_services.update(services)

            time.sleep(1)

    # Clean and deduplicate
    company['emails'] = [e for e in all_emails if '@' in e and len(e) > 6]
    company['phones'] = [clean_phone(p) for p in all_phones if p and len(p) >= 10]
    company['services'] = list(all_services)

    # Update score
    company['data_score'] = 0
    if company['emails']:
        company['data_score'] += 10
    if company['phones']:
        company['data_score'] += 10
    if company.get('address'):
        company['data_score'] += 15
    if company.get('social_media'):
        company['data_score'] += 10
    if company['services']:
        company['data_score'] += 15
    if company.get('certifications'):
        company['data_score'] += 15
    if company.get('revenue'):
        company['data_score'] += 15
    if company.get('ticker'):
        company['data_score'] += 10

    company['deep_enriched_at'] = time.strftime("%Y-%m-%dT%H:%M:%S")

    # Report progress
    email_count = len(company['emails'])
    phone_count = len(company['phones'])
    service_count = len(company['services'])

    if email_count > 0 or phone_count > 0 or service_count > 0:
        print(f"    ✅ Found: {email_count} emails, {phone_count} phones, {service_count} services")
    else:
        print(f"    ⚠️  No new data found")

    return company

# Load existing database
print("📊 Loading database...")
with open(DATA_DIR / "lab_cleaning_services_master.json", 'r') as f:
    companies = json.load(f)

print(f"✅ Loaded {len(companies)} companies")

# Enrich each company
print(f"\n🔍 Starting deep enrichment...\n")

enriched_count = 0
for i, company in enumerate(companies, 1):
    print(f"{i}/{len(companies)} ", end='')

    # Check if already deep enriched
    if company.get('deep_enriched_at'):
        age_hours = (time.time() - time.mktime(time.strptime(company['deep_enriched_at'], "%Y-%m-%dT%H:%M:%S"))) / 3600
        if age_hours < 24:  # Skip if enriched in last 24 hours
            print(f"⏭️  Skipping {company['name']} (enriched {int(age_hours)}h ago)\n")
            continue

    company = enrich_company(company)
    enriched_count += 1

    print()

    # Rate limiting - don't overwhelm Brave API
    if i % 5 == 0:
        print(f"    💤 Pausing for rate limit...")
        time.sleep(5)

# Calculate statistics
stats = {
    'total_companies': len(companies),
    'enriched_this_run': enriched_count,
    'with_emails': len([c for c in companies if c.get('emails')]),
    'with_phones': len([c for c in companies if c.get('phones')]),
    'with_services': len([c for c in companies if c.get('services')]),
    'with_addresses': len([c for c in companies if c.get('address')]),
    'with_social_media': len([c for c in companies if c.get('social_media')]),
    'with_certifications': len([c for c in companies if c.get('certifications')]),
    'avg_score': sum(c.get('data_score', 0) for c in companies) / len(companies),
    'generated_at': time.strftime("%Y-%m-%dT%H:%M:%S")
}

# Save enriched database
output_file = DATA_DIR / "lab_cleaning_services_deep_enriched.json"
with open(output_file, 'w') as f:
    json.dump(companies, f, indent=2)

print(f"\n✅ Deep enrichment complete!")
print(f"💾 Saved to: {output_file}")
print(f"\n📊 Statistics:")
print(f"  Total Companies: {stats['total_companies']}")
print(f"  Enriched This Run: {stats['enriched_this_run']}")
print(f"  With Emails: {stats['with_emails']} ({stats['with_emails']/stats['total_companies']*100:.1f}%)")
print(f"  With Phones: {stats['with_phones']} ({stats['with_phones']/stats['total_companies']*100:.1f}%)")
print(f"  With Services: {stats['with_services']} ({stats['with_services']/stats['total_companies']*100:.1f}%)")
print(f"  With Addresses: {stats['with_addresses']} ({stats['with_addresses']/stats['total_companies']*100:.1f}%)")
print(f"  With Certifications: {stats['with_certifications']} ({stats['with_certifications']/stats['total_companies']*100:.1f}%)")
print(f"  Avg Data Score: {stats['avg_score']:.1f}/100")

# Save statistics
with open(DATA_DIR / "deep_enrichment_stats.json", 'w') as f:
    json.dump(stats, f, indent=2)
