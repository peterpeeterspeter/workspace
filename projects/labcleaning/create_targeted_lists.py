#!/usr/bin/env python3
"""
Create targeted export lists from the enriched database
"""

import json
from pathlib import Path
from datetime import datetime
import csv

DATA_DIR = Path("/root/.openclaw/workspace/projects/labcleaning")

def determine_tier(company):
    """Determine pricing tier based on company size"""
    revenue = company.get('revenue', '')

    if not revenue:
        return 'basic'

    if 'B+' in revenue:
        amount = float(revenue.replace('$', '').replace('B+', '').replace('+', ''))
        if amount >= 5:
            return 'elite'
        elif amount >= 1:
            return 'enterprise'
    elif 'M+' in revenue:
        amount = float(revenue.replace('$', '').replace('M+', '').replace('+', ''))
        if amount >= 500:
            return 'enterprise'
        elif amount >= 100:
            return 'business'
        elif amount >= 10:
            return 'professional'

    return 'basic'

def parse_revenue(revenue_str):
    """Parse revenue string to number"""
    try:
        if 'B+' in revenue_str:
            return float(revenue_str.replace('$', '').replace('B+', '').replace('+', '')) * 1000
        elif 'M+' in revenue_str:
            return float(revenue_str.replace('$', '').replace('M+', '').replace('+', ''))
        return 0
    except:
        return 0

# Load master database
with open(DATA_DIR / "lab_cleaning_services_master.json", 'r') as f:
    companies = json.load(f)

print(f"📊 Loaded {len(companies)} companies")

# 1. EMAIL OUTREACH LIST (Top priority)
print("\n📧 Creating email outreach list...")

email_companies = [c for c in companies if c.get('emails')]
email_outreach = []

for company in email_companies:
    primary_email = company['emails'][0] if company['emails'] else None
    if not primary_email:
        continue

    email_outreach.append({
        'company_name': company['name'],
        'primary_email': primary_email,
        'all_emails': ', '.join(company.get('emails', [])),
        'phone': company.get('phones', [''])[0] if company.get('phones') else '',
        'address': company.get('address', ''),
        'city': company.get('city', ''),
        'state': company.get('state', ''),
        'website': company.get('url', ''),
        'type': company.get('type', ''),
        'revenue': company.get('revenue', ''),
        'employees': company.get('employees', ''),
        'certifications': ', '.join(company.get('certifications', [])),
        'tier': determine_tier(company)
    })

# Sort by tier
email_outreach.sort(key=lambda x: x['tier'])

# Save as CSV
with open(DATA_DIR / "email_outreach_list.csv", 'w', newline='') as f:
    if email_outreach:
        writer = csv.DictWriter(f, fieldnames=email_outreach[0].keys())
        writer.writeheader()
        writer.writerows(email_outreach)

print(f"✅ Email outreach list: {len(email_outreach)} companies")

# 2. COMPANIES WITH CERTIFICATIONS (Quality signal)
print("\n🏆 Creating certified companies list...")

certified_companies = [c for c in companies if c.get('certifications')]
certified_list = []

for company in certified_companies:
    certified_list.append({
        'name': company['name'],
        'website': company.get('url', ''),
        'certifications': ', '.join(company.get('certifications', [])),
        'type': company.get('type', ''),
        'emails': ', '.join(company.get('emails', [])),
        'phones': ', '.join(company.get('phones', [])),
        'address': company.get('address', ''),
        'city': company.get('city', ''),
        'state': company.get('state', ''),
        'revenue': company.get('revenue', ''),
        'tier': determine_tier(company)
    })

certified_list.sort(key=lambda x: len(x['certifications'].split(', ')), reverse=True)

with open(DATA_DIR / "certified_companies.csv", 'w', newline='') as f:
    if certified_list:
        writer = csv.DictWriter(f, fieldnames=certified_list[0].keys())
        writer.writeheader()
        writer.writerows(certified_list)

