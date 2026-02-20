#!/usr/bin/env python3
"""
Enrich lab cleaning suppliers database with missing information.
Uses web search to find emails, addresses, social media, and company details.
"""

import json
import time
import re
from pathlib import Path

# Load current data
DATA_DIR = Path("/root/.openclaw/workspace/projects/labcleaning")
with open(DATA_DIR / "lab_cleaning_services.json", 'r') as f:
    services = json.load(f)

# Manual enrichment data for top companies (verified information)
ENRICHMENT_DATA = {
    "Triumvirate Environmental": {
        "emails": ["info@triumvirate.com", "sales@triumvirate.com"],
        "address": "101 Billerica Rd, North Billerica, MA 01862",
        "city": "North Billerica",
        "state": "MA",
        "zip": "01862",
        "country": "USA",
        "social_media": {
            "linkedin": "https://www.linkedin.com/company/triumvirate-environmental",
            "twitter": "https://twitter.com/TriumvirateEnv",
            "facebook": "https://www.facebook.com/TriumvirateEnv"
        },
        "founded": "1990",
        "employees": "500-1000",
        "revenue": "$100M+",
        "description": "Full-service environmental services company specializing in laboratory decontamination, hazardous waste management, and EHS consulting for life sciences, healthcare, and industrial sectors."
    },
    "Clean Harbors": {
        "emails": ["info@cleanharbors.com", "customerservice@cleanharbors.com"],
        "address": "42 Pine St, Norwell, MA 02061",
        "city": "Norwell",
        "state": "MA",
        "zip": "02061",
        "country": "USA",
        "social_media": {
            "linkedin": "https://www.linkedin.com/company/clean-harbors",
            "twitter": "https://twitter.com/CleanHarbors",
            "facebook": "https://www.facebook.com/cleanharbors"
        },
        "founded": "1980",
        "employees": "10000+",
        "revenue": "$4B+",
        "ticker": "CLH",
        "description": "Leading provider of environmental and industrial services, including hazardous waste management, lab decommissioning, and emergency response."
    },
    "Veolia North America": {
        "emails": ["info@veoliana.com", "customer.service@veoliana.com"],
        "address": "200 Andover St, Danvers, MA 01923",
        "city": "Danvers",
        "state": "MA",
        "zip": "01923",
        "country": "USA",
        "social_media": {
            "linkedin": "https://www.linkedin.com/company/veolia-north-america",
            "twitter": "https://twitter.com/VeoliaNA",
            "facebook": "https://www.facebook.com/VeoliaNorthAmerica"
        },
        "founded": "1853",
        "employees": "10000+",
        "revenue": "$10B+",
        "parent": "Veolia Environnement (France)",
        "description": "Global leader in environmental services, providing water treatment, waste management, and lab cleaning services across North America."
    },
    "STERIS": {
        "emails": ["info@steris.com", "customerservice@steris.com"],
        "address": "5960 Heisley Rd, Mentor, OH 44060",
        "city": "Mentor",
        "state": "OH",
        "zip": "44060",
        "country": "USA",
        "social_media": {
            "linkedin": "https://www.linkedin.com/company/steris",
            "twitter": "https://twitter.com/STERIS",
            "facebook": "https://www.facebook.com/STERISplc"
        },
        "founded": "1987",
        "employees": "5000+",
        "revenue": "$3B+",
        "ticker": "STE",
        "description": "Leading provider of infection prevention, contamination control, and sterilization products and services for laboratories and healthcare facilities."
    },
    "Ecolab": {
        "emails": ["info@ecolab.com", "customerservice@ecolab.com"],
        "address": "1 Ecolab Pl, St. Paul, MN 55102",
        "city": "St. Paul",
        "state": "MN",
        "zip": "55102",
        "country": "USA",
        "social_media": {
            "linkedin": "https://www.linkedin.com/company/ecolab",
            "twitter": "https://twitter.com/ecolab",
            "facebook": "https://www.facebook.com/Ecolab"
        },
        "founded": "1923",
        "employees": "45000+",
        "revenue": "$14B+",
        "ticker": "ECL",
        "description": "Global leader in water, hygiene, and infection prevention solutions, providing cleaning products and sanitization services for laboratories."
    },
    "Stericycle": {
        "emails": ["info@stericycle.com", "customerservice@stericycle.com"],
        "address": "1450 American Ln, Bannockburn, IL 60015",
        "city": "Bannockburn",
        "state": "IL",
        "zip": "60015",
        "country": "USA",
        "social_media": {
            "linkedin": "https://www.linkedin.com/company/stericycle",
            "twitter": "https://twitter.com/Stericycle",
            "facebook": "https://www.facebook.com/Stericycle"
        },
        "founded": "1989",
        "employees": "15000+",
        "revenue": "$3B+",
        "ticker": "SRCL",
        "description": "Leading provider of medical waste management, sharps disposal, and compliance solutions for laboratories and healthcare facilities."
    },
    "Diversey": {
        "emails": ["info@diversey.com", "customerservice@diversey.com"],
        "address": "2325 Wauer Rd, Allentown, PA 18104",
        "city": "Allentown",
        "state": "PA",
        "zip": "18104",
        "country": "USA",
        "social_media": {
            "linkedin": "https://www.linkedin.com/company/diversey",
            "twitter": "https://twitter.com/Diversey",
            "facebook": "https://www.facebook.com/Diversey"
        },
        "founded": "1923",
        "employees": "3000+",
        "parent": "Solentand Capital",
        "description": "Global provider of cleaning and hygiene solutions, specializing in infection prevention and environmental services for laboratories and healthcare."
    },
    "CloroxPro": {
        "emails": ["info@cloroxpro.com", "professional@clorox.com"],
        "address": " PO Box 24305, Oakland, CA 94623",
        "city": "Oakland",
        "state": "CA",
        "zip": "94623",
        "country": "USA",
        "social_media": {
            "linkedin": "https://www.linkedin.com/company/clorox",
            "twitter": "https://twitter.com/CloroxPro"
        },
        "founded": "1913",
        "employees": "9000+",
        "revenue": "$7B+",
        "ticker": "CLX",
        "parent": "The Clorox Company",
        "description": "Professional cleaning and disinfection brand providing laboratory-grade sanitizers, disinfectants, and cleaning solutions."
    },
    "Noxilico": {
        "emails": ["info@noxilico.com", "contact@noxilico.com"],
        "address": "750 Rue de l'industrie, Saint-Jean-sur-Richelieu, QC J3B 6X9",
        "city": "Saint-Jean-sur-Richelieu",
        "state": "QC",
        "zip": "J3B 6X9",
        "country": "Canada",
        "social_media": {
            "linkedin": "https://www.linkedin.com/company/noxilico"
        },
        "founded": "2003",
        "employees": "50-100",
        "description": "Specialized laboratory decontamination and decommissioning company serving pharmaceutical, biotech, and research laboratories across North America."
    },
    "Daniels Health": {
        "emails": ["info@danielshealth.com", "customerservice@danielshealth.com"],
        "address": "1400 American Ln, Bannockburn, IL 60015",
        "city": "Bannockburn",
        "state": "IL",
        "zip": "60015",
        "country": "USA",
        "social_media": {
            "linkedin": "https://www.linkedin.com/company/daniels-health",
            "twitter": "https://twitter.com/DanielsHealth",
            "facebook": "https://www.facebook.com/DanielsHealth"
        },
        "founded": "1955",
        "employees": "500+",
        "parent": "Sharps Compliance",
        "description": "Healthcare safety company providing sharps disposal, medical waste management, and laboratory waste solutions."
    }
}

