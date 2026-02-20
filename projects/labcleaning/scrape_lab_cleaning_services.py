#!/usr/bin/env python3
"""
Lab Cleaning Services Scraper
Finds companies that provide lab cleaning, decontamination, and sterilization services
"""

import json
import csv
import re
import subprocess
from datetime import datetime
from urllib.parse import urljoin

OUTPUT_DIR = "/root/.openclaw/workspace/projects/labcleaning"

# Lab cleaning service providers
LAB_CLEANING_SERVICES = [
    {
        "name": "Triumvirate Environmental",
        "url": "https://www.triumvirate.com",
        "type": "cleaning_service",
        "description": "Laboratory cleaning, decontamination, and waste management",
        "services": ["Lab cleaning", "Chemical decontamination", "Waste disposal", "Emergency response"]
    },
    {
        "name": "Clean Harbors",
        "url": "https://www.cleanharbors.com",
        "type": "cleaning_service",
        "description": "Lab decontamination and hazardous waste services",
        "services": ["Hazardous waste", "Lab decommissioning", "Chemical cleaning", "Emergency spill response"]
    },
    {
        "name": "Veolia North America",
        "url": "https://www.veolianorthamerica.com",
        "type": "cleaning_service",
        "description": "Environmental services and lab waste management",
        "services": ["Waste management", "Lab cleaning", "Environmental compliance", "Water treatment"]
    },
    {
        "name": "STERIS",
        "url": "https://www.steris.com",
        "type": "sterilization",
        "description": "Lab sterilization and infection prevention",
        "services": ["Lab sterilization", "Equipment sterilization", "Infection control", "Validation services"]
    },
    {
        "name": "Ecolab",
        "url": "https://www.ecolab.com",
        "type": "cleaning_products",
        "description": "Cleaning and sanitizing solutions for labs",
        "services": ["Lab cleaning products", "Sanitization", "Water systems", "Infection prevention"]
    },
    {
        "name": "Diversey",
        "url": "https://www.diversey.com",
        "type": "cleaning_products",
        "description": "Cleaning and hygiene solutions",
        "services": ["Cleaning chemicals", "Lab hygiene", "Training", "Equipment"]
    },
    {
        "name": "Sealed Air",
        "url": "https://www.sealedair.com",
        "type": "cleaning_products",
        "description": "Cleaning and sanitization products",
        "services": ["Sanitization", "Cleaning systems", "Food safety", "Lab hygiene"]
    },
    {
        "name": "Stericycle",
        "url": "https://www.stericycle.com",
        "type": "waste_management",
        "description": "Medical and lab waste disposal",
        "services": ["Waste disposal", "Sharps disposal", "Lab waste", "Compliance solutions"]
    },
    {
        "name": "Sharps Compliance",
        "url": "https://www.sharpsinc.com",
        "type": "waste_management",
        "description": "Medical waste management solutions",
        "services": ["Waste disposal", "Mail-back programs", "Pharmaceutical waste", "Lab waste"]
    },
    {
        "name": "Daniels Health",
        "url": "https://danielshealth.com",
        "type": "waste_management",
        "description": "Healthcare and lab waste management",
        "services": ["Sharps disposal", "Lab waste", "Waste containers", "Sustainable solutions"]
    },
    {
        "name": "Republic Services",
        "url": "https://www.republicservices.com",
        "type": "waste_management",
        "description": "Environmental services including lab waste",
        "services": ["Waste disposal", "Recycling", "Lab waste services", "Sustainability"]
    },
    {
        "name": "Waste Management",
        "url": "https://www.wm.com",
        "type": "waste_management",
        "description": "Comprehensive waste services including labs",
        "services": ["Hazardous waste", "Lab disposal", "Environmental services", "Compliance"]
    },
    {
        "name": "Kimberly-Clark Professional",
        "url": "https://www.kcprofessional.com",
        "type": "cleaning_products",
        "description": "Lab cleaning and safety products",
        "services": ["Wipes", "Cleaning products", "PPE", "Lab supplies"]
    },
    {
        "name": "3M Health Care",
        "url": "https://www.3m.com/3M/en_US/healthcare/",
        "type": "cleaning_products",
        "description": "Healthcare and lab cleaning products",
        "services": ["Disinfectants", "Cleaning solutions", "Infection control", "Lab supplies"]
    },
    {
        "name": "CloroxPro",
        "url": "https://www.cloroxpro.com",
        "type": "cleaning_products",
        "description": "Professional cleaning and disinfection",
        "services": ["Disinfectants", "Cleaners", "Lab sanitation", "Training"]
    },
    {
        "name": "Betco",
        "url": "https://www.betco.com",
        "type": "cleaning_products",
        "description": "Professional cleaning solutions",
        "services": ["Cleaning chemicals", "Disinfectants", "Training", "Equipment"]
    },
    {
        "name": "ABC Laboratories",
        "url": "https://www.abclabs.com",
        "type": "analytical_lab",
        "description": "Lab testing and analytical services",
        "services": ["Analytical testing", "Lab services", "Research", "Testing"]
    },
    {
        "name": "Eurofins Scientific",
        "url": "https://www.eurofinsus.com",
        "type": "analytical_lab",
        "description": "Lab testing and analysis",
        "services": ["Lab testing", "Analytical services", "Research", "Quality control"]
    },
    {
        "name": "ALS Limited",
        "url": "https://www.alsglobal.com",
        "type": "analytical_lab",
        "description": "Laboratory testing services",
        "services": ["Lab testing", "Environmental testing", "Food testing", "Forensics"]
    },
    {
        "name": "NSF International",
        "url": "https://www.nsf.org",
        "type": "testing_certification",
        "description": "Lab testing and certification",
        "services": ["Lab certification", "Testing", "Standards", "Audits"]
    },
    {
        "name": "UL Solutions",
        "url": "https://www.ul.com",
        "type": "testing_certification",
        "description": "Safety testing and certification",
        "services": ["Lab testing", "Certification", "Safety testing", "Standards"]
    },
    {
        "name": "Intertek",
        "url": "https://www.intertek.com",
        "type": "testing_certification",
        "description": "Quality and safety testing",
        "services": ["Lab testing", "Inspection", "Certification", "Assurance"]
    },
    {
        "name": "SGS",
        "url": "https://www.sgs.com",
        "type": "testing_certification",
        "description": "Testing, inspection and certification",
        "services": ["Lab testing", "Inspection", "Certification", "Verification"]
    },
    {
        "name": "Bureau Veritas",
        "url": "https://www.bureauveritas.com",
        "type": "testing_certification",
        "description": "Testing, inspection and certification",
        "services": ["Lab testing", "Inspection", "Certification", "Compliance"]
    },
    {
        "name": "Noxilico",
        "url": "https://www.noxilico.com",
        "type": "lab_decommissioning",
        "description": "Lab decontamination and decommissioning",
        "services": ["Lab decommissioning", "Decontamination", "Chemical clearance", "Equipment disposal"]
    },
    {
        "name": "Chemistry Rx",
        "url": "https://www.chemistryrx.com",
        "type": "lab_services",
        "description": "Lab equipment and services",
        "services": ["Lab equipment", "Glassware cleaning", "Sterilization", "Calibration"]
    },
    {
        "name": "Avantor Services",
        "url": "https://avantorsciences.com",
        "type": "lab_services",
        "description": "Lab services and solutions",
        "services": ["Lab equipment", "Cleaning validation", "Calibration", "Training"]
    },
    {
        "name": "Thermo Fisher Scientific Services",
        "url": "https://www.thermofisher.com",
        "type": "lab_services",
        "description": "Lab equipment and service",
        "services": ["Equipment service", "Calibration", "Validation", "Training"]
    },
    {
        "name": "Agilent CrossLab",
        "url": "https://www.agilent.com",
        "type": "lab_services",
        "description": "Lab instrument services",
        "services": ["Instrument service", "Calibration", "Training", "Support"]
    },
    {
        "name": "Waters Corporation Services",
        "url": "https://www.waters.com",
        "type": "lab_services",
        "description": "Chromatography system services",
        "services": ["Instrument service", "Preventive maintenance", "Training", "Validation"]
    },
    {
        "name": "Shimadzu Scientific Instruments",
        "url": "https://www.ssi.shimadzu.com",
        "type": "lab_services",
        "description": "Analytical instrument services",
        "services": ["Service", "Support", "Training", "Calibration"]
    },
    {
        "name": "PerkinElmer Services",
        "url": "https://www.perkinelmer.com",
        "type": "lab_services",
        "description": "Lab equipment and services",
        "services": ["Instrument service", "Applications support", "Training", "Validation"]
    },
    {
        "name": "Beckman Coulter Life Sciences",
        "url": "https://www.beckmancoulter.com",
        "type": "lab_services",
        "description": "Centrifuge and lab services",
        "services": ["Service", "Preventive maintenance", "Training", "Validation"]
    },
    {
        "name": "Bio-Rad Laboratories Services",
        "url": "https://www.bio-rad.com",
        "type": "lab_services",
        "description": "Life science equipment service",
        "services": ["Service", "Support", "Training", "Applications"]
    },
    {
        "name": "Eppendorf Service",
        "url": "https://www.eppendorf.com",
        "type": "lab_services",
        "description": "Lab equipment service",
        "services": ["Service", "Calibration", "Training", "Repair"]
    },
    {
        "name": "Sartorius Services",
        "url": "https://www.sartorius.com",
        "type": "lab_services",
        "description": "Lab and bioprocess services",
        "services": ["Service", "Validation", "Training", "Applications"]
    },
    {
        "name": "Metler Toledo Service",
        "url": "https://www.mt.com",
        "type": "lab_services",
        "description": "Lab balance and scale service",
        "services": ["Calibration", "Service", "Training", "Validation"]
    },
    {
        "name": "Cytiva",
        "url": "https://www.cytiva.com",
        "type": "lab_services",
        "description": "Bioprocessing lab services",
        "services": ["Service", "Validation", "Training", "Applications"]
    },
    {
        "name": "Danaher",
        "url": "https://www.danaher.com",
        "type": "lab_services",
        "description": "Lab diagnostics and services",
        "services": ["Service", "Support", "Training", "Applications"]
    },
    {
        "name": "Labconco",
        "url": "https://www.labconco.com",
        "type": "equipment_manufacturer",
        "description": "Fume hoods and lab equipment",
        "services": ["Equipment", "Installation", "Service", "Certification"]
    },
    {
        "name": "NuAire",
        "url": "https://www.nuaire.com",
        "type": "equipment_manufacturer",
        "description": "Biological safety cabinets",
        "services": ["Equipment", "Installation", "Certification", "Service"]
    },
    {
        "name": "The Baker Company",
        "url": "https://www.bakerco.com",
        "type": "equipment_manufacturer",
        "description": "Biological safety cabinets",
        "services": ["Equipment", "Installation", "Certification", "Service"]
    },
    {
        "name": "Air Science",
        "url": "https://www.airscience.com",
        "type": "equipment_manufacturer",
        "description": "Fume hoods and enclosures",
        "services": ["Equipment", "Installation", "Service", "Filters"]
    },
    {
        "name": "Bertsche",
        "url": "https://www.bertsche.com",
        "type": "lab_decommissioning",
        "description": "Lab relocation and decommissioning",
        "services": ["Lab relocation", "Decommissioning", "Decontamination", "Moving"]
    },
    {
        "name": "H+H Laboratory Services",
        "url": "https://hhlab.com",
        "type": "lab_services",
        "description": "Lab equipment service",
        "services": ["Service", "Repair", "Calibration", "Training"]
    },
    {
        "name": "GenVault",
        "url": "https://www.genvault.com",
        "type": "lab_services",
        "description": "Sample management services",
        "services": ["Biobanking", "Sample storage", "Cold chain", "Tracking"]
    },
    {
        "name": "Brooks Life Sciences",
        "url": "https://www.brooks.com",
        "type": "lab_services",
        "description": "Sample management and automation",
        "services": ["Automation", "Sample management", "Storage", "Tracking"]
    },
    {
        "name": "Azenta Life Sciences",
        "url": "https://www.azenta.com",
        "type": "lab_services",
        "description": "Sample management and storage",
        "services": ["Biobanking", "Sample storage", "Cold chain", "Software"]
    },
    {
        "name": "Hamilton Company",
        "url": "https://www.hamiltoncompany.com",
        "type": "automation",
        "description": "Lab automation and liquid handling",
        "services": ["Automation", "Liquid handling", "Service", "Training"]
    },
    {
        "name": "Tecan",
        "url": "https://www.tecan.com",
        "type": "automation",
        "description": "Lab automation",
        "services": ["Automation", "Liquid handling", "Service", "Applications"]
    },
    {
        "name": "PerkinElmer Informatics",
        "url": "https://www.perkinelmerinformatics.com",
        "type": "software",
        "description": "Lab information management",
        "services": ["LIMS", "Software", "Training", "Support"]
    },
    {
        "name": "LabWare",
        "url": "https://www.labware.com",
        "type": "software",
        "description": "LIMS and laboratory software",
        "services": ["LIMS", "Software", "Implementation", "Training"]
    },
    {
        "name": "Thermo Fisher SampleManager",
        "url": "https://www.thermofisher.com",
        "type": "software",
        "description": "LIMS software",
        "services": ["LIMS", "Software", "Implementation", "Support"]
    },
    {
        "name": "Agilent OpenLAB",
        "url": "https://www.agilent.com",
        "type": "software",
        "description": "Lab software solutions",
        "services": ["Software", "ELN", "LIMS", "Support"]
    },
    {
        "name": "Waters NuGenesis",
        "url": "https://www.waters.com",
        "type": "software",
        "description": "Lab data management",
        "services": ["Software", "LIMS", "SDMS", "Training"]
    },
    {
        "name": "BIOVIA",
        "url": "https://www.3ds.com/products-services/biovia",
        "type": "software",
        "description": "Scientific software",
        "services": ["ELN", "LIMS", "Software", "Training"]
    },
    {
        "name": "IDBS",
        "url": "https://www.idbs.com",
        "type": "software",
        "description": "Bioinformatics software",
        "services": ["Software", "ELN", "Biobanking", "Support"]
    },
    {
        "name": "Labguru",
        "url": "https://www.labguru.com",
        "type": "software",
        "description": "Lab management platform",
        "services": ["Software", "ELN", "Inventory", "Training"]
    },
    {
        "name": "Benchling",
        "url": "https://www.benchling.com",
        "type": "software",
        "description": "Lab informatics platform",
        "services": ["Software", "ELN", "LIMS", "Support"]
    },
    {
        "name": "Science Exchange",
        "url": "https://www.scienceexchange.com",
        "type": "marketplace",
        "description": "Lab service marketplace",
        "services": ["Lab services", "Outsourcing", "Testing", "Research"]
    },
    {
        "name": " Scientist.com",
        "url": "https://www.scientist.com",
        "type": "marketplace",
        "description": "Research marketplace",
        "services": ["Lab services", "Outsourcing", "Research", "Testing"]
    }
]

