#!/usr/bin/env python3
"""Analyze MBA data and create summary"""

import csv
from collections import Counter

input_file = '/root/.openclaw/workspace/research/onlinembaprograms-comprehensive.csv'

programs = []

with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    programs = list(reader)

print("=" * 80)
print("MBA PROGRAM DATA ANALYSIS")
print("=" * 80)
print(f"\nTotal Programs: {len(programs)}\n")

# By tier
tiers = Counter(p.get('tier', 'Unknown') for p in programs)
print("BY TIER:")
for tier, count in sorted(tiers.items(), key=lambda x: x[1], reverse=True):
    print(f"  {tier}: {count}")
print()

# By accreditation
accreditations = Counter(p.get('accreditation', 'Unknown') for p in programs)
print("BY ACCREDITATION:")
for acc, count in sorted(accreditations.items(), key=lambda x: x[1], reverse=True):
    print(f"  {acc}: {count}")
print()

# Confidence scores
high_conf = [p for p in programs if float(p.get('confidence_score', 0)) >= 80]
med_conf = [p for p in programs if 50 <= float(p.get('confidence_score', 0)) < 80]
low_conf = [p for p in programs if 0 < float(p.get('confidence_score', 0)) < 50]
no_conf = [p for p in programs if float(p.get('confidence_score', 0)) == 0]

print("BY CONFIDENCE SCORE:")
print(f"  80-100% (High Quality): {len(high_conf)}")
print(f"  50-79% (Medium Quality): {len(med_conf)}")
print(f"  1-49% (Low Quality): {len(low_conf)}")
print(f"  0% (Failed/No Data): {len(no_conf)}")
print()

# Data completeness
print("DATA COMPLETENESS:")
fields_to_check = ['tuition_total', 'tuition_per_credit', 'format', 'duration',
                   'total_credits', 'gmat_requirement', 'gre_accepted']
for field in fields_to_check:
    filled = sum(1 for p in programs if p.get(field) and p.get(field).strip())
    pct = round(filled / len(programs) * 100, 1)
    print(f"  {field}: {filled}/{len(programs)} ({pct}%)")
print()

# Top programs by confidence
print("=" * 80)
print("TOP 15 PROGRAMS BY CONFIDENCE SCORE")
print("=" * 80)
top_programs = sorted(programs, key=lambda x: float(x.get('confidence_score', 0)), reverse=True)[:15]
for i, p in enumerate(top_programs, 1):
    print(f"\n{i}. {p['school_name']} - {p['program_name']}")
    print(f"   Tier: {p.get('tier', 'N/A')}")
    print(f"   Accreditation: {p.get('accreditation', 'N/A')}")
    print(f"   Format: {p.get('format', 'N/A')}")
    print(f"   Duration: {p.get('duration', 'N/A')}")
    print(f"   Tuition: {p.get('tuition_total', 'N/A')}")
    print(f"   GMAT: {p.get('gmat_requirement', 'N/A')}")
    print(f"   GRE: {p.get('gre_accepted', 'N/A')}")
    print(f"   Confidence: {p.get('confidence_score', '0')}%")
    print(f"   URL: {p.get('program_url', 'N/A')}")

print("\n" + "=" * 80)
print("PROGRAMS WITH TUITION DATA")
print("=" * 80)
tuition_programs = [p for p in programs if p.get('tuition_total') and p.get('tuition_total').strip()]
for p in tuition_programs[:20]:
    print(f"{p['school_name']}: {p['tuition_total']} - {p.get('tuition_per_credit', 'N/A')}")

print("\n" + "=" * 80)
print(f"AFFILIATE-FRIENDLY SUMMARY")
print("=" * 80)
print(f"Total programs for affiliate site: {len(programs)}")
print(f"Programs with tuition data: {len(tuition_programs)}")
print(f"Programs with high confidence (80%+): {len(high_conf)}")
print(f"Programs with tier information: {sum(1 for p in programs if p.get('tier'))}")
print(f"International programs: {sum(1 for p in programs if p.get('tier') == 'International')}")
print(f"Affordable programs: {sum(1 for p in programs if p.get('tier') == 'Affordable')}")
print(f"Top Tier programs: {sum(1 for p in programs if p.get('tier') == 'Top Tier')}")
