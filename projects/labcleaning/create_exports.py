#!/usr/bin/env python3
"""
Create enriched CSV exports for WordPress import and analysis
"""

import json
import csv
from pathlib import Path
from datetime import datetime

DATA_DIR = Path("/root/.openclaw/workspace/projects/labcleaning")

# Load enriched data
with open(DATA_DIR / "lab_cleaning_services_enriched.json", 'r') as f:
    services = json.load(f)

def flatten_company(company):
    """Flatten nested structure for CSV export"""
    return {
        'name': company.get('name', ''),
        'url': company.get('url', ''),
        'type': company.get('type', ''),
        'description': company.get('description', ''),
        'address': company.get('address', ''),
        'city': company.get('city', ''),
        'state': company.get('state', ''),
        'zip': company.get('zip', ''),
        'country': company.get('country', 'USA'),
        'emails': ', '.join(company.get('emails', [])),
        'phones': ', '.join(company.get('phones', [])),
        'services': ', '.join(company.get('services', [])),
        'founded': company.get('founded', ''),
        'employees': company.get('employees', ''),
        'revenue': company.get('revenue', ''),
        'ticker': company.get('ticker', ''),
        'parent': company.get('parent', ''),
        'linkedin': company.get('social_media', {}).get('linkedin', ''),
        'twitter': company.get('social_media', {}).get('twitter', ''),
        'facebook': company.get('social_media', {}).get('facebook', ''),
        'scraped_at': company.get('scraped_at', ''),
        'enriched_at': company.get('enriched_at', ''),
        'auto_enriched_at': company.get('auto_enriched_at', '')
    }

# 1. Full enriched CSV
with open(DATA_DIR / "lab_cleaning_services_enriched.csv", 'w', newline='', encoding='utf-8') as f:
    fieldnames = [
        'name', 'url', 'type', 'description', 'address', 'city', 'state', 'zip', 'country',
        'emails', 'phones', 'services', 'founded', 'employees', 'revenue', 'ticker', 'parent',
        'linkedin', 'twitter', 'facebook', 'scraped_at', 'enriched_at', 'auto_enriched_at'
    ]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    
    for company in services:
        writer.writerow(flatten_company(company))

print("✅ Created: lab_cleaning_services_enriched.csv")

# 2. WordPress import CSV (custom post type fields)
with open(DATA_DIR / "wordpress_suppliers_enriched.csv", 'w', newline='', encoding='utf-8') as f:
    fieldnames = [
        'post_title', 'post_content', 'post_excerpt', 'post_status',
        'meta_url', 'meta_email', 'meta_phone', 'meta_address',
        'meta_city', 'meta_state', 'meta_zip', 'meta_country',
        'meta_type', 'meta_services', 'meta_founded', 'meta_employees',
        'meta_revenue', 'meta_ticker', 'meta_parent',
        'meta_linkedin', 'meta_twitter', 'meta_facebook'
    ]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    
    for company in services:
        flat = flatten_company(company)
        writer.writerow({
            'post_title': flat['name'],
            'post_content': flat['description'],
            'post_excerpt': flat['description'][:150] + '...' if len(flat['description']) > 150 else flat['description'],
            'post_status': 'draft',
            'meta_url': flat['url'],
            'meta_email': flat['emails'],
            'meta_phone': flat['phones'],
            'meta_address': flat['address'],
            'meta_city': flat['city'],
            'meta_state': flat['state'],
            'meta_zip': flat['zip'],
            'meta_country': flat['country'],
            'meta_type': flat['type'],
            'meta_services': flat['services'],
            'meta_founded': flat['founded'],
            'meta_employees': flat['employees'],
            'meta_revenue': flat['revenue'],
            'meta_ticker': flat['ticker'],
            'meta_parent': flat['parent'],
            'meta_linkedin': flat['linkedin'],
            'meta_twitter': flat['twitter'],
            'meta_facebook': flat['facebook']
        })

print("✅ Created: wordpress_suppliers_enriched.csv")