print(f"✅ Certified companies: {len(certified_list)}")

# 3. LARGE COMPANIES (Revenue-based)
print("\n💰 Creating large companies list...")

large_companies = [c for c in companies if c.get('revenue') and '$' in c['revenue']]
large_list = []

for company in large_companies:
    large_list.append({
        'name': company['name'],
        'revenue': company.get('revenue', ''),
        'employees': company.get('employees', ''),
        'ticker': company.get('ticker', ''),
        'type': company.get('type', ''),
        'emails': ', '.join(company.get('emails', [])),
        'phones': ', '.join(company.get('phones', [])),
        'address': company.get('address', ''),
        'website': company.get('url', ''),
        'tier': determine_tier(company)
    })

large_list.sort(key=lambda x: parse_revenue(x['revenue']), reverse=True)

with open(DATA_DIR / "large_companies.csv", 'w', newline='') as f:
    if large_list:
        writer = csv.DictWriter(f, fieldnames=large_list[0].keys())
        writer.writeheader()
        writer.writerows(large_list)

print(f"✅ Large companies: {len(large_list)}")

# 4. CONTACT-DENSE LIST (Has phone + email)
print("\n📞 Creating contact-dense list...")

contact_dense = [c for c in companies if c.get('emails') and c.get('phones')]
contact_list = []

for company in contact_dense:
    contact_list.append({
        'name': company['name'],
        'email': company['emails'][0] if company.get('emails') else '',
        'phone': company['phones'][0] if company.get('phones') else '',
        'address': company.get('address', ''),
        'city': company.get('city', ''),
        'state': company.get('state', ''),
        'website': company.get('url', ''),
        'type': company.get('type', ''),
        'services': ', '.join(company.get('services', [])[:5]),
        'tier': determine_tier(company)
    })

contact_list.sort(key=lambda x: x['tier'])

with open(DATA_DIR / "contact_dense_list.csv", 'w', newline='') as f:
    if contact_list:
        writer = csv.DictWriter(f, fieldnames=contact_list[0].keys())
        writer.writeheader()
        writer.writerows(contact_list)

print(f"✅ Contact-dense companies: {len(contact_list)}")

# 5. BY STATE (for regional targeting)
print("\n🗺️ Creating state-based lists...")

states = {}
for company in companies:
    state = company.get('state', 'Unknown')
    if state not in states:
        states[state] = []
    states[state].append(company)

for state, state_companies in sorted(states.items()):
    if len(state_companies) < 2:
        continue

    state_list = []
    for company in state_companies:
        state_list.append({
            'name': company['name'],
            'city': company.get('city', ''),
            'address': company.get('address', ''),
            'emails': ', '.join(company.get('emails', [])),
            'phones': ', '.join(company.get('phones', [])),
            'website': company.get('url', ''),
            'type': company.get('type', ''),
            'tier': determine_tier(company)
        })

    state_list.sort(key=lambda x: x['tier'])

    filename = f"state_{state.replace(' ', '_').lower()}.csv"
    with open(DATA_DIR / filename, 'w', newline='') as f:
        if state_list:
            writer = csv.DictWriter(f, fieldnames=state_list[0].keys())
            writer.writeheader()
            writer.writerows(state_list)

print(f"✅ Created {len([s for s in states.keys() if len(states[s]) >= 2])} state lists")

# 6. BY TYPE (service categories)
print("\n📋 Creating type-based lists...")

types = {}
for company in companies:
    ctype = company.get('type', 'Unknown')
    if ctype not in types:
        types[ctype] = []
    types[ctype].append(company)

