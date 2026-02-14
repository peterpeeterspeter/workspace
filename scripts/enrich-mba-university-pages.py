#!/usr/bin/env python3
"""
MBA Database Enrichment - Scrape Actual University MBA Pages

Strategy:
1. Use known URLs for top programs
2. Search for official MBA pages for others
3. Scrape and extract available fields
"""

import os
import csv
import asyncio
import re
from pathlib import Path
from datetime import datetime
from firecrawl import FirecrawlApp
from dotenv import load_dotenv

load_dotenv('/root/.openclaw/workspace/.env')

INPUT_CSV = '/root/.openclaw/media/inbound/file_8---9ea59e54-dd4e-40ee-90ef-620484a9eefb.csv'
OUTPUT_CSV = '/root/.openclaw/workspace/data/mba-enriched-university-pages.csv'
LOG_DIR = Path('/root/.openclaw/workspace/logs')
LOG_DIR.mkdir(parents=True, exist_ok=True)

api_key = os.getenv('FIRECRAWL_API_KEY')
app = FirecrawlApp(api_key=api_key)

log_file = LOG_DIR / f'mba-university-{datetime.now().strftime("%Y%m%d-%H%M%S")}.log'

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")
    with open(log_file, 'a') as f:
        f.write(f"[{timestamp}] {msg}\n")

# Known MBA program URLs (from top 5 + common schools)
KNOWN_URLS = {
    'usc-online-mba': 'https://www.marshall.usc.edu/programs/online-mba',
    'unc-online-mba': 'https://onlinemba.unc.edu/',
    'indiana-kelley-online-mba': 'https://kelley.iu.edu/programs/online-mba',
    'carnegie-mellon-online-mba': 'https://www.tepper.cmu.edu/online/online-mba',
    'florida-warrington-online-mba': 'https://warrington.ufl.edu/programs/online-mba',
    'harvard-university-master-of-business-administration': 'https://www.hbs.edu/mba/',
    'stanford-university-master-of-business-administration': 'https://www.gsb.stanford.edu/mba',
    'university-of-pennsylvania-wharton-master-of-business-administration': 'https://www.wharton.upenn.edu/mba/',
    'mit-sloan-master-of-business-administration': 'https://mitsloan.mit.edu/mba',
    'northwestern-university-kellogg-master-of-business-administration': 'https://www.kellogg.northwestern.edu/programs/mba',
    'university-of-chicago-booth-master-of-business-administration': 'https://www.chicagobooth.edu/programs/full-time-mba',
    'columbia-university-master-of-business-administration': 'https://www8.gsb.columbia.edu/mba',
    'university-of-california-berkeley-haas-master-of-business-administration': 'https://www.haas.berkeley.edu/mba',
    'yale-university-master-of-business-administration': 'https://som.yale.edu/mba',
    'duke-university-fuqua-master-of-business-administration': 'https://www.fuqua.duke.edu/mba',
}

def get_mba_url(slug, name):
    """Get MBA program URL from slug/name"""
    # Check known URLs first
    if slug in KNOWN_URLS:
        return KNOWN_URLS[slug]
    
    # Extract university name from slug
    # Remove common suffixes
    university = slug.replace('-online-mba', '').replace('-master-of-business-administration', '').replace('-mba', '')
    
    # Try common patterns
    patterns = [
        f"https://www.{university}.edu/mba",
        f"https://www.{university}.edu/business/mba",
        f"https://{university}.edu/programs/mba",
        f"https://onlinemba.{university}.edu/",
    ]
    
    return patterns[0]  # Return first pattern (may not exist)

def scrape_mba_page(url):
    """Scrape MBA program page"""
    try:
        log(f"  🌐 Scraping: {url}")
        result = app.scrape(url, formats=['markdown'], only_main_content=True)
        
        if result and hasattr(result, 'markdown') and result.markdown:
            return result.markdown
        else:
            log(f"  ⚠️ No markdown returned")
            return None
            
    except Exception as e:
        log(f"  ❌ Error: {str(e)[:100]}")
        return None