# 3. Contact list for outreach
with open(DATA_DIR / "supplier_outreach_list.csv", 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['company_name', 'contact_email', 'phone', 'address', 'city', 'state', 'website', 'type']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    
    for company in services:
        if company.get('emails') or company.get('phones'):
            emails = company.get('emails', [])
            writer.writerow({
                'company_name': company.get('name'),
                'contact_email': emails[0] if emails else '',
                'phone': company.get('phones', [''])[0] if company.get('phones') else '',
                'address': company.get('address', ''),
                'city': company.get('city', ''),
                'state': company.get('state', ''),
                'website': company.get('url', ''),
                'type': company.get('type', '')
            })

print("✅ Created: supplier_outreach_list.csv")

# 4. Generate summary report
summary = {
    'generated_at': datetime.now().isoformat(),
    'total_companies': len(services),
    'enrichment_stats': {
        'with_address': len([s for s in services if s.get('address')]),
        'with_emails': len([s for s in services if s.get('emails')]),
        'with_phones': len([s for s in services if s.get('phones')]),
        'with_social_media': len([s for s in services if s.get('social_media')]),
        'with_founding_year': len([s for s in services if s.get('founded')]),
        'with_employee_count': len([s for s in services if s.get('employees')]),
        'with_revenue': len([s for s in services if s.get('revenue')]),
        'publicly_traded': len([s for s in services if s.get('ticker')])
    },
    'by_type': {},
    'top_companies': []
}

# Count by type
for company in services:
    company_type = company.get('type', 'unknown')
    summary['by_type'][company_type] = summary['by_type'].get(company_type, 0) + 1

# Top 10 most complete companies
def completeness_score(company):
    score = 0
    if company.get('name'): score += 1
    if company.get('url'): score += 1
    if company.get('address'): score += 2
    if company.get('emails'): score += 2
    if company.get('phones'): score += 1
    if company.get('social_media'): score += 1
    if company.get('founded'): score += 1
    if company.get('employees'): score += 1
    if company.get('revenue'): score += 1
    if company.get('services'): score += 1
    return score

sorted_companies = sorted(services, key=completeness_score, reverse=True)
summary['top_companies'] = [
    {
        'name': c.get('name'),
        'score': completeness_score(c),
        'has_address': bool(c.get('address')),
        'has_email': bool(c.get('emails')),
        'has_phone': bool(c.get('phones')),
        'has_social': bool(c.get('social_media'))
    }
    for c in sorted_companies[:10]
]

with open(DATA_DIR / "enrichment_summary.json", 'w') as f:
    json.dump(summary, f, indent=2)

print("✅ Created: enrichment_summary.json")

# Print summary
print("\n" + "="*60)
print("📊 ENRICHMENT SUMMARY")
print("="*60)
print(f"\nTotal Companies: {summary['total_companies']}")
print(f"\nEnrichment Coverage:")
print(f"  Addresses:    {summary['enrichment_stats']['with_address']}/{summary['total_companies']} ({summary['enrichment_stats']['with_address']/summary['total_companies']*100:.1f}%)")
print(f"  Emails:       {summary['enrichment_stats']['with_emails']}/{summary['total_companies']} ({summary['enrichment_stats']['with_emails']/summary['total_companies']*100:.1f}%)")
print(f"  Phones:       {summary['enrichment_stats']['with_phones']}/{summary['total_companies']} ({summary['enrichment_stats']['with_phones']/summary['total_companies']*100:.1f}%)")
print(f"  Social Media: {summary['enrichment_stats']['with_social_media']}/{summary['total_companies']} ({summary['enrichment_stats']['with_social_media']/summary['total_companies']*100:.1f}%)")
print(f"  Founded Year: {summary['enrichment_stats']['with_founding_year']}/{summary['total_companies']} ({summary['enrichment_stats']['with_founding_year']/summary['total_companies']*100:.1f}%)")
print(f"  Employee Count: {summary['enrichment_stats']['with_employee_count']}/{summary['total_companies']} ({summary['enrichment_stats']['with_employee_count']/summary['total_companies']*100:.1f}%)")
print(f"  Revenue Data: {summary['enrichment_stats']['with_revenue']}/{summary['total_companies']} ({summary['enrichment_stats']['with_revenue']/summary['total_companies']*100:.1f}%)")
print(f"  Public Companies: {summary['enrichment_stats']['publicly_traded']}")

print(f"\n📈 Top 10 Most Complete Profiles:")
for i, company in enumerate(summary['top_companies'], 1):
    status = []
    if company['has_address']: status.append('addr')
    if company['has_email']: status.append('email')
    if company['has_phone']: status.append('phone')
    if company['has_social']: status.append('social')
    print(f"  {i}. {company['name']} (score: {company['score']}) - {', '.join(status)}")

print("\n✅ All exports complete!")
print(f"\nFiles created:")
print(f"  - lab_cleaning_services_enriched.csv (full data)")
print(f"  - wordpress_suppliers_enriched.csv (WP import)")
print(f"  - supplier_outreach_list.csv (contact list)")
print(f"  - enrichment_summary.json (statistics)")
