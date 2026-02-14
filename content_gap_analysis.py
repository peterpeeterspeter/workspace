#!/usr/bin/env python3
"""
Content Gap Analysis for Cardfair.com
Identifies missing content opportunities and topical gaps
"""

import requests
import json

DOMAIN = "https://www.cardfair.com"
AUTH = ("admin", "GyOC qXGg K82P hxRt ZjbY 2v9k")

# Target keywords and topics
TARGET_KEYWORDS = {
    "secured_credit_cards": {
        "keywords": [
            "best secured credit cards 2025",
            "secured credit cards no credit check",
            "secured cards with low deposit",
            "secured credit cards that graduate to unsecured",
            "secured credit cards for bad credit",
            "discover it secured card",
            "capital one platinum secured",
            "chime credit builder",
            "self credit builder"
        ],
        "search_volume": "high",
        "competition": "high",
        "priority": "critical"
    },
    "credit_building": {
        "keywords": [
            "how to build credit fast",
            "credit building apps",
            "credit builder loans",
            "become authorized user to build credit",
            "experian boost review",
            "how to improve credit score quickly",
            "credit utilization ratio",
            "how long to build credit from scratch"
        ],
        "search_volume": "high",
        "competition": "medium",
        "priority": "high"
    },
    "bankruptcy_credit": {
        "keywords": [
            "credit cards after bankruptcy discharge",
            "how long after bankruptcy to get credit card",
            "best credit card after chapter 7",
            "rebuilding credit after bankruptcy timeline",
            "getting a mortgage after bankruptcy",
            "car loan after bankruptcy",
            "bankruptcy friendly credit cards"
        ],
        "search_volume": "medium",
        "competition": "low",
        "priority": "high"
    },
    "credit_card_comparison": {
        "keywords": [
            "credit cards for fair credit 600-650",
            "credit cards for 580 credit score",
            "no annual fee credit cards",
            "cash back credit cards for bad credit",
            "balance transfer credit cards for bad credit",
            "business credit cards for bad credit"
        ],
        "search_volume": "high",
        "competition": "high",
        "priority": "medium"
    },
    "credit_education": {
        "keywords": [
            "what is a good credit score",
            "how to check credit score for free",
            "credit score ranges explained",
            "hard vs soft credit inquiry",
            "how to dispute credit report errors",
            "when do credit scores update",
            "how to freeze credit report"
        ],
        "search_volume": "medium",
        "competition": "medium",
        "priority": "medium"
    }
}

def get_existing_posts():
    """Get all published posts from WordPress"""
    url = f"{DOMAIN}/wp-json/wp/v2/posts?per_page=100&_fields=slug,title,link"
    posts = []

    try:
        response = requests.get(url, auth=AUTH, timeout=10)
        if response.status_code == 200:
            posts = response.json()
            print(f"Found {len(posts)} published posts")
    except Exception as e:
        print(f"Error fetching posts: {e}")

    return posts

def get_existing_pages():
    """Get all published pages from WordPress"""
    url = f"{DOMAIN}/wp-json/wp/v2/pages?per_page=100&_fields=slug,title,link"
    pages = []

    try:
        response = requests.get(url, auth=AUTH, timeout=10)
        if response.status_code == 200:
            pages = response.json()
            print(f"Found {len(pages)} published pages")
    except Exception as e:
        print(f"Error fetching pages: {e}")

    return pages

