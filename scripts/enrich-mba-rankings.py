#!/usr/bin/env python3
"""
MBA Database Enrichment - Poets&Quants Rankings

Parses Poets&Quants 2025-2026 ranking data to populate usNewsRank and overall ranking.
"""

import os
import csv
import re
from pathlib import Path
from datetime import datetime

INPUT_CSV = '/root/.openclaw/workspace/data/mba-acceptance-enriched.csv'
OUTPUT_CSV = '/root/.openclaw/workspace/data/mba-rankings-enriched.csv'
LOG_DIR = Path('/root/.openclaw/workspace/logs')
LOG_DIR.mkdir(parents=True, exist_ok=True)

log_file = LOG_DIR / f'mba-rankings-{datetime.now().strftime("%Y%m%d-%H%M%S")}.log'

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")
    with open(log_file, 'a') as f:
        f.write(f"[{timestamp}] {msg}\n")

# Poets&Quants 2025-2026 Rankings (Top 25)
# Format: School keywords -> (PQ_Rank, US_News_Rank)
POETS_QUANTS_RANKINGS = {
    'kellogg': (1, 2),
    'harvard': (2, 6),
    'columbia': (3, 9),
    'dartmouth': (4, 6),
    'tuck': (4, 6),
    'virginia': (5, 11),
    'darden': (5, 11),
    'nyu': (6, 6),
    'stern': (6, 6),
    'cornell': (7, 15),
    'johnson': (7, 15),
    'pennsylvania': (8, 1),
    'wharton': (8, 1),
    'michigan': (9, 13),
    'ross': (9, 13),
    'ucla': (10, 18),
    'anderson': (10, 18),
    'mit': (11, 5),
    'sloan': (11, 5),
    'chicago': (12, 4),
    'booth': (12, 4),
    'texas': (13, 16),
    'mccombs': (13, 16),
    'berkeley': (14, 11),
    'haas': (14, 11),
    'duke': (15, 13),
    'fuqua': (15, 13),
    'carnegie': (16, 18),
    'tepper': (16, 18),
    'yale': (17, 10),
    'som': (17, 10),
    'vanderbilt': (18, 18),
    'owen': (18, 18),
    'washington': (19, 24),
    'olin': (19, 24),
    'georgia': (20, 21),
    'scheller': (20, 21),
    'north carolina': (21, 28),
    'kenan': (21, 28),
    'flagler': (21, 28),
    'emory': (22, 17),
    'goizueta': (22, 17),
    'uw': (23, 22),
    'foster': (23, 22),
    'southern california': (24, 24),
    'usc': (24, 24),
    'marshall': (24, 24),
    'georgetown': (25, 24),
    'mcdonough': (25, 24),
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

def enrich_rankings(programs):
    """Enrich programs with rankings"""
    pq_matched = 0
    usnews_matched = 0

    for program in programs:
        slug = program.get('slug', '')
        normalized = normalize_name(slug)

        # Check for match in POETS_QUANTS_RANKINGS
        for school_key, (pq_rank, usnews_rank) in POETS_QUANTS_RANKINGS.items():
            if school_key in normalized:
                if not program.get('fortuneRank'):
                    program['fortuneRank'] = pq_rank
                    pq_matched += 1
                if not program.get('usNewsRank'):
                    program['usNewsRank'] = usnews_rank
                    usnews_matched += 1
                log(f"✓ Matched: {program.get('name')} -> PQ#{pq_rank}, US News#{usnews_rank}")
                break

    log(f"✓ Matched {pq_matched} programs with Poets&Quants rankings")
    log(f"✓ Matched {usnews_matched} programs with US News rankings")
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
    log("MBA ENRICHMENT - POETS&QUANTS RANKINGS")
    log("=" * 60)
    log("")

    # Load database
    programs = load_mba_database()

    # Enrich with rankings
    enriched = enrich_rankings(programs)

    # Save
    save_enriched_data(enriched)

    # Report coverage
    acceptance_rate_count = sum(1 for p in enriched if p.get('acceptanceRate'))
    class_size_count = sum(1 for p in enriched if p.get('classSize'))
    salary_count = sum(1 for p in enriched if p.get('avgSalaryPost'))
    fortune_rank_count = sum(1 for p in enriched if p.get('fortuneRank'))
    usnews_rank_count = sum(1 for p in enriched if p.get('usNewsRank'))

    log("")
    log("📈 Coverage Report:")
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
