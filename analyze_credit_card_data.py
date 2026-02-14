#!/usr/bin/env python3
"""
Credit Card Comparison Tool Generator for WordPress
Creates a shortcode-based comparison tool from JSON data
"""

import json
import re

# Load the credit card data
with open('/root/.openclaw/media/inbound/file_0---1cf36a19-42d3-40ac-b404-b7ddc9c78914.json', 'r') as f:
    data = json.load(f)

credit_cards = data[0]['credit_cards']

print("="*80)
print("📊 CREDIT CARD DATA ANALYSIS")
print("="*80)
print()

# Analyze the data
print(f"Total credit cards: {len(credit_cards)}")
print()

# Count by issuer
issuers = {}
for card in credit_cards:
    issuer = card.get('issuer', 'Unknown')
    issuers[issuer] = issuers.get(issuer, 0) + 1

print("Top Issuers:")
print("-"*80)
for issuer, count in sorted(issuers.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"  {issuer}: {count} cards")

print()

# Count by annual fee
no_fee = [c for c in credit_cards if '$0' in c.get('annual_fee', '') or 'None' in c.get('annual_fee', '')]
print(f"Cards with $0 annual fee: {len(no_fee)}")

print()

# Secured cards
secured = [c for c in credit_cards if 'secured' in c.get('name', '').lower()]
print(f"Secured credit cards: {len(secured)}")

print()

# Student cards
student = [c for c in credit_cards if 'student' in c.get('name', '').lower()]
print(f"Student credit cards: {len(student)}")

print()

# Business cards
business = [c for c in credit_cards if 'business' in c.get('name', '').lower()]
print(f"Business credit cards: {len(business)}")

print()
print("="*80)
print("✅ Analysis Complete")
print("="*80)
