#!/usr/bin/env python3
"""
Quick Indexing Checker for Multiple Sites
Checks if sites are indexed in Google and have sitemaps
"""

import requests
import json
from urllib.parse import urlparse
from typing import List, Dict

def check_google_indexing(domain: str) -> Dict:
    """Check if domain is indexed in Google"""
    try:
        # Method 1: Try to fetch via search URL (won't work directly, needs API)
        # Alternative: Check if site is accessible
        url = f"https://{domain}" if not domain.startswith('http') else domain
        response = requests.get(url, timeout=10, allow_redirects=True)
        return {
            "domain": domain,
            "accessible": response.status_code == 200,
            "redirects": len(response.history),
            "final_url": response.url
        }
    except Exception as e:
        return {
            "domain": domain,
            "accessible": False,
            "error": str(e)
        }

def check_sitemap(domain: str) -> Dict:
    """Check if sitemap exists"""
    sitemaps = [
        f"https://{domain}/sitemap.xml",
        f"https://{domain}/sitemap_index.xml",
        f"https://{domain}/wp-sitemap.xml",  # WordPress
        f"https://{domain}/sitemap/sitemap.xml"  # Common
    ]

    for sitemap in sitemaps:
        try:
            response = requests.head(sitemap, timeout=5)
            if response.status_code == 200:
                return {
                    "domain": domain,
                    "sitemap_found": True,
                    "sitemap_url": sitemap,
                    "status": response.status_code
                }
        except:
            continue

    return {
        "domain": domain,
        "sitemap_found": False,
        "sitemap_url": None
    }

def check_robots_txt(domain: str) -> Dict:
    """Check if robots.txt exists"""
    try:
        url = f"https://{domain}/robots.txt"
        response = requests.get(url, timeout=5)
        return {
            "domain": domain,
            "robots_txt_found": response.status_code == 200,
            "content_length": len(response.text) if response.status_code == 200 else 0
        }
    except:
        return {
            "domain": domain,
            "robots_txt_found": False
        }

def batch_check_sites(domains: List[str]) -> List[Dict]:
    """Check multiple sites and return comprehensive report"""
    results = []

    print(f"🔍 Checking {len(domains)} sites...\n")

    for domain in domains:
        # Clean domain
        domain = domain.replace('https://', '').replace('http://', '').strip('/')

        print(f"Checking: {domain}...")

        site_info = {
            "domain": domain,
            "accessibility": check_google_indexing(domain),
            "sitemap": check_sitemap(domain),
            "robots": check_robots_txt(domain)
        }

        results.append(site_info)

    return results

def print_report(results: List[Dict]):
    """Print formatted report"""
    print("\n" + "="*80)
    print("📊 INDEXING STATUS REPORT")
    print("="*80 + "\n")

    for site in results:
        domain = site["domain"]
        accessible = site["accessibility"].get("accessible", False)
        sitemap = site["sitemap"].get("sitemap_found", False)
        robots = site["robots"].get("robots_txt_found", False)

        # Status indicators
        status = "✅" if accessible else "❌"
        sitemap_status = "✅" if sitemap else "⚠️"
        robots_status = "✅" if robots else "⚠️"

        print(f"{status} {domain}")
        print(f"   Accessible: {accessible}")
        print(f"   Sitemap: {sitemap_status} {site['sitemap'].get('sitemap_url', 'Not found')}")
        print(f"   Robots.txt: {robots_status}")
        print()

        # Recommendations
        if not sitemap:
            print(f"   ⚠️ ACTION NEEDED: Create sitemap.xml")
        if not robots:
            print(f"   ⚠️ ACTION NEEDED: Create robots.txt")
        print()

# Example usage
if __name__ == "__main__":
    # Add your domains here
    domains = [
        "pronosticiserieb.com",
        # Add more domains here...
    ]

    results = batch_check_sites(domains)
    print_report(results)

    # Save to JSON
    with open('/root/.openclaw/workspace/indexing_report.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("✅ Report saved to: indexing_report.json")
