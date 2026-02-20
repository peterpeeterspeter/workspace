#!/usr/bin/env python3
"""
Comprehensive MBA Program Data Scraper
Scrapes data from multiple ranking sources for onlinembaprograms.com affiliate site
"""

import requests
from bs4 import BeautifulSoup
import csv
import json
import time
from datetime import datetime
import re
from urllib.parse import urljoin, urlparse

# User agent to avoid blocking
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

# Data sources to scrape
SOURCES = {
    'us_news': {
        'name': 'US News',
        'base_url': 'https://www.usnews.com',
        'search_url': 'https://www.usnews.com/education/online-education/business-mba'
    },
    'poets_quants': {
        'name': 'Poets&Quants',
        'base_url': 'https://poetsandquants.com',
        'search_url': 'https://poetsandquants.com/rankings/'
    },
    'niche': {
        'name': 'Niche',
        'base_url': 'https://www.niche.com',
        'search_url': 'https://www.niche.com/colleges/search/best-online-mba/'
    },
    'princeton_review': {
        'name': 'Princeton Review',
        'base_url': 'https://www.princetonreview.com',
        'search_url': 'https://www.princetonreview.com/business-schools'
    }
}

# Known MBA programs with their URLs (manual seed data)
KNOWN_PROGRAMS = {
    'Indiana University Bloomington': {
        'url': 'https://kelley.iu.edu/programs/online-mba',
        'school': 'Indiana University',
        'program': 'Kelley Direct Online MBA',
        'accreditation': 'AACSB'
    },
    'University of North Carolina': {
        'url': 'https://onlinemba.unc.edu',
        'school': 'University of North Carolina',
        'program': 'MBA@UNC',
        'accreditation': 'AACSB'
    },
    'Carnegie Mellon University': {
        'url': 'https://www.tepper.cmu.edu/online-hybrid-mba',
        'school': 'Carnegie Mellon University',
        'program': 'Online Hybrid MBA',
        'accreditation': 'AACSB'
    },
    'University of Florida': {
        'url': 'https://warrington.ufl.edu/degrees/online-mba',
        'school': 'University of Florida',
        'program': 'Online MBA',
        'accreditation': 'AACSB'
    },
    'Arizona State University': {
        'url': 'https://wpcarey.asu.edu/online-degrees/mba',
        'school': 'Arizona State University',
        'program': 'Online MBA',
        'accreditation': 'AACSB'
    },
    'University of Southern California': {
        'url': 'https://www.marshall.usc.edu/programs/online-mba',
        'school': 'University of Southern California',
        'program': 'Online MBA',
        'accreditation': 'AACSB'
    },
    'University of Texas at Dallas': {
        'url': 'https://jindal.utdallas.edu/programs/online-mba',
        'school': 'University of Texas at Dallas',
        'program': 'Online MBA',
        'accreditation': 'AACSB'
    },
    'University of Massachusetts Amherst': {
        'url': 'https://www.isenberg.umass.edu/programs/online-mba',
        'school': 'University of Massachusetts Amherst',
        'program': 'Online MBA',
        'accreditation': 'AACSB'
    },
    'Liberty University': {
        'url': 'https://www.liberty.edu/business/online-mba',
        'school': 'Liberty University',
        'program': 'Online MBA',
        'accreditation': 'ACBSP'
    },
    'Southern New Hampshire University': {
        'url': 'https://www.snhu.edu/online-degrees/master/mba',
        'school': 'Southern New Hampshire University',
        'program': 'Online MBA',
        'accreditation': 'ACBSP'
    }
}

