#!/usr/bin/env python3
"""
MBA Database Enrichment - Salary Data from Coursera/US News

Adds average starting salary data (with bonuses) from US News ranking data.
"""

import os
import csv
import re
from pathlib import Path
from datetime import datetime

INPUT_CSV = '/root/.openclaw/workspace/data/mba-rankings-enriched.csv'
OUTPUT_CSV = '/root/.openclaw/workspace/data/mba-final-enriched.csv'
LOG_DIR = Path('/root/.openclaw/workspace/logs')
LOG_DIR.mkdir(parents=True, exist_ok=True)

log_file = LOG_DIR / f'mba-salary-{datetime.now().strftime("%Y%m%d-%H%M%S")}.log'

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")
    with open(log_file, 'a') as f:
        f.write(f"[{timestamp}] {msg}\n")

# US News 2024 MBA Salary Data (Average starting salary + bonuses)
# Source: Coursera article citing US News
SALARY_DATA = {
    'stanford': 221471,
    'pennsylvania': 213129,
    'wharton': 213129,
    'chicago': 212211,
    'booth': 212211,
    'harvard': 210125,
    'mit': 205270,
    'sloan': 205270,
    'dartmouth': 204090,
    'tuck': 204090,
    'nyu': 203176,
    'stern': 203176,
    'columbia': 202234,
    'northwestern': 202225,
    'kellogg': 202225,
    'cornell': 200405,
    'johnson': 200405,
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

def enrich_salaries(programs):
    """Enrich programs with salary data"""
    matched = 0

    for program in programs:
        # Skip if already has salary
        if program.get('avgSalaryPost'):
            continue

        slug = program.get('slug', '')
        normalized = normalize_name(slug)

        # Check for match in SALARY_DATA
        for school_key, salary in SALARY_DATA.items():
            if school_key in normalized:
                program['avgSalaryPost'] = salary
                matched += 1
                log(f"✓ Matched: {program.get('name')} -> ${salary:,}")
                break

    log(f"✓ Matched {matched} programs with salary data")
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
    log("MBA ENRICHMENT - SALARY DATA")
    log("=" * 60)
    log("")

    # Load database
    programs = load_mba_database()

    # Enrich with salaries
    enriched = enrich_salaries(programs)

    # Save
    save_enriched_data(enriched)

    # Report coverage
    acceptance_rate_count = sum(1 for p in enriched if p.get('acceptanceRate'))
    class_size_count = sum(1 for p in enriched if p.get('classSize'))
    salary_count = sum(1 for p in enriched if p.get('avgSalaryPost'))
    fortune_rank_count = sum(1 for p in enriched if p.get('fortuneRank'))
    usnews_rank_count = sum(1 for p in enriched if p.get('usNewsRank'))

    log("")
    log("📈 Final Coverage Report:")
    log(f"  acceptanceRate: {acceptance_rate_count}/{len(enriched)} ({acceptance_rate_count/len(enriched)*100:.1f}%)")
    log(f"  classSize: {class_size_count}/{len(enriched)} ({class_size_count/len(enriched)*100:.1f}%)")
    log(f"  avgSalaryPost: {salary_count}/{len(enriched)} ({salary_count/len(enriched)*100:.1f}%)")
    log(f"  fortuneRank (PQ): {fortune_rank_count}/{len(enriched)} ({fortune_rank_count/len(enriched)*100:.1f}%)")
    log(f"  usNewsRank: {usnews_rank_count}/{len(enriched)} ({usnews_rank_count/len(enriched)*100:.1f}%)")
    log("")
    log("=" * 60)
    log("COMPLETE")
    log("=" * 60)

if __name__ == '__main__':
    main()
