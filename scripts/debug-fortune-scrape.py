#!/usr/bin/env python3
"""
Debug Fortune scraping to see what we're getting
"""

import os
from firecrawl import FirecrawlApp
from dotenv import load_dotenv

load_dotenv('/root/.openclaw/workspace/.env')

api_key = os.getenv('FIRECRAWL_API_KEY')
app = FirecrawlApp(api_key=api_key)

url = 'https://fortune.com/ranking/best-mba-programs/'

print(f"Scraping: {url}")
result = app.scrape(url, formats=['markdown'], only_main_content=True)

if result and hasattr(result, 'markdown') and result.markdown:
    print("\n" + "=" * 80)
    print("MARKDOWN OUTPUT (first 2000 chars):")
    print("=" * 80)
    print(result.markdown[:2000])
    print("\n" + "=" * 80)
    print("MARKDOWN OUTPUT (last 2000 chars):")
    print("=" * 80)
    print(result.markdown[-2000:])
else:
    print("No markdown returned")
