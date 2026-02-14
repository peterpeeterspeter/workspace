#!/usr/bin/env python3
"""
MBA Database Enrichment - Class Size Data from Poets&Quants

Adds class size data from M7 schools (2025 class profiles).
"""

import os
import csv
import re
from pathlib import Path
from datetime import datetime

INPUT_CSV = '/root/.openclaw/workspace/data/mba-final-enriched.csv'
OUTPUT_CSV = '/root/.openclaw/workspace/data/mba-enriched-final.csv'
LOG_DIR = Path('/root/.openclaw/workspace/logs')
LOG_DIR.mkdir(parents=True, exist_ok=True)

log_file = LOG_DIR / f'mba-classsize-{datetime.now().strftime("%Y%m%d-%H%M%S")}.log'

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")
    with open(log_file, 'a') as f:
        f.write(f"[{timestamp}] {msg}\n")

# M7 Class Size Data 2025 (Poets&Quants article)
CLASS_SIZE_DATA = {
    'columbia': 982,
    'harvard': 943,
    'wharton': 888,
    'pennsylvania': 888,
    'chicago': 635,
    'booth': 635,
    'mit': 450,
    'sloan': 450,
    'northwestern': 520,
    'kellogg': 520,
    'stanford': 420,
}

def normalize_name(slug):
    """Normalize school slug for matching"""
    slug = slug.lower()
    slug = slug.replace('-', ' ')
    slug = re.sub(r'\b(university|school|college|of|at|the|business|mba|online|master|administration)\b', '', slug)
    slug = re.sub(r'\s+', ' ', slug).strip()
    return slug

def load_mba_database():
    """Load existing MBA database"""
    programs = []

    with open(INPUT_CSV, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            programs.append(row)

    log(f"📊 Loaded {len(programs)} programs from database")
    return programs

def enrich_class_sizes(programs):
    """Enrich programs with class size data"""
    matched = 0

    for program in programs:
        # Skip if already has class size
        if program.get('classSize'):
            continue

        slug = program.get('slug', '')
        normalized = normalize_name(slug)

        # Check for match in CLASS_SIZE_DATA
        for school_key, size in CLASS_SIZE_DATA.items():
            if school_key in normalized:
                program['classSize'] = size
                matched += 1
                log(f"✓ Matched: {program.get('name')} -> {size} students")
                break

    log(f"✓ Matched {matched} programs with class size data")
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
    log("MBA ENRICHMENT - CLASS SIZE DATA")
    log("=" * 60)
    log("")

    # Load database
    programs = load_mba_database()

    # Enrich with class sizes
    enriched = enrich_class_sizes(programs)

    # Save
    save_enriched_data(enriched)

    # Report final coverage
    acceptance_rate_count = sum(1 for p in enriched if p.get('acceptanceRate'))
    class_size_count = sum(1 for p in enriched if p.get('classSize'))
    salary_count = sum(1 for p in enriched if p.get('avgSalaryPost'))
    fortune_rank_count = sum(1 for p in enriched if p.get('fortuneRank'))
    usnews_rank_count = sum(1 for p in enriched if p.get('usNewsRank'))

    log("")
    log("📈 FINAL ENRICHMENT COVERAGE:")
    log("=" * 60)
    log(f"  acceptanceRate:  {acceptance_rate_count:2d}/30 ({acceptance_rate_count/30*100:.0f}%)")
    log(f"  classSize:       {class_size_count:2d}/30 ({class_size_count/30*100:.0f}%)")
    log(f"  avgSalaryPost:   {salary_count:2d}/30 ({salary_count/30*100:.0f}%)")
    log(f"  fortuneRank (PQ):{fortune_rank_count:2d}/30 ({fortune_rank_count/30*100:.0f}%)")
    log(f"  usNewsRank:      {usnews_rank_count:2d}/30 ({usnews_rank_count/30*100:.0f}%)")
    log("=" * 60)
    log("")
    log("✅ MBA DATABASE ENRICHMENT COMPLETE")
    log("📁 Final file: /root/.openclaw/workspace/data/mba-enriched-final.csv")
    log("")

if __name__ == '__main__':
    main()
