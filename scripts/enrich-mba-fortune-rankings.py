#!/usr/bin/env python3
"""
MBA Database Enrichment - Fortune MBA Rankings Scraping

Scrape Fortune MBA rankings to get missing fields:
- acceptanceRate
- classSize
- avgSalaryPost
- fortuneRank

Fortune ranking pages are public and contain this data.
"""

import os
import csv
import re
from pathlib import Path
from datetime import datetime
from firecrawl import FirecrawlApp
from dotenv import load_dotenv

load_dotenv('/root/.openclaw/workspace/.env')

INPUT_CSV = '/root/.openclaw/workspace/data/mba-enriched-university-pages.csv'
OUTPUT_CSV = '/root/.openclaw/workspace/data/mba-fortune-enriched.csv'
LOG_DIR = Path('/root/.openclaw/workspace/logs')
LOG_DIR.mkdir(parents=True, exist_ok=True)

api_key = os.getenv('FIRECRAWL_API_KEY')
app = FirecrawlApp(api_key=api_key)

log_file = LOG_DIR / f'mba-fortune-{datetime.now().strftime("%Y%m%d-%H%M%S")}.log'

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")
    with open(log_file, 'a') as f:
        f.write(f"[{timestamp}] {msg}\n")

# Fortune MBA ranking URLs
FORTUNE_URLS = [
    'https://fortune.com/ranking/best-mba-programs/',
    'https://fortune.com/education/ranking/best-online-mba-programs/',
]