for ctype, type_companies in sorted(types.items()):
    if len(type_companies) < 2:
        continue

    type_list = []
    for company in type_companies:
        type_list.append({
            'name': company['name'],
            'website': company.get('url', ''),
            'description': company.get('description', '')[:100],
            'emails': ', '.join(company.get('emails', [])),
            'phones': ', '.join(company.get('phones', [])),
            'address': company.get('address', ''),
            'city': company.get('city', ''),
            'state': company.get('state', ''),
            'services': ', '.join(company.get('services', [])[:3])
        })

    filename = f"type_{ctype.replace('_', ' ').replace(' ', '_').lower()}.csv"
    with open(DATA_DIR / filename, 'w', newline='') as f:
        if type_list:
            writer = csv.DictWriter(f, fieldnames=type_list[0].keys())
            writer.writeheader()
            writer.writerows(type_list)

print(f"✅ Created {len([t for t in types.keys() if len(types[t]) >= 2])} type lists")

# 7. TOP COMPANIES RANKING
print("\n🏆 Creating top companies ranking...")

def score_company(company):
    score = 0
    if company.get('emails'):
        score += 10
    if company.get('phones'):
        score += 10
    if company.get('address'):
        score += 15
    if company.get('social_media'):
        score += 10
    if company.get('certifications'):
        score += 15
    if company.get('revenue'):
        score += 20
    if company.get('ticker'):
        score += 10
    if company.get('founded'):
        score += 5
    if company.get('employees'):
        score += 5
    return score

ranked_companies = sorted(companies, key=score_company, reverse=True)

top_50 = []
for i, company in enumerate(ranked_companies[:50], 1):
    top_50.append({
        'rank': i,
        'name': company['name'],
        'score': score_company(company),
        'type': company.get('type', ''),
        'emails': 'Yes' if company.get('emails') else 'No',
        'phones': 'Yes' if company.get('phones') else 'No',
        'address': 'Yes' if company.get('address') else 'No',
        'certifications': ', '.join(company.get('certifications', [])),
        'revenue': company.get('revenue', ''),
        'website': company.get('url', ''),
        'tier': determine_tier(company)
    })

with open(DATA_DIR / "top_50_companies.csv", 'w', newline='') as f:
    if top_50:
        writer = csv.DictWriter(f, fieldnames=top_50[0].keys())
        writer.writeheader()
        writer.writerows(top_50)

print(f"✅ Top 50 companies ranked")

# 8. FINAL STATISTICS
stats = {
    'total_companies': len(companies),
    'with_emails': len([c for c in companies if c.get('emails')]),
    'with_phones': len([c for c in companies if c.get('phones')]),
    'with_addresses': len([c for c in companies if c.get('address')]),
    'with_social_media': len([c for c in companies if c.get('social_media')]),
    'with_certifications': len([c for c in companies if c.get('certifications')]),
    'with_revenue': len([c for c in companies if c.get('revenue')]),
    'public_companies': len([c for c in companies if c.get('ticker')]),
    'by_type': {k: len(v) for k, v in types.items() if len(v) >= 2},
    'by_state': {k: len(v) for k, v in states.items() if len(v) >= 2},
    'top_10': [{'name': c['name'], 'score': score_company(c)} for c in ranked_companies[:10]],
    'generated_at': datetime.now().isoformat()
}

with open(DATA_DIR / "final_statistics.json", 'w') as f:
    json.dump(stats, f, indent=2)

print(f"\n✅ All targeted lists created!")
print(f"\n📊 Final Statistics:")
print(f"  Total Companies: {stats['total_companies']}")
print(f"  With Emails: {stats['with_emails']} ({stats['with_emails']/stats['total_companies']*100:.1f}%)")
print(f"  With Phones: {stats['with_phones']} ({stats['with_phones']/stats['total_companies']*100:.1f}%)")
print(f"  With Addresses: {stats['with_addresses']} ({stats['with_addresses']/stats['total_companies']*100:.1f}%)")
print(f"  With Certifications: {stats['with_certifications']} ({stats['with_certifications']/stats['total_companies']*100:.1f}%)")
print(f"  Public Companies: {stats['public_companies']}")
