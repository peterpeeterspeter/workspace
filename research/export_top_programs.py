#!/usr/bin/env python3
"""Export top MBA programs for immediate affiliate use"""

import csv

input_file = '/root/.openclaw/workspace/research/onlinembaprograms-comprehensive.csv'
output_file = '/root/.openclaw/workspace/research/TOP_PROGRAMS_FOR_AFFILIATE.csv'

programs = []

with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    programs = list(reader)

# Filter for high confidence programs
top_programs = [p for p in programs if float(p.get('confidence_score', 0)) >= 80]

# Sort by confidence
top_programs.sort(key=lambda x: float(x.get('confidence_score', 0)), reverse=True)

# Write to CSV
fieldnames = [
    'school_name', 'program_name', 'tuition_total', 'tuition_per_credit',
    'format', 'duration', 'total_credits', 'gmat_requirement', 'gre_accepted',
    'accreditation', 'tier', 'program_url', 'confidence_score'
]

with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(top_programs)

print(f"✓ Exported {len(top_programs)} high-confidence programs")
print(f"  Output: {output_file}")
print(f"\nReady for affiliate site integration!")