def normalize_name(name):
    """Normalize school names for matching"""
    # Remove common suffixes/prefixes
    name = name.lower()
    name = re.sub(r'\b(university|school|college|of|at|the)\b', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name

def scrape_fortune_ranking(url):
    """Scrape Fortune ranking page"""
    try:
        log(f"🌐 Scraping: {url}")
        result = app.scrape(url, formats=['markdown'], only_main_content=True)
        
        if result and hasattr(result, 'markdown') and result.markdown:
            log(f"✓ Scraped {len(result.markdown)} characters")
            return result.markdown
        else:
            log(f"⚠️ No markdown returned")
            return None
            
    except Exception as e:
        log(f"❌ Error: {str(e)[:100]}")
        return None

def extract_fortune_data(markdown):
    """Extract MBA data from Fortune ranking page"""
    if not markdown:
        return []
    
    programs = []
    
    # Split into sections by school/program
    # Fortune typically formats as: Rank. School Name - data points
    
    # Pattern to match ranking entries
    # Example: "1. Harvard Business School" or "#1. Harvard"
    entry_pattern = r'(?:#)?(\d+)\.\s+([^\n]+?)(?=\n(?:#)?\d+\.|$)'
    
    entries = re.findall(entry_pattern, markdown, re.MULTILINE | re.DOTALL)
    
    for rank, school_text in entries:
        rank = int(rank)
        school_name = school_text.strip()
        
        # Extract data from school text
        program = {
            'fortuneRank': rank,
            'schoolNameRaw': school_name,
        }
        
        # Acceptance rate
        m = re.search(r'(\d+\.?\d*)%?\s*(?:acceptance|admit)', school_text, re.IGNORECASE)
        if m:
            program['acceptanceRate'] = float(m.group(1))
        
        # Class size
        m = re.search(r'(\d+)\s*(?:students?|class|cohort)', school_text, re.IGNORECASE)
        if m:
            program['classSize'] = int(m.group(1))
        
        # Average salary
        m = re.search(r'\$?(\d{2,3},?\d{3})\s*(?:average salary|salary|earnings)', school_text, re.IGNORECASE)
        if m:
            salary_str = m.group(1).replace(',', '')
            program['avgSalaryPost'] = int(salary_str)
        
        # Tuition
        m = re.search(r'\$?(\d{1,3},?\d{3},?\d{3})\s*(?:tuition|cost)', school_text, re.IGNORECASE)
        if m:
            tuition_str = m.group(1).replace(',', '')
            program['tuitionTotal'] = float(tuition_str)
        
        programs.append(program)
    
    log(f"✓ Extracted {len(programs)} programs from Fortune")
    return programs

def load_mba_database():
    """Load existing MBA database"""
    programs = []
    
    with open(INPUT_CSV, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            programs.append(row)
    
    log(f"📊 Loaded {len(programs)} programs from database")
    return programs

def match_and_merge(mba_programs, fortune_data):
    """Match Fortune data to MBA programs by school name"""
    matched = 0
    unmatched_fortune = 0
    
    # Create name lookup for Fortune data
    fortune_lookup = {}
    for fp in fortune_data:
        norm_name = normalize_name(fp['schoolNameRaw'])
        fortune_lookup[norm_name] = fp
    
    log(f"📋 Fortune data: {len(fortune_lookup)} programs")
    
    for mba in mba_programs:
        mba_name = mba.get('name', '')
        mba_slug = mba.get('slug', '')
        
        # Try to match by slug first (more reliable)
        mba_norm = normalize_name(mba_slug.replace('-', ' '))
        
        # Look for partial match
        matched_fortune = None
        for fortune_key, fortune_data in fortune_lookup.items():
            if mba_norm in fortune_key or fortune_key in mba_norm:
                matched_fortune = fortune_data
                break
        
        if matched_fortune:
            # Merge fields
            if 'fortuneRank' in matched_fortune:
                mba['fortuneRank'] = matched_fortune['fortuneRank']
            if 'acceptanceRate' in matched_fortune:
                mba['acceptanceRate'] = matched_fortune['acceptanceRate']
            if 'classSize' in matched_fortune:
                mba['classSize'] = matched_fortune['classSize']
            if 'avgSalaryPost' in matched_fortune:
                mba['avgSalaryPost'] = matched_fortune['avgSalaryPost']
            if 'tuitionTotal' in matched_fortune and not mba.get('tuitionTotal'):
                mba['tuitionTotal'] = matched_fortune['tuitionTotal']
            
            matched += 1
        else:
            unmatched_fortune += 1
    
    log(f"✓ Matched: {matched} programs")
    log(f"⚠️ Unmatched: {unmatched_fortune} programs")
    
    return mba_programs

def save_enriched_data(programs):
    """Save enriched MBA database"""
    fieldnames = [
        'id', 'schoolId', 'name', 'slug', 'degreeType', 'format',
        'tuitionTotal', 'tuitionPerCredit', 'totalCredits', 'durationMonths',
        'gmatRequired', 'greAccepted', 'accreditation', 'specializations',
        'startDates', 'applicationDeadline', 'acceptanceRate', 'classSize',
        'avgSalaryPost', 'usNewsRank', 'fortuneRank', 'asyncPercentage',
        'description', 'pros', 'cons', 'ourRating', 'affiliateUrl',
        'leadPartner', 'isFeatured', 'isPublished', 'createdAt', 'updatedAt'
    ]
    
    with open(OUTPUT_CSV, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(programs)
    
    log(f"✓ Saved to: {OUTPUT_CSV}")

def main():
    log("=" * 60)
    log("MBA ENRICHMENT - FORTUNE RANKINGS")
    log("=" * 60)
    log("")
    
    # Load existing database
    mba_programs = load_mba_database()
    
    # Scrape Fortune rankings
    fortune_data = []
    for url in FORTUNE_URLS:
        markdown = scrape_fortune_ranking(url)
        if markdown:
            programs = extract_fortune_data(markdown)
            fortune_data.extend(programs)
    
    if not fortune_data:
        log("❌ No Fortune data extracted")
        return
    
    # Match and merge
    enriched = match_and_merge(mba_programs, fortune_data)
    
    # Save
    save_enriched_data(enriched)
    
    # Report coverage
    acceptance_rate_count = sum(1 for p in enriched if p.get('acceptanceRate'))
    class_size_count = sum(1 for p in enriched if p.get('classSize'))
    salary_count = sum(1 for p in enriched if p.get('avgSalaryPost'))
    fortune_rank_count = sum(1 for p in enriched if p.get('fortuneRank'))
    
    log("")
    log("📈 Coverage Report:")
    log(f"  acceptanceRate: {acceptance_rate_count} programs")
    log(f"  classSize: {class_size_count} programs")
    log(f"  avgSalaryPost: {salary_count} programs")
    log(f"  fortuneRank: {fortune_rank_count} programs")
    log()
    log("=" * 60)
    log("COMPLETE")
    log("=" * 60)

if __name__ == '__main__':
    main()
