#!/usr/bin/env python3
"""
MBA Database Enrichment Script using Firecrawl

Scrapes university MBA program pages to fill missing fields:
- acceptanceRate
- classSize
- avgSalaryPost
- usNewsRank
- fortuneRank
- applicationDeadline
- Better descriptions
"""

import os
import csv
import json
import asyncio
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
if not api_key:
    raise ValueError("FIRECRAWL_API_KEY not found in .env")

app = FirecrawlApp(api_key=api_key)

# Logging setup
log_file = LOG_DIR / f'mba-enrich-{datetime.now().strftime("%Y%m%d-%H%M%S")}.log'

def log(message):
    """Write to log file and print"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"[{timestamp}] {message}"
    print(msg)
    with open(log_file, 'a') as f:
        f.write(msg + '\n')

def read_mba_csv():
    """Read MBA programs from CSV"""
    programs = []
    with open(INPUT_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            programs.append(row)
    log(f"✓ Loaded {len(programs)} programs from CSV")
    return programs

def needs_enrichment(program):
    """Check if program needs enrichment (has missing critical fields)"""
    missing_fields = []

    # Check critical fields
    if not program.get('acceptanceRate') or program['acceptanceRate'].strip() == '':
        missing_fields.append('acceptanceRate')

    if not program.get('classSize') or program['classSize'].strip() == '':
        missing_fields.append('classSize')

    if not program.get('avgSalaryPost') or program['avgSalaryPost'].strip() == '':
        missing_fields.append('avgSalaryPost')

    if not program.get('usNewsRank') or program['usNewsRank'].strip() == '':
        missing_fields.append('usNewsRank')

    if not program.get('fortuneRank') or program['fortuneRank'].strip() == '':
        missing_fields.append('fortuneRank')

    # Check for generic description
    desc = program.get('description', '')
    generic_desc = 'Comprehensive business education. Flexible online format designed for working professionals.'
    if desc == generic_desc or not desc or desc.strip() == '':
        missing_fields.append('description')

    return missing_fields

def construct_university_url(program):
    """Construct university MBA program URL from slug/name"""
    slug = program.get('slug', '')
    name = program.get('name', '')
    description = program.get('description', '')

    # If slug contains a URL, extract it (find-mba.com links)
    if 'http' in slug:
        import re
        urls = re.findall(r'https?://[^\s\)]+', slug)
        if urls:
            return urls[0]

    # If description contains find-mba.com links, extract them
    if 'find-mba.com' in description:
        import re
        urls = re.findall(r'https?://[^\s\)]+', description)
        if urls:
            return urls[0]

    # Otherwise construct URL from university name
    # Parse university name from slug
    # Example: "usc-online-mba" -> "https://www.marshall.usc.edu/programs/online-mba"
    # Example: "unc-online-mba" -> "https://onlinemba.unc.edu/"

    # Hardcoded mappings for top programs
    known_urls = {
        'usc-online-mba': 'https://www.marshall.usc.edu/programs/online-mba',
        'unc-online-mba': 'https://onlinemba.unc.edu/',
        'indiana-kelley-online-mba': 'https://kelley.iu.edu/programs/online-mba',
        'carnegie-mellon-online-mba': 'https://www.tepper.cmu.edu/online/online-mba',
        'florida-warrington-online-mba': 'https://warrington.ufl.edu/programs/online-mba',
        'harvard-university-master-of-business-administration': 'https://www.hbs.edu/mba/',
        'stanford-university-master-of-business-administration': 'https://www.gsb.stanford.edu/mba',
        'university-of-pennsylvania-wharton-master-of-business-administration': 'https://www.wharton.upenn.edu/mba/',
    }

    if slug in known_urls:
        return known_urls[slug]

    # Generic construction from slug
    # Remove common prefixes/suffixes
    university = slug.replace('-online-mba', '').replace('-master-of-business-administration', '')

    # Try common patterns
    patterns = [
        f"https://www.{university}.edu/mba",
        f"https://www.{university}.edu/business/mba",
        f"https://{university}.edu/programs/mba",
        f"https://onlinemba.{university}.edu/",
    ]

    return patterns[0] if patterns else None

def scrape_mba_program(url, program_name):
    """Scrape MBA program page using Firecrawl"""
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
            log(f"  ⚠️ No content returned for {program_name}")
            return None

    except Exception as e:
        log(f"  ❌ Error scraping {url}: {str(e)}")
        return None

def extract_mba_data(content, program_name):
    """Extract MBA program data from scraped content"""
    if not content or 'markdown' not in content:
        return {}

    markdown = content['markdown']
    extracted = {}

    # Extract acceptance rate
    import re

    # Look for acceptance rate patterns
    acceptance_patterns = [
        r'acceptance rate[:\s]+(\d+\.?\d*)%?',
        r'(\d+\.?\d*)%?\s+acceptance rate',
        r'accept[^\d]*(\d+\.?\d*)%?',
    ]
    for pattern in acceptance_patterns:
        match = re.search(pattern, markdown, re.IGNORECASE)
        if match:
            extracted['acceptanceRate'] = float(match.group(1))
            break

    # Extract class size
    class_size_patterns = [
        r'class size[:\s]+(\d+)',
        r'(\d+)\s+students',
        r'cohort[:\s]+(\d+)',
        r'average class size[:\s]+(\d+)',
    ]
    for pattern in class_size_patterns:
        match = re.search(pattern, markdown, re.IGNORECASE)
        if match:
            extracted['classSize'] = int(match.group(1))
            break

    # Extract average salary
    salary_patterns = [
        r'\$(\d{2,3},?\d{3})\s+average salary',
        r'average salary[:\s]+\$(\d{2,3},?\d{3})',
        r'graduates earn[:\s]+\$(\d{2,3},?\d{3})',
        r'salary[:\s]+\$(\d{2,3},?\d{3})',
    ]
    for pattern in salary_patterns:
        match = re.search(pattern, markdown, re.IGNORECASE)
        if match:
            # Remove commas and convert to int
            salary_str = match.group(1).replace(',', '')
            extracted['avgSalaryPost'] = int(salary_str)
            break

    # Extract US News ranking
    usnews_patterns = [
        r'U\.S\.? News[^#]*#?(\d+)',
        r'US News[^#]*ranked\s+#?(\d+)',
        r'ranked\s+#?(\d+)\s+by\s+U\.S\.? News',
    ]
    for pattern in usnews_patterns:
        match = re.search(pattern, markdown, re.IGNORECASE)
        if match:
            extracted['usNewsRank'] = int(match.group(1))
            break

    # Extract Fortune ranking
    fortune_patterns = [
        r'Fortune[^#]*#?(\d+)',
        r'Fortune[^#]*ranked\s+#?(\d+)',
        r'ranked\s+#?(\d+)\s+by\s+Fortune',
    ]
    for pattern in fortune_patterns:
        match = re.search(pattern, markdown, re.IGNORECASE)
        if match:
            extracted['fortuneRank'] = int(match.group(1))
            break

    # Extract application deadline
    deadline_patterns = [
        r'application deadline[:\s]+([A-Za-z]+\s+\d{1,2})',
        r'deadline[:\s]+([A-Za-z]+\s+\d{1,2})',
        r'apply by[:\s]+([A-Za-z]+\s+\d{1,2})',
    ]
    for pattern in deadline_patterns:
        match = re.search(pattern, markdown, re.IGNORECASE)
        if match:
            extracted['applicationDeadline'] = match.group(1)
            break

    # Generate better description if generic
    generic_desc = 'Comprehensive business education. Flexible online format designed for working professionals.'
    if len(markdown) > 200:
        # Extract first 200 chars as description
        desc = markdown[:200].strip()
        # Clean up markdown formatting
        desc = re.sub(r'[#*`]', '', desc)
        desc = ' '.join(desc.split()[:30])  # First 30 words
        extracted['description'] = desc + '...'

    log(f"  ✓ Extracted: {', '.join(extracted.keys())}")
    return extracted

async def enrich_program(program, index, total):
    """Enrich a single MBA program"""
    program_name = program.get('name', f'Program {index}')
    log(f"\n[{index}/{total}] Processing: {program_name}")

    # Check if enrichment needed
    missing = needs_enrichment(program)
    if not missing:
        log(f"  ⊘ Skipping: All fields present")
        return program

    log(f"  → Missing fields: {', '.join(missing)}")

    # Construct URL
    url = construct_university_url(program)
    if not url:
        log(f"  ⚠️ Could not construct URL for {program_name}")
        return program

    # Scrape page
    content = scrape_mba_program(url, program_name)
    if not content:
        return program

    # Extract data
    extracted = extract_mba_data(content, program_name)
    if extracted:
        # Update program with extracted data
        for key, value in extracted.items():
            if value:  # Only update if we found a value
                program[key] = value

        log(f"  ✓ Updated {len(extracted)} fields for {program_name}")

    return program

async def main():
    """Main enrichment workflow"""
    log("=" * 60)
    log("MBA DATABASE ENRICHMENT STARTED")
    log("=" * 60)

    # Read CSV
    programs = read_mba_csv()

    # Count programs needing enrichment
    needs_work = [p for p in programs if needs_enrichment(p)]
    log(f"\n📊 Summary:")
    log(f"  Total programs: {len(programs)}")
    log(f"  Need enrichment: {len(needs_work)}")
    log(f"  Complete: {len(programs) - len(needs_work)}")

    # Enrich programs (limit to first 10 for testing)
    BATCH_SIZE = 10
    log(f"\n🚀 Processing first {BATCH_SIZE} programs (batch mode)...")

    enriched = []
    for i, program in enumerate(programs[:BATCH_SIZE], 1):
        try:
            updated = await enrich_program(program, i, min(BATCH_SIZE, len(programs)))
            enriched.append(updated)

            # Small delay between requests
            await asyncio.sleep(2)

        except Exception as e:
            log(f"  ❌ Error processing program {i}: {str(e)}")
            enriched.append(program)

    # Write enriched CSV
    output_path = Path(OUTPUT_CSV)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        if enriched:
            writer = csv.DictWriter(f, fieldnames=enriched[0].keys())
            writer.writeheader()
            writer.writerows(enriched)

    log(f"\n✓ Enriched CSV saved to: {OUTPUT_CSV}")
    log(f"  Programs processed: {len(enriched)}")

    # Statistics
    fields_filled = {}
    for program in enriched:
        for field in ['acceptanceRate', 'classSize', 'avgSalaryPost', 'usNewsRank', 'fortuneRank']:
            if program.get(field) and str(program[field]).strip():
                fields_filled[field] = fields_filled.get(field, 0) + 1

    log(f"\n📈 Fields filled:")
    for field, count in fields_filled.items():
        log(f"  {field}: {count} programs")

    log("\n" + "=" * 60)
    log("MBA DATABASE ENRICHMENT COMPLETE")
    log("=" * 60)

if __name__ == '__main__':
    asyncio.run(main())
