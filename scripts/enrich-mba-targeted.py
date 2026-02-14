#!/usr/bin/env python3
"""
MBA Database Enrichment - Target find-mba.com URLs

Processes rows 25+ where find-mba.com URLs actually exist
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
OUTPUT_CSV = '/root/.openclaw/workspace/data/mba-enriched-targeted.csv'
LOG_DIR = Path('/root/.openclaw/workspace/logs')
LOG_DIR.mkdir(parents=True, exist_ok=True)

api_key = os.getenv('FIRECRAWL_API_KEY')
app = FirecrawlApp(api_key=api_key)

log_file = LOG_DIR / f'mba-targeted-{datetime.now().strftime("%Y%m%d-%H%M%S")}.log'

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")
    with open(log_file, 'a') as f:
        f.write(f"[{timestamp}] {msg}\n")

def extract_findmba_urls(description):
    """Extract all find-mba.com URLs from description"""
    if not description:
        return []
    return re.findall(r'https://find-mba\.com/[^\s\)]+', description)

def scrape_findmba(url):
    """Scrape find-mba.com page"""
    try:
        log(f"  🌐 Scraping: {url}")
        result = app.scrape(url, formats=['markdown'], only_main_content=True)
        if result and 'markdown' in result:
            return result['markdown']
        return None
    except Exception as e:
        log(f"  ❌ Error: {str(e)}")
        return None

def extract_fields(markdown):
    """Extract MBA fields from markdown"""
    extracted = {}

    # Acceptance rate
    for pattern in [r'acceptance rate[:\s]+(\d+\.?\d*)%?', r'(\d+\.?\d*)%?\s+acceptance', r'selectivity[:\s]+(\d+\.?\d*)%?']:
        m = re.search(pattern, markdown, re.IGNORECASE)
        if m:
            extracted['acceptanceRate'] = float(m.group(1))
            break

    # Class size
    for pattern in [r'class size[:\s]+(\d+)', r'cohort[:\s]+(\d+)', r'enrollment[:\s]+(\d+)']:
        m = re.search(pattern, markdown, re.IGNORECASE)
        if m:
            extracted['classSize'] = int(m.group(1))
            break

    # Salary
    for pattern in [r'\$(\d{2,3},?\d{3})\s+average', r'average.*?\$(\d{2,3},?\d{3})', r'salary.*?\$(\d{2,3},?\d{3})']:
        m = re.search(pattern, markdown, re.IGNORECASE)
        if m:
            extracted['avgSalaryPost'] = int(m.group(1).replace(',', ''))
            break

    # Rankings
    for pattern in [r'U\.S\.? News[^#]*#?(\d+)', r'#?(\d+)\s+in.*?U\.S\.? News']:
        m = re.search(pattern, markdown, re.IGNORECASE)
        if m:
            extracted['usNewsRank'] = int(m.group(1))
            break

    for pattern in [r'Fortune[^#]*#?(\d+)', r'#?(\d+)\s+in.*?Fortune']:
        m = re.search(pattern, markdown, re.IGNORECASE)
        if m:
            extracted['fortuneRank'] = int(m.group(1))
            break

    return extracted

async def main():
    log("=" * 60)
    log("MBA ENRICHMENT - TARGETED (find-mba.com URLs only)")
    log("=" * 60)

    # Read CSV
    programs = []
    with open(INPUT_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        programs = list(reader)

    log(f"\n📊 Loaded {len(programs)} programs")

    # Find programs with find-mba.com URLs
    target_programs = []
    for prog in programs:
        urls = extract_findmba_urls(prog.get('description', ''))
        if urls:
            prog['_findmba_urls'] = urls
            target_programs.append(prog)

    log(f"  Programs with find-mba.com URLs: {len(target_programs)}")

    if not target_programs:
        log("⚠️ No programs with find-mba.com URLs found")
        return

    # Enrich
    enriched = []
    for i, prog in enumerate(target_programs, 1):
        name = prog.get('name', 'Unknown')
        log(f"\n[{i}/{len(target_programs)}] {name}")

        urls = prog.get('_findmba_urls', [])
        if not urls:
            continue

        # Scrape first URL
        url = urls[0]
        markdown = scrape_findmba(url)

        if markdown:
            # Extract fields
            extracted = extract_fields(markdown)

            if extracted:
                for key, val in extracted.items():
                    if val:
                        prog[key] = val

                log(f"  ✓ Extracted: {', '.join(extracted.keys())}")

        # Cleanup
        if '_findmba_urls' in prog:
            del prog['_findmba_urls']

        enriched.append(prog)
        await asyncio.sleep(1)

    # Save
    output_path = Path(OUTPUT_CSV)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        if enriched:
            writer = csv.DictWriter(f, fieldnames=enriched[0].keys())
            writer.writeheader()
            writer.writerows(enriched)

    log(f"\n✓ Saved to: {OUTPUT_CSV}")
    log(f"  Enriched: {len(enriched)} programs")

    # Stats
    fields_filled = {}
    for prog in enriched:
        for field in ['acceptanceRate', 'classSize', 'avgSalaryPost', 'usNewsRank', 'fortuneRank']:
            if prog.get(field):
                fields_filled[field] = fields_filled.get(field, 0) + 1

    log(f"\n📈 Fields filled:")
    for field, count in fields_filled.items():
        log(f"  {field}: {count}")

    log("\n" + "=" * 60)
    log("COMPLETE")
    log("=" * 60)

if __name__ == '__main__':
    asyncio.run(main())