def scrape_page(url, timeout=30):
    """Scrape a single page with error handling"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=timeout)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

def extract_program_data(soup, source_url):
    """Extract MBA program data from a program page"""
    data = {
        'school_name': '',
        'program_name': '',
        'tuition_total': '',
        'tuition_per_credit': '',
        'in_state_tuition': '',
        'out_of_state_tuition': '',
        'format': '',
        'duration': '',
        'total_credits': '',
        'gmat_requirement': '',
        'gre_accepted': '',
        'acceptance_rate': '',
        'class_size': '',
        'avg_salary': '',
        'employment_rate': '',
        'accreditation': '',
        'specializations': '',
        'start_dates': '',
        'application_deadlines': '',
        'program_url': source_url,
        'source_url': source_url,
        'date_scraped': datetime.now().isoformat(),
        'confidence_score': 0
    }
    
    # Try to find school name
    title_tags = soup.find_all(['h1', 'h2', 'title'])
    for tag in title_tags:
        text = tag.get_text().strip()
        if 'MBA' in text or 'Business' in text or 'University' in text:
            if not data['school_name']:
                data['school_name'] = text
    
    # Try to extract tuition information
    tuition_keywords = ['tuition', 'cost', 'price', 'fee', 'per credit', 'total cost']
    text_content = soup.get_text().lower()
    
    # Look for tuition patterns
    for p in soup.find_all('p'):
        text = p.get_text()
        if any(kw in text.lower() for kw in tuition_keywords):
            if '$' in text:
                # Extract dollar amounts
                amounts = re.findall(r'\$[\d,]+', text)
                if amounts:
                    if 'per credit' in text.lower() or '/credit' in text.lower():
                        data['tuition_per_credit'] = amounts[0]
                    elif 'total' in text.lower() or 'program' in text.lower():
                        data['tuition_total'] = amounts[0]
    
    # Try to find program duration
    duration_patterns = [
        r'(\d+)\s*months?',
        r'(\d+)\s*years?',
        r'(\d+)\s*weeks?'
    ]
    for pattern in duration_patterns:
        matches = re.findall(pattern, text_content)
        if matches:
            data['duration'] = matches[0] + (' months' if 'month' in pattern else ' years')
            break
    
    # Try to find credits
    credit_patterns = [
        r'(\d+)\s*credits?',
        r'(\d+)\s*credit\s*hours?',
        r'(\d+)\s*semester\s*hours?'
    ]
    for pattern in credit_patterns:
        matches = re.findall(pattern, text_content)
        if matches:
            data['total_credits'] = matches[0]
            break
    
    # Try to find GMAT info
    if re.search(r'gmat.*required', text_content, re.I):
        data['gmat_requirement'] = 'Required'
    elif re.search(r'gmat.*optional', text_content, re.I):
        data['gmat_requirement'] = 'Optional'
    elif re.search(r'gmat.*waived?|waived?.*gmat', text_content, re.I):
        data['gmat_requirement'] = 'Waived'
    
    # GRE acceptance
    if re.search(r'gre.*accept', text_content, re.I):
        data['gre_accepted'] = 'Yes'
    
    # Try to find format
    if 'online' in text_content:
        data['format'] = 'Online'
    if 'hybrid' in text_content:
        if data['format']:
            data['format'] += '/Hybrid'
        else:
            data['format'] = 'Hybrid'
    
    # Calculate confidence score
    fields_filled = sum(1 for v in data.values() if v and v != '')
    total_fields = len(data) - 3  # Exclude metadata fields
    data['confidence_score'] = round((fields_filled / total_fields) * 100, 2)
    
    return data

def main():
    """Main scraping function"""
    programs = []
    
    print("=" * 80)
    print("MBA PROGRAM SCRAPER STARTING")
    print("=" * 80)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Known programs to scrape: {len(KNOWN_PROGRAMS)}")
    print()
    
    # Scrape known programs first
    for school, info in KNOWN_PROGRAMS.items():
        print(f"Scraping: {school} - {info['program']}")
        print(f"URL: {info['url']}")
        
        soup = scrape_page(info['url'])
        if soup:
            data = extract_program_data(soup, info['url'])
            # Override with known info
            data['school_name'] = info['school']
            data['program_name'] = info['program']
            data['accreditation'] = info.get('accreditation', '')
            data['program_url'] = info['url']
            
            programs.append(data)
            print(f"  ✓ Extracted data (confidence: {data['confidence_score']}%)")
        else:
            print(f"  ✗ Failed to scrape")
        
        time.sleep(2)  # Be respectful
    
    # Save to CSV
    output_file = '/root/.openclaw/workspace/research/onlinembaprograms-comprehensive.csv'
    
    if programs:
        fieldnames = [
            'school_name', 'program_name', 'tuition_total', 'tuition_per_credit',
            'in_state_tuition', 'out_of_state_tuition', 'format', 'duration',
            'total_credits', 'gmat_requirement', 'gre_accepted', 'acceptance_rate',
            'class_size', 'avg_salary', 'employment_rate', 'accreditation',
            'specializations', 'start_dates', 'application_deadlines',
            'program_url', 'source_url', 'date_scraped', 'confidence_score'
        ]
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(programs)
        
        print()
        print("=" * 80)
        print(f"✓ SAVED {len(programs)} programs to {output_file}")
        print("=" * 80)
        
        # Print summary
        print("\nSUMMARY:")
        print(f"  Total programs: {len(programs)}")
        print(f"  Average confidence: {sum(p['confidence_score'] for p in programs)/len(programs):.1f}%")
        print(f"  Programs with 80%+ confidence: {sum(1 for p in programs if p['confidence_score'] >= 80)}")
        
        # Print sample
        print("\nSAMPLE DATA (first 3 programs):")
        for i, p in enumerate(programs[:3], 1):
            print(f"\n{i}. {p['school_name']} - {p['program_name']}")
            print(f"   Tuition: {p['tuition_total'] or 'N/A'}")
            print(f"   Format: {p['format'] or 'N/A'}")
            print(f"   Duration: {p['duration'] or 'N/A'}")
            print(f"   Confidence: {p['confidence_score']}%")
    else:
        print("No programs scraped successfully!")
    
    return len(programs)

if __name__ == '__main__':
    main()