def extract_all_fields(markdown):
    """Extract ALL available MBA data from markdown"""
    if not markdown:
        return {}
    
    extracted = {}
    
    # Acceptance rate
    patterns = [
        r'acceptance rate[:\s]+(\d+\.?\d*)%?',
        r'(\d+\.?\d*)%?\s+acceptance',
        r'selectivity[:\s]+(\d+\.?\d*)%?',
        r'admit rate[:\s]+(\d+\.?\d*)%?',
    ]
    for pattern in patterns:
        m = re.search(pattern, markdown, re.IGNORECASE)
        if m:
            extracted['acceptanceRate'] = float(m.group(1))
            break
    
    # Class size
    patterns = [
        r'class size[:\s]+(\d+)',
        r'cohort size[:\s]+(\d+)',
        r'cohort[:\s]+(\d+)\s+students',
        r'enrollment[:\s]+(\d+)',
        r'average class size[:\s]+(\d+)',
    ]
    for pattern in patterns:
        m = re.search(pattern, markdown, re.IGNORECASE)
        if m:
            extracted['classSize'] = int(m.group(1))
            break
    
    # Average salary
    patterns = [
        r'\$(\d{2,3},?\d{3})\s+average salary',
        r'average salary[:\s]+\$(\d{2,3},?\d{3})',
        r'graduates earn[:\s]+\$(\d{2,3},?\d{3})',
        r'starting salary[:\s]+\$(\d{2,3},?\d{3})',
        r'median salary[:\s]+\$(\d{2,3},?\d{3})',
    ]
    for pattern in patterns:
        m = re.search(pattern, markdown, re.IGNORECASE)
        if m:
            salary_str = m.group(1).replace(',', '')
            extracted['avgSalaryPost'] = int(salary_str)
            break
    
    # US News ranking
    patterns = [
        r'U\.S\.? News[^#]*ranked\s+#?(\d+)',
        r'U\.S\.? News[^#]*#?(\d+)',
        r'#?(\d+)\s+in.*?U\.S\.? News',
        r'ranked\s+#?(\d+).*?U\.S\.? News',
        r'U.S. News.*?No\. (\d+)',
    ]
    for pattern in patterns:
        m = re.search(pattern, markdown, re.IGNORECASE)
        if m:
            extracted['usNewsRank'] = int(m.group(1))
            break
    
    # Fortune ranking
    patterns = [
        r'Fortune[^#]*ranked\s+#?(\d+)',
        r'Fortune[^#]*#?(\d+)',
        r'#?(\d+)\s+in.*?Fortune',
        r'ranked\s+#?(\d+).*?Fortune',
    ]
    for pattern in patterns:
        m = re.search(pattern, markdown, re.IGNORECASE)
        if m:
            extracted['fortuneRank'] = int(m.group(1))
            break
    
    # Application deadline
    patterns = [
        r'application deadline[:\s]+([A-Za-z]+\s+\d{1,2})',
        r'deadline[:\s]+([A-Za-z]+\s+\d{1,2})',
        r'apply by[:\s]+([A-Za-z]+\s+\d{1,2})',
    ]
    for pattern in patterns:
        m = re.search(pattern, markdown, re.IGNORECASE)
        if m:
            extracted['applicationDeadline'] = m.group(1)
            break
    
    # Tuition (if available)
    patterns = [
        r'tuition[:\s]+\$(\d{1,3},?\d{3},?\d{3})',
        r'\$(\d{1,3},?\d{3},?\d{3})\s+tuition',
        r'cost[:\s]+\$(\d{1,3},?\d{3},?\d{3})',
    ]
    for pattern in patterns:
        m = re.search(pattern, markdown, re.IGNORECASE)
        if m:
            tuition_str = m.group(1).replace(',', '')
            extracted['tuitionTotal'] = float(tuition_str)
            break
    
    # Generate better description if generic
    generic_desc = 'Comprehensive business education. Flexible online format designed for working professionals.'
    if len(markdown) > 200:
        # Extract first meaningful paragraph
        paragraphs = re.split(r'\n\n+', markdown)
        for para in paragraphs:
            # Skip headers, links, short lines
            if len(para) > 100 and not para.startswith('#') and 'http' not in para[:50]:
                # Clean markdown
                clean = re.sub(r'[#*`_\[\]]', ' ', para)
                clean = ' '.join(clean.split())
                desc = clean[:200] + '...'
                extracted['description'] = desc
                break
    
    return extracted

async def enrich_program(program, index, total):
    """Enrich a single MBA program"""
    slug = program.get('slug', '')
    name = program.get('name', f'Program {index}')
    
    log(f"\n[{index}/{total}] {name}")
    log(f"  Slug: {slug}")
    
    # Get URL
    url = get_mba_url(slug, name)
    if not url:
        log(f"  ⚠️ No URL found")
        return program
    
    # Scrape page
    markdown = scrape_mba_page(url)
    if not markdown:
        return program
    
    # Extract fields
    extracted = extract_all_fields(markdown)
    
    if extracted:
        for key, value in extracted.items():
            if value:
                program[key] = value
        
        log(f"  ✓ Extracted: {', '.join(extracted.keys())}")
    else:
        log(f"  ⚠️ No fields extracted")
    
    return program

async def main():
    log("=" * 60)
    log("MBA ENRICHMENT - ACTUAL UNIVERSITY PAGES")
    log("=" * 60)
    
    # Read CSV
    programs = []
    with open(INPUT_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        programs = list(reader)
    
    log(f"\n📊 Loaded {len(programs)} programs")
    
    # Process first 30 programs (batch mode)
    BATCH_SIZE = 30
    log(f"\n🚀 Processing first {BATCH_SIZE} programs...")
    
    enriched = []
    for i, program in enumerate(programs[:BATCH_SIZE], 1):
        try:
            updated = await enrich_program(program, i, BATCH_SIZE)
            enriched.append(updated)
            
            # Delay between requests
            await asyncio.sleep(1)
            
        except Exception as e:
            log(f"  ❌ Error: {str(e)}")
            enriched.append(program)
    
    # Save results
    output_path = Path(OUTPUT_CSV)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        if enriched:
            writer = csv.DictWriter(f, fieldnames=enriched[0].keys())
            writer.writeheader()
            writer.writerows(enriched)
    
    log(f"\n✓ Saved to: {OUTPUT_CSV}")
    log(f"  Processed: {len(enriched)} programs")
    
    # Statistics
    fields_filled = {}
    for program in enriched:
        for field in ['acceptanceRate', 'classSize', 'avgSalaryPost', 'usNewsRank', 'fortuneRank', 'applicationDeadline', 'tuitionTotal', 'description']:
            if program.get(field) and str(program[field]).strip():
                fields_filled[field] = fields_filled.get(field, 0) + 1
    
    log(f"\n📈 Fields filled:")
    for field, count in sorted(fields_filled.items()):
        log(f"  {field}: {count}")
    
    log("\n" + "=" * 60)
    log("COMPLETE")
    log("=" * 60)

if __name__ == '__main__':
    asyncio.run(main())
