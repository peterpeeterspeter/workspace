#!/usr/bin/env python3
"""
Audit published articles for affiliate links and metadata issues
"""

import json
import subprocess
import re

# Peter's CORRECT affiliate links
CORRECT_AFFILIATES = {
    'cybet': 'https://cybetplay.com/tluy6cbpp',
    'bitstarz': 'https://bzstarz1.com/b196c322b',
    'betzrd': 'https://betzrd.com/pyondmfcx',
    '7bit': 'https://7bit.partners/p4i4w1udu',
    '7bit casino': 'https://7bit.partners/p4i4w1udu',
    'mirax': 'https://mirax.partners/p4fp2iusj',
    'mirax casino': 'https://mirax.partners/p4fp2iusj',
    'trustdice': 'https://trustdice.win/?ref=u_peterp',
    '1xpartners': 'https://reffpa.com/L?tag=d_4381452m_97c_&site=4381452&ad=97',
    '1xbet': 'https://reffpa.com/L?tag=d_4381452m_97c_&site=4381452&ad=97',
    'betfury': 'https://betfury.bet/df1865703'
}

# Sites to check
SITES = {
    'crashcasino': {
        'url': 'https://crashcasino.io/wp-json',
        'user': 'peter',
        'pass': '3vRhtTs2khfdLtTiDFqkdeXI'
    },
    'crashgamegambling': {
        'url': 'https://crashgamegambling.com/wp-json',
        'user': '@peter',
        'pass': 'MioX SygN Xaz6 pK9o RUiK tBMF'
    },
    'freecrashgames': {
        'url': 'https://freecrashgames.com/wp-json',
        'user': '@peter',
        'pass': 'F8Mg yZXM qJy4 jQvp BMeZ FoMG'
    },
    'cryptocrash': {
        'url': 'https://cryptocrashgambling.com/wp-json',
        'user': '@peter',
        'pass': 'R3kQ 6vRA UwYd x7Cn KEtT Pk83'
    }
}

def get_recent_posts(site_key, limit=50):
    """Get recent posts from a site"""
    site = SITES[site_key]
    curl_cmd = [
        'curl', '-s',
        '-u', f"{site['user']}:{site['pass']}",
        f"{site['url']}/wp/v2/posts?per_page={limit}&orderby=date&order=desc&_fields=id,title,link,date,content"
    ]

    try:
        result = subprocess.run(curl_cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except Exception as e:
        print(f"Error fetching posts from {site_key}: {e}")
        return []

def check_affiliate_links(content):
    """Check if content has wrong affiliate links"""
    issues = []

    # Check for wrong affiliate domains
    wrong_domains = [
        'stake.com',
        'bc.game',
        'thunderpick.com',
        'roobet.com',
        'metaspins.com',
        'cnd',
        'bitstarz.com',  # Should be bzstarz1.com
        '7bitcasino.com'  # Should be 7bit.partners
    ]

    for domain in wrong_domains:
        if domain in content.lower():
            issues.append(f"Contains wrong affiliate domain: {domain}")

    # Check for CORRECT affiliate links
    has_correct_links = any(url in content for url in CORRECT_AFFILIATES.values())

    return issues, has_correct_links

def check_metadata_issue(content):
    """Check if metadata is showing as text in content"""
    issues = []

    # Check for raw metadata markers in content
    metadata_patterns = [
        r'Meta Description',
        r'Article Schema',
        r'FAQPage Schema',
        r'Bottom Line',
        r'@context',
        r'@type',
        r'datePublished'
    ]

    for pattern in metadata_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            issues.append(f"Metadata visible in content: {pattern}")

    return issues

def audit_site(site_key):
    """Audit all recent posts on a site"""
    print(f"\n{'='*70}")
    print(f"AUDITING: {site_key}")
    print(f"{'='*70}\n")

    posts = get_recent_posts(site_key, limit=100)

    if not posts:
        print("No posts found")
        return

    print(f"Found {len(posts)} posts\n")

    problems = []

    for post in posts:
        post_id = post['id']
        title = post['title']['rendered']
        content = post.get('content', {}).get('rendered', '')

        affiliate_issues, has_correct = check_affiliate_links(content)
        metadata_issues = check_metadata_issue(content)

        if affiliate_issues or metadata_issues or not has_correct:
            problems.append({
                'id': post_id,
                'title': title,
                'link': post['link'],
                'affiliate_issues': affiliate_issues,
                'metadata_issues': metadata_issues,
                'has_correct_affiliates': has_correct
            })

            print(f"❌ Post {post_id}: {title}")
            print(f"   URL: {post['link']}")

            if affiliate_issues:
                print(f"   Affiliate issues:")
                for issue in affiliate_issues:
                    print(f"     • {issue}")

            if not has_correct:
                print(f"   ⚠️  Missing YOUR affiliate links")

            if metadata_issues:
                print(f"   Metadata issues:")
                for issue in metadata_issues:
                    print(f"     • {issue}")

            print()

    if not problems:
        print("✅ No issues found in recent posts")
    else:
        print(f"\n{'='*70}")
        print(f"SUMMARY: {len(problems)} posts with issues")
        print(f"{'='*70}")

    return problems

# Main audit
print("🔍 AFFILIATE LINK & METADATA AUDIT")
print("="*70)
print("Checking for:")
print("  • Wrong affiliate domains (Stake, BC.Game, etc.)")
print("  • Missing YOUR affiliate links")
print("  • Metadata showing as text in articles")
print("="*70)

total_problems = {}

for site_key in SITES:
    problems = audit_site(site_key)
    if problems:
        total_problems[site_key] = problems

print(f"\n{'='*70}")
print("OVERALL SUMMARY")
print(f"{'='*70}")

for site_key, problems in total_problems.items():
    print(f"\n{site_key}: {len(problems)} posts need fixing")

print(f"\n{'='*70}")
print("NEXT STEP: Create bulk fix script")
print(f"{'='*70}")