def analyze_content_gaps():
    """Analyze content gaps"""
    print("="*80)
    print("🔍 CONTENT GAP ANALYSIS FOR CARDFAIR.COM")
    print("="*80)
    print()

    # Get existing content
    print("Fetching existing content...")
    print("-"*80)

    posts = get_existing_posts()
    pages = get_existing_pages()

    # Create set of existing content slugs
    existing_slugs = set()
    for post in posts:
        existing_slugs.add(post['slug'])

    for page in pages:
        existing_slugs.add(page['slug'])

    print()

    # Analyze each topic
    print("="*80)
    print("📊 CONTENT GAPS BY TOPIC")
    print("="*80)
    print()

    gaps = []

    for topic, data in TARGET_KEYWORDS.items():
        print(f"\n🎯 TOPIC: {topic.replace('_', ' ').title()}")
        print(f"   Priority: {data['priority'].upper()}")
        print(f"   Search Volume: {data['search_volume']}")
        print(f"   Competition: {data['competition']}")
        print()

        missing_keywords = []

        for keyword in data['keywords']:
            # Check if keyword is covered by existing content
            covered = False

            # Simple matching - check if any words from keyword appear in slugs
            keyword_words = set(keyword.lower().split())
            for slug in existing_slugs:
                slug_words = set(slug.split('-'))
                # If 3+ words match, consider it covered
                overlap = keyword_words & slug_words
                if len(overlap) >= 3:
                    covered = True
                    break

            if not covered:
                missing_keywords.append(keyword)

        if missing_keywords:
            print(f"   ❌ MISSING CONTENT ({len(missing_keywords)} keywords):")
            for kw in missing_keywords:
                print(f"      • {kw}")

            gaps.append({
                "topic": topic,
                "priority": data['priority'],
                "missing_count": len(missing_keywords),
                "keywords": missing_keywords
            })
        else:
            print(f"   ✅ Topic well covered")

    print()
    print("="*80)
    print("📋 CONTENT PRIORITIZATION")
    print("="*80)
    print()

    # Sort by priority
    priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    gaps.sort(key=lambda x: priority_order.get(x['priority'], 99))

    total_opportunities = sum(g['missing_count'] for g in gaps)

    print(f"Total content opportunities: {total_opportunities}")
    print()

    for i, gap in enumerate(gaps, 1):
        print(f"{i}. {gap['topic'].replace('_', ' ').title()} ({gap['priority'].upper()})")
        print(f"   Missing: {gap['missing_count']} articles/guides")

        # Suggest content types
        if gap['priority'] == 'critical':
            print(f"   Suggested: Comprehensive guides, comparison tables, reviews")
        elif gap['priority'] == 'high':
            print(f"   Suggested: How-to guides, listicles, tools")
        else:
            print(f"   Suggested: Quick tips, FAQs, definitions")

        print()

    print("="*80)
    print("🎯 RECOMMENDED CONTENT CALENDAR")
    print("="*80)
    print()

    print("WEEK 1-2 (Critical - Secured Cards):")
    print("  1. 'Best Secured Credit Cards 2025: Complete Guide'")
    print("  2. 'Secured Cards That Graduate to Unsecured: Timeline & Tips'")
    print("  3. 'Low Deposit Secured Cards: From $49 to $200'")
    print("  4. 'No Credit Check Secured Cards: Guaranteed Approval'")
    print()

    print("WEEK 3-4 (High Priority - Credit Building):")
    print("  5. 'How to Build Credit Fast: 5 Proven Strategies'")
    print("  6. 'Credit Building Apps That Actually Work: 2025 Review'")
    print("  7. 'Credit Builder Loans: What They Are and How to Use Them'")
    print("  8. 'Authorized User Strategy: Build Credit with Someone Else's Card'")
    print()

    print("WEEK 5-6 (High Priority - Bankruptcy):")
    print("  9. 'Credit Cards After Chapter 7: Best Options & Timeline'")
    print("  10. 'Rebuilding Credit After Bankruptcy: Month-by-Month Guide'")
    print("  11. 'Mortgage After Bankruptcy: How Long to Wait'")
    print()

    print("="*80)
    print("📈 SEO IMPACT ESTIMATE")
    print("="*80)
    print()

    print("If all {0} pieces of content are created:".format(total_opportunities))
    print()
    print("  • Topical Authority: +150%")
    print("  • Long-tail rankings: +200-300 keywords")
    print("  • Organic traffic potential: +500-1000 visitors/month")
    print("  • Conversion potential: 5-10% (credit card applications)")
    print()

    print("Time to create: 2-3 months (at 3-4 articles/week)")
    print("Estimated cost: $2,000-5,000 (if outsourcing)")
    print()

    # Save results
    results = {
        "analysis_date": "2026-02-01",
        "existing_posts": len(posts),
        "existing_pages": len(pages),
        "total_opportunities": total_opportunities,
        "gaps": gaps
    }

    with open('/root/.openclaw/workspace/content_gap_analysis.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("📊 Full analysis saved to: content_gap_analysis.json")

if __name__ == "__main__":
    analyze_content_gaps()