def extract_emails(text):
    """Extract email addresses from text"""
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)
    valid_emails = [e for e in emails if not any(x in e for x in ['example.com', 'test.com', 'localhost', 'sentry'])]
    return list(set(valid_emails))

def extract_phones(text):
    """Extract phone numbers from text"""
    phone_patterns = [
        r'\(\d{3}\)\s*\d{3}[-.\s]?\d{4}',
        r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',
        r'\+1\s*\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',
    ]
    phones = []
    for pattern in phone_patterns:
        phones.extend(re.findall(pattern, text))
    cleaned = [p for p in phones if len(re.findall(r'\d', p)) >= 10]
    return list(set(cleaned))

def fetch_page(url):
    """Fetch page using curl"""
    try:
        cmd = f'curl -s -L -A "Mozilla/5.0" --max-time 10 "{url}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
        if result.returncode == 0:
            return result.stdout
    except:
        pass
    return ''

def scrape_company_details(company):
    """Scrape details for a cleaning service company"""
    print(f"\n🔍 {company['name']}")

    html = fetch_page(company['url'])

    if html:
        # Clean HTML
        text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()

        # Extract info
        emails = extract_emails(text)[:5]
        phones = extract_phones(text)[:5]

        # Extract title
        title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE)
        title = title_match.group(1).strip()[:100] if title_match else ''

        # Extract meta description
        desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']', html, re.IGNORECASE)
        description = desc_match.group(1).strip() if desc_match else ''

        company.update({
            'title': title,
            'meta_description': description,
            'emails': emails,
            'phones': phones,
            'scraped_at': datetime.now().isoformat()
        })

        print(f"  ✅ Emails: {len(emails)}, Phones: {len(phones)}")
    else:
        print(f"  ⚠️ Could not fetch page")

    return company

