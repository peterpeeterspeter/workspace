#!/usr/bin/env python3
"""
MBA Database Enrichment Script using Firecrawl v2

Strategy: Use find-mba.com URLs directly from descriptions
"""

import os
import csv
import json
import asyncio
import re
from pathlib import Path
from datetime import datetime
from firecrawl import FirecrawlApp

# Load environment
from dotenv import load_dotenv
load_dotenv('/root/.openclaw/workspace/.env')

# Configuration
INPUT_CSV = '/root/.openclaw/media/inbound/file_8---9ea59e54-dd4e-40ee-90ef-620484a9eefb.csv'
OUTPUT_CSV = '/root/.openclaw/workspace/data/mba-programs-enriched.csv'
LOG_DIR = Path('/root/.openclaw/workspace/logs')
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Firecrawl API
api_key = os.getenv('FIRECRAWL_API_KEY')
app = FirecrawlApp(api_key=api_key)

# Logging
log_file = LOG_DIR / f'mba-enrich-v2-{datetime.now().strftime("%Y%m%d-%H%M%S")}.log'

def log(message):
    """Write to log file and print"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"[{timestamp}] {message}"
    print(msg)
    with open(log_file, 'a') as f:
        f.write(msg + '\n')

def extract_findmba_url(program):
    """Extract find-mba.com URL from description"""
    description = program.get('description', '')

    # Find all find-mba.com URLs
    urls = re.findall(r'https://find-mba\.com/[^\s\)]+', description)

    if urls:
        # Return the first find-mba.com URL
        return urls[0]

    return None

def needs_enrichment(program):
    """Check if program needs enrichment"""
    missing_fields = []

    if not program.get('acceptanceRate') or str(program['acceptanceRate']).strip() == '':
        missing_fields.append('acceptanceRate')

    if not program.get('classSize') or str(program['classSize']).strip() == '':
        missing_fields.append('classSize')

    if not program.get('avgSalaryPost') or str(program['avgSalaryPost']).strip() == '':
        missing_fields.append('avgSalaryPost')

    if not program.get('usNewsRank') or str(program['usNewsRank']).strip() == '':
        missing_fields.append('usNewsRank')

    if not program.get('fortuneRank') or str(program['fortuneRank']).strip() == '':
        missing_fields.append('fortuneRank')

    return missing_fields

def scrape_findmba_page(url, program_name):
    """Scrape find-mba.com page using Firecrawl"""
    try:
        log(f"  🌐 Scraping: {url}")

        result = app.scrape(
            url,
            formats=['markdown'],
            only_main_content=True,
        )

        if result and 'markdown' in result:
            return result
        else:
            log(f"  ⚠️ No content returned")
            return None

    except Exception as e:
        log(f"  ❌ Error: {str(e)}")
        return None

def extract_mba_data(content, program_name):
    """Extract MBA data from find-mba.com markdown content"""
    if not content or 'markdown' not in content:
        return {}

    markdown = content['markdown']
    extracted = {}

    # Acceptance rate
    patterns = [
        r'acceptance rate[:\s]+(\d+\.?\d*)%?',
        r'(\d+\.?\d*)%?\s+acceptance',
        r'selectivity[:\s]+(\d+\.?\d*)%?',
    ]
    for pattern in patterns:
        match = re.search(pattern, markdown, re.IGNORECASE)
        if match:
            extracted['acceptanceRate'] = float(match.group(1))
            break

    # Class size
    patterns = [
        r'class size[:\s]+(\d+)',
        r'(\d+)\s+students.*class',
        r'cohort[:\s]+(\d+)',
        r'enrollment[:\s]+(\d+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, markdown, re.IGNORECASE)
        if match:
            extracted['classSize'] = int(match.group(1))
            break

    # Average salary
    patterns = [
        r'\$(\d{2,3},?\d{3})\s+average',
        r'average.*?\$(\d{2,3},?\d{3})',
        r'salary.*?\$(\d{2,3},?\d{3})',
        r'graduates.*?\$(\d{2,3},?\d{3})',
    ]
    for pattern in patterns:
        match = re.search(pattern, markdown, re.IGNORECASE)
        if match:
            salary_str = match.group(1).replace(',', '')
            extracted['avgSalaryPost'] = int(salary_str)
            break

    # US News ranking
    patterns = [
        r'U\.S\.? News[^#]*#?(\d+)',
        r'US News[^#]*ranked\s+#?(\d+)',
        r'#?(\d+)\s+in.*?U\.S\.? News',
        r'ranked\s+#?(\d+).*?U\.S\.? News',
    ]
    for pattern in patterns:
        match = re.search(pattern, markdown, re.IGNORECASE)
        if match:
            extracted['usNewsRank'] = int(match.group(1))
            break

    # Fortune ranking
    patterns = [
        r'Fortune[^#]*#?(\d+)',
        r'Fortune[^#]*ranked\s+#?(\d+)',
        r'#?(\d+)\s+in.*?Fortune',
        r'ranked\s+#?(\d+).*?Fortune',
    ]
    for pattern in patterns:
        match = re.search(pattern, markdown, re.IGNORECASE)
        if match:
            extracted['fortuneRank'] = int(match.group(1))
            break

    if extracted:
        log(f"  ✓ Extracted: {', '.join(extracted.keys())}")

    return extracted

async def enrich_program(program, index, total):
    """Enrich a single MBA program"""
    program_name = program.get('name', f'Program {index}')
    log(f"\n[{index}/{total}] {program_name}")

    # Check if enrichment needed
    missing = needs_enrichment(program)
    if not missing:
        log(f"  ⊘ Complete: All fields present")
        return program

    log(f"  → Missing: {', '.join(missing)}")

    # Extract find-mba.com URL
    url = extract_findmba_url(program)
    if not url:
        log(f"  ⚠️ No find-mba.com URL found")
        return program

    # Scrape page
    content = scrape_findmba_page(url, program_name)
    if not content:
        return program

    # Extract data
    extracted = extract_mba_data(content, program_name)
    if extracted:
        # Update program with extracted data
        for key, value in extracted.items():
            if value:
                program[key] = value

    return program

async def main():
    """Main enrichment workflow"""
    log("=" * 60)
    log("MBA DATABASE ENRICHMENT V2 - find-mba.com URLs")
    log("=" * 60)

    # Read CSV
    programs = []
    with open(INPUT_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            programs.append(row)

    log(f"\n📊 Loaded {len(programs)} programs")

    # Count programs with find-mba URLs
    with_urls = [p for p in programs if extract_findmba_url(p)]
    needs_work = [p for p in programs if needs_enrichment(p)]

    log(f"  Programs with find-mba.com URLs: {len(with_urls)}")
    log(f"  Programs needing enrichment: {len(needs_work)}")

    # Process first 20 programs as batch
    BATCH_SIZE = 20
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
        for field in ['acceptanceRate', 'classSize', 'avgSalaryPost', 'usNewsRank', 'fortuneRank']:
            if program.get(field) and str(program[field]).strip():
                fields_filled[field] = fields_filled.get(field, 0) + 1

    log(f"\n📈 Fields filled:")
    for field, count in fields_filled.items():
        log(f"  {field}: {count}")

    log("\n" + "=" * 60)
    log("ENRICHMENT COMPLETE")
    log("=" * 60)

if __name__ == '__main__':
    asyncio.run(main())