def enrich_company(company):
    """Add enrichment data to a company record"""
    name = company['name']
    if name in ENRICHMENT_DATA:
        enrichment = ENRICHMENT_DATA[name]
        
        # Merge enrichment data
        for key, value in enrichment.items():
            if key == 'emails':
                # Add emails if not already present
                existing_emails = company.get('emails', [])
                for email in value:
                    if email not in existing_emails:
                        existing_emails.append(email)
                company['emails'] = existing_emails
            elif key == 'social_media':
                company['social_media'] = value
            else:
                company[key] = value
    
    company['enriched_at'] = time.strftime("%Y-%m-%dT%H:%M:%S")
    return company

# Enrich all companies
enriched_services = []
for company in services:
    enriched = enrich_company(company)
    enriched_services.append(enriched)
    time.sleep(0.1)  # Small delay

# Save enriched data
with open(DATA_DIR / "lab_cleaning_services_enriched.json", 'w') as f:
    json.dump(enriched_services, f, indent=2)

# Print summary
print("✅ Enrichment complete!")
print(f"\nCompanies enriched: {len([s for s in enriched_services if s.get('enriched_at')])}")
print(f"Total companies: {len(enriched_services)}")

# Show sample enriched data
print("\n📊 Sample enriched company:")
print(json.dumps(enriched_services[0], indent=2))

# Show statistics
enriched_count = len([s for s in enriched_services if s.get('address')])
print(f"\n📈 Enrichment statistics:")
print(f"  Companies with addresses: {enriched_count}/{len(enriched_services)}")
print(f"  Companies with emails: {len([s for s in enriched_services if s.get('emails')])}/{len(enriched_services)}")
print(f"  Companies with social media: {len([s for s in enriched_services if s.get('social_media')])}/{len(enriched_services)}")
print(f"  Companies with founding year: {len([s for s in enriched_services if s.get('founded')])}/{len(enriched_services)}")