def main():
    """Main function"""
    print("🧪 Lab Cleaning Services Scraper")
    print("=" * 60)

    enhanced_companies = []

    for i, company in enumerate(LAB_CLEANING_SERVICES, 1):
        print(f"\n[{i}/{len(LAB_CLEANING_SERVICES)}] {company['name']}")

        try:
            enhanced = scrape_company_details(company)
            enhanced_companies.append(enhanced)

            if i % 10 == 0:
                # Save progress
                progress_file = f"{OUTPUT_DIR}/cleaning_services_progress_{i}.json"
                with open(progress_file, 'w') as f:
                    json.dump(enhanced_companies, f, indent=2)

        except Exception as e:
            print(f"  ❌ Error: {e}")
            enhanced_companies.append(company)

    # Save final results
    output_file = f"{OUTPUT_DIR}/lab_cleaning_services.json"
    with open(output_file, 'w') as f:
        json.dump(enhanced_companies, f, indent=2)

    # Save CSV
    csv_file = f"{OUTPUT_DIR}/lab_cleaning_services.csv"
    if enhanced_companies:
        keys = list(enhanced_companies[0].keys())
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(enhanced_companies)

    # Categorize by type
    by_type = {}
    for company in enhanced_companies:
        company_type = company.get('type', 'other')
        if company_type not in by_type:
            by_type[company_type] = []
        by_type[company_type].append(company)

    # Save categories
    for company_type, companies in by_type.items():
        type_file = f"{OUTPUT_DIR}/cleaning_{company_type}.json"
        with open(type_file, 'w') as f:
            json.dump(companies, f, indent=2)
        print(f"\n✅ Saved {len(companies)} {company_type} companies")

    print(f"\n📊 Summary:")
    print(f"   Total companies: {len(enhanced_companies)}")
    for company_type, companies in by_type.items():
        print(f"   - {company_type}: {len(companies)}")

    print(f"\n✅ Files saved to {OUTPUT_DIR}/")

if __name__ == "__main__":
    main()
