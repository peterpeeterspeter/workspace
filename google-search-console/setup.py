#!/usr/bin/env python3
"""
Google Search Console API Integration
Pulls SEO data: clicks, impressions, CTR, positions
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

try:
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from google.auth.transport.requests import Request
except ImportError:
    print("❌ Missing required packages:")
    print("   pip install google-api-python-client google-auth-oauthlib")
    exit(1)

# Sites to monitor
SITES = {
    "crashcasino": "https://crashcasino.io",
    "crashgame": "https://crashgamegambling.com",
    "freecrash": "https://freecrashgames.com",
    "cryptocrash": "https://cryptocrashgambling.com",
    "debadkamer": "https://debadkamer.com"
}

def get_credentials():
    """Get OAuth2 credentials from token.json"""
    token_file = Path('token.json')

    if not token_file.exists():
        print("❌ token.json not found")
        print("\n📋 Run authorization first:")
        print("   python get_auth_url.py")
        print("   python exchange_code.py <code>")
        return None

    try:
        # Load token from JSON
        with open(token_file, 'r') as f:
            token_data = json.load(f)

        creds = Credentials(
            token=token_data['access_token'],
            refresh_token=token_data.get('refresh_token'),
            token_uri='https://oauth2.googleapis.com/token',
            client_id='714859164602-6f535vo1en6f1qvfv01beiqig09ko1v5.apps.googleusercontent.com',
            client_secret='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',
            scopes=['https://www.googleapis.com/auth/webmasters.readonly']
        )

        # Refresh if expired
        if creds.expired:
            creds.refresh(Request())

        return creds

    except Exception as e:
        print(f"❌ Error loading credentials: {e}")
        return None

def get_analytics_data(service, site_url, days=7):
    """Pull search analytics data for a site"""
    end_date = datetime.now().date()
    start_date = (datetime.now() - timedelta(days=days)).date()

    try:
        request = {
            'startDate': start_date.isoformat(),
            'endDate': end_date.isoformat(),
            'dimensions': ['query', 'page', 'device', 'country'],
            'rowLimit': 10000
        }

        response = service.searchanalytics().query(
            siteUrl=site_url,
            body=request
        ).execute()

        if 'rows' in response:
            return response['rows']
        return []

    except HttpError as e:
        print(f"⚠️  API Error for {site_url}: {e}")
        return []

def main():
    """Main execution"""
    print("🔍 Google Search Console API Integration")
    print("=" * 50)

    creds = get_credentials()
    if not creds:
        print("\n❌ Cannot proceed without credentials")
        return

    # Build service
    try:
        service = build('searchconsole', 'v1', credentials=creds)
        print("✅ Connected to Google Search Console API")
    except Exception as e:
        print(f"❌ Failed to build service: {e}")
        return

    # Output directory
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)

    results = {}

    # Pull data for each site
    for site_name, site_url in SITES.items():
        print(f"\n📊 Pulling data for {site_name}...")
        print(f"   URL: {site_url}")

        try:
            site_results = {
                'url': site_url,
                'analytics': get_analytics_data(service, site_url, days=7),
                'timestamp': datetime.now().isoformat()
            }

            results[site_name] = site_results
            print(f"   ✓ Analytics: {len(site_results['analytics'])} rows")

        except Exception as e:
            print(f"   ❌ Error: {e}")
            results[site_name] = {'error': str(e)}

    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = output_dir / f"gsc_data_{timestamp}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n✅ Data saved to: {output_file}")

    # Generate summary
    summary_lines = []
    summary_lines.append("# Google Search Console Data Summary")
    summary_lines.append(f"\n**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    summary_lines.append(f"**Period:** Last 7 days\n")

    for site_name, data in results.items():
        if 'error' in data:
            summary_lines.append(f"## {site_name}\n❌ {data['error']}\n")
            continue

        analytics_count = len(data.get('analytics', []))
        summary_lines.append(f"## {site_name}\n")
        summary_lines.append(f"- **Analytics rows:** {analytics_count}\n")

        if analytics_count > 0:
            # Get top queries
            top_queries = sorted(
                data['analytics'],
                key=lambda x: x.get('impressions', 0),
                reverse=True
            )[:5]

            summary_lines.append("### Top Queries:\n")
            for row in top_queries:
                keys = row.get('keys', [])
                query = keys[0] if keys else 'N/A'
                clicks = row.get('clicks', 0)
                impressions = row.get('impressions', 0)
                ctr = row.get('ctr', 0)
                position = row.get('position', 0)

                summary_lines.append(
                    f"- **{query}**: {clicks} clicks, {impressions} impressions, "
                    f"{ctr:.1%} CTR, pos {position:.1f}"
                )
            summary_lines.append("")

    # Save summary
    summary_file = output_dir / f"summary_{timestamp}.md"
    with open(summary_file, 'w') as f:
        f.write('\n'.join(summary_lines))

    print(f"📋 Summary saved to: {summary_file}")

    # Generate CSV
    import csv
    csv_file = output_dir / f"top_keywords_{timestamp}.csv"

    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['site', 'query', 'page', 'clicks', 'impressions', 'ctr', 'position', 'device', 'country'])

        for site_name, data in results.items():
            if 'error' in data:
                continue

            for row in data.get('analytics', []):
                keys = row.get('keys', [])
                writer.writerow([
                    site_name,
                    keys[0] if len(keys) > 0 else '',
                    keys[1] if len(keys) > 1 else '',
                    row.get('clicks', 0),
                    row.get('impressions', 0),
                    f"{row.get('ctr', 0):.4f}",
                    f"{row.get('position', 0):.1f}",
                    keys[2] if len(keys) > 2 else '',
                    keys[3] if len(keys) > 3 else ''
                ])

    print(f"📊 CSV saved to: {csv_file}")

    # Print summary to console
    print("\n" + "=" * 50)
    print("📋 SUMMARY")
    print("=" * 50)

    for site_name, data in results.items():
        if 'error' in data:
            print(f"\n{site_name}: ❌ {data['error']}")
            continue

        analytics_count = len(data.get('analytics', []))

        # Calculate totals
        total_clicks = sum(r.get('clicks', 0) for r in data.get('analytics', []))
        total_impressions = sum(r.get('impressions', 0) for r in data.get('analytics', []))
        avg_ctr = sum(r.get('ctr', 0) for r in data.get('analytics', [])) / analytics_count if analytics_count > 0 else 0
        avg_position = sum(r.get('position', 0) for r in data.get('analytics', [])) / analytics_count if analytics_count > 0 else 0

        print(f"\n📊 {site_name} ({data['url']})")
        print(f"   Rows: {analytics_count}")
        print(f"   Clicks: {total_clicks}")
        print(f"   Impressions: {total_impressions}")
        print(f"   Avg CTR: {avg_ctr:.2%}")
        print(f"   Avg Position: {avg_position:.1f}")

if __name__ == '__main__':
    main()
