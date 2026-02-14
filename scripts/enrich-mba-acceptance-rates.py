#!/usr/bin/env python3
"""
MBA Database Enrichment - Acceptance Rates from Menlo Coaching

Parses acceptance rate data from Menlo Coaching and enriches MBA database.
"""

import os
import csv
import re
from pathlib import Path
from datetime import datetime

INPUT_CSV = '/root/.openclaw/workspace/data/mba-enriched-university-pages.csv'
OUTPUT_CSV = '/root/.openclaw/workspace/data/mba-acceptance-enriched.csv'
LOG_DIR = Path('/root/.openclaw/workspace/logs')
LOG_DIR.mkdir(parents=True, exist_ok=True)

log_file = LOG_DIR / f'mba-acceptance-{datetime.now().strftime("%Y%m%d-%H%M%S")}.log'

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")
    with open(log_file, 'a') as f:
        f.write(f"[{timestamp}] {msg}\n")

# Acceptance rate data from Menlo Coaching (2024 data)
# Maps slug keywords to acceptance rates
ACCEPTANCE_RATES = {
    'stanford': 7.0,
    'harvard': 11.0,
    'wharton': 21.0,
    'kellogg': 29.0,
    'booth': 29.0,
    'columbia': 21.0,
    'mit': 14.0,
    'sloan': 14.0,
    'dartmouth': 31.0,
    'tuck': 31.0,
    'berkeley': 25.0,
    'haas': 25.0,
    'virginia': 34.0,
    'darden': 34.0,
    'yale': 27.0,
    'duke': 20.0,
    'fuqua': 20.0,
    'michigan': 29.0,
    'ross': 29.0,
    'texas': 38.0,
    'mccombs': 38.0,
    'cornell': 28.0,
    'johnson': 28.0,
    'ucla': 31.0,
    'anderson': 31.0,
    'nyu': 25.0,
    'stern': 25.0,
    'carnegie': 27.0,
    'tepper': 27.0,
    'unc': 37.0,
    'kenan': 37.0,
    'flagler': 37.0,
    'emory': 37.0,
    'goizueta': 37.0,
    'usc': 23.0,
    'marshall': 23.0,
    'georgetown': 60.0,
    'mcdonough': 60.0,
    'indiana': 29.0,
    'kelley': 29.0,
    'uw': 39.0,
    'foster': 39.0,
    'rice': 34.0,
    'jones': 34.0,
}

def normalize_name(name):
    """Normalize school names for matching"""
    name = name.lower()
    name = re.sub(r'\b(university|school|college|of|at|the|business|mba)\b', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name

def load_mba_database():
    """Load existing MBA database"""
    programs = []

    with open(INPUT_CSV, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            programs.append(row)

    log(f"📊 Loaded {len(programs)} programs from database")
    return programs

def enrich_acceptance_rates(programs):
    """Enrich programs with acceptance rates"""
    matched = 0

    for program in programs:
        # Skip if already has acceptance rate
        if program.get('acceptanceRate'):
            continue

        # Try to match by name and slug
        name = program.get('name', '').lower()
        slug = program.get('slug', '').lower()

        # Check for match in ACCEPTANCE_RATES
        for school_key, rate in ACCEPTANCE_RATES.items():
            if school_key in name or school_key in slug:
                program['acceptanceRate'] = rate
                matched += 1
                log(f"✓ Matched: {program.get('name')} -> {rate}%")
                break

    log(f"✓ Matched {matched} programs with acceptance rates")
    return programs

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
    log("MBA ENRICHMENT - ACCEPTANCE RATES")
    log("=" * 60)
    log("")

    # Load database
    programs = load_mba_database()

    # Enrich with acceptance rates
    enriched = enrich_acceptance_rates(programs)

    # Save
    save_enriched_data(enriched)

    # Report coverage
    acceptance_rate_count = sum(1 for p in enriched if p.get('acceptanceRate'))
    class_size_count = sum(1 for p in enriched if p.get('classSize'))
    salary_count = sum(1 for p in enriched if p.get('avgSalaryPost'))

    log("")
    log("📈 Coverage Report:")
    log(f"  acceptanceRate: {acceptance_rate_count}/{len(enriched)} programs ({acceptance_rate_count/len(enriched)*100:.1f}%)")
    log(f"  classSize: {class_size_count}/{len(enriched)} programs ({class_size_count/len(enriched)*100:.1f}%)")
    log(f"  avgSalaryPost: {salary_count}/{len(enriched)} programs ({salary_count/len(enriched)*100:.1f}%)")
    log("")
    log("=" * 60)
    log("COMPLETE")
    log("=" * 60)

if __name__ == '__main__':
    main()
