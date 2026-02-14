#!/usr/bin/env python3
"""
MBA Database Enrichment - Search-Based Approach

For each MBA program:
1. Search for "[University] MBA acceptance rate", "class size", "salary", "rankings"
2. Scrape the found pages
3. Extract available data
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
OUTPUT_CSV = '/root/.openclaw/workspace/data/mba-enriched-search-based.csv'
LOG_DIR = Path('/root/.openclaw/workspace/logs')
LOG_DIR.mkdir(parents=True, exist_ok=True)

api_key = os.getenv('FIRECRAWL_API_KEY')
app = FirecrawlApp(api_key=api_key)

log_file = LOG_DIR / f'mba-search-{datetime.now().strftime("%Y%m%d-%H%M%S")}.log'

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")
    with open(log_file, 'a') as f:
        f.write(f"[{timestamp}] {msg}\n")

def clean_university_name(slug, name):
    """Extract clean university name from slug/name"""
    # Remove common suffixes
    university = slug.replace('-online-mba', '').replace('-master-of-business-administration', '').replace('-mba', '')
    university = university.replace('-', ' ')
    return university.title()

def search_and_scrape(university, search_term):
    """Search for a stat and scrape the result"""
    try:
        # Construct search query
        query = f"{university} MBA {search_term}"
        log(f"  🔍 Searching: {query}")
        
        # Note: Firecrawl doesn't have search - we'd need to use browser tool or external search
        # For now, return None to indicate we need search capability
        return None
        
    except Exception as e:
        log(f"  ❌ Search error: {str(e)[:100]}")
        return None

def extract_field_from_page(markdown, field_type):
    """Extract specific field from page content"""
    if not markdown:
        return None
    
    if field_type == 'acceptanceRate':
        patterns = [
            r'acceptance rate[:\s]+(\d+\.?\d*)%?',
            r'(\d+\.?\d*)%?\s+acceptance',
            r'selectivity[:\s]+(\d+\.?\d*)%?',
        ]
        for pattern in patterns:
            m = re.search(pattern, markdown, re.IGNORECASE)
            if m:
                return float(m.group(1))
    
    elif field_type == 'classSize':
        patterns = [
            r'class size[:\s]+(\d+)',
            r'cohort size[:\s]+(\d+)',
            r'enrollment[:\s]+(\d+)',
        ]
        for pattern in patterns:
            m = re.search(pattern, markdown, re.IGNORECASE)
            if m:
                return int(m.group(1))
    
    elif field_type == 'avgSalaryPost':
        patterns = [
            r'\$(\d{2,3},?\d{3})\s+average salary',
            r'average salary[:\s]+\$(\d{2,3},?\d{3})',
            r'graduates earn[:\s]+\$(\d{2,3},?\d{3})',
        ]
        for pattern in patterns:
            m = re.search(pattern, markdown, re.IGNORECASE)
            if m:
                return int(m.group(1).replace(',', ''))
    
    elif field_type == 'usNewsRank':
        patterns = [
            r'U\.S\.? News.*?ranked\s+#?(\d+)',
            r'ranked\s+#?(\d+).*?U\.S\.? News',
        ]
        for pattern in patterns:
            m = re.search(pattern, markdown, re.IGNORECASE)
            if m:
                return int(m.group(1))
    
    elif field_type == 'fortuneRank':
        patterns = [
            r'Fortune.*?ranked\s+#?(\d+)',
            r'ranked\s+#?(\d+).*?Fortune',
        ]
        for pattern in patterns:
            m = re.search(pattern, markdown, re.IGNORECASE)
            if m:
                return int(m.group(1))
    
    return None

async def enrich_program_search(program, index, total):
    """Enrich program using search-based approach"""
    slug = program.get('slug', '')
    name = program.get('name', f'Program {index}')
    
    log(f"\n[{index}/{total}] {name}")
    
    # Clean university name
    university = clean_university_name(slug, name)
    log(f"  University: {university}")
    
    # Fields to search for
    fields_to_search = ['acceptanceRate', 'classSize', 'avgSalaryPost', 'usNewsRank', 'fortuneRank']
    
    extracted = {}
    for field in fields_to_search:
        # Skip if already has value
        if program.get(field) and str(program[field]).strip():
            continue
        
        # Search for this field
        search_term = {
            'acceptanceRate': 'acceptance rate 2024',
            'classSize': 'class size cohort',
            'avgSalaryPost': 'average salary graduates',
            'usNewsRank': 'US News ranking',
            'fortuneRank': 'Fortune MBA ranking',
        }.get(field, field)
        
        # Search and scrape
        page_content = search_and_scrape(university, search_term)
        
        if page_content:
            value = extract_field_from_page(page_content, field)
            if value:
                extracted[field] = value
                log(f"  ✓ Found {field}: {value}")
        
        # Small delay between searches
        await asyncio.sleep(0.5)
    
    # Update program with extracted data
    for key, value in extracted.items():
        program[key] = value
    
    return program

async def main():
    log("=" * 60)
    log("MBA ENRICHMENT - SEARCH-BASED APPROACH")
    log("=" * 60)
    
    # Read CSV
    programs = []
    with open(INPUT_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        programs = list(reader)
    
    log(f"\n📊 Loaded {len(programs)} programs")
    
    # Process first 10 as test
    BATCH_SIZE = 10
    log(f"\n🚀 Processing first {BATCH_SIZE} programs (search-based test)...")
    
    enriched = []
    for i, program in enumerate(programs[:BATCH_SIZE], 1):
        try:
            updated = await enrich_program_search(program, i, BATCH_SIZE)
            enriched.append(updated)
            
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
    
    # Statistics
    fields_filled = {}
    for program in enriched:
        for field in ['acceptanceRate', 'classSize', 'avgSalaryPost', 'usNewsRank', 'fortuneRank']:
            if program.get(field) and str(program[field]).strip():
                fields_filled[field] = fields_filled.get(field, 0) + 1
    
    log(f"\n📈 Fields filled:")
    for field, count in sorted(fields_filled.items()):
        log(f"  {field}: {count}")
    
    log("\n" + "=" * 60)
    log("COMPLETE")
    log("=" * 60)
    
    log("\n⚠️ NOTE: Search-based approach requires web_search integration")
    log("   Current implementation shows the structure")
    log("   To fully implement, need to:")
    log("   1. Use web_search tool to find relevant pages")
    log("   2. Use Firecrawl to scrape those pages")
    log("   3. Extract specific fields from scraped content")

if __name__ == '__main__':
    asyncio.run(main())
