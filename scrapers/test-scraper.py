#!/usr/bin/env python3
"""
Test scraper for badkamer-meubelsets
"""
import sys
import os

# Add workspace to path
sys.path.insert(0, '/root/.openclaw/workspace')

# Import the scraper
import scrapers.sawiday_badkamer_meubelsets

# Run scraper
scraper = scrapers.sawiday_badkamer_meubelsets.SawidayMeubelsetsScraper(headless=True)
scraper.run()
