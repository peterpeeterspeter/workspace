# Google Search Console API Integration

Pull SEO data (clicks, impressions, CTR, positions, index coverage) from Google Search Console for all your sites.

## Sites Monitored

- crashcasino.io
- crashgamegambling.com
- freecrashgames.com
- cryptocrashgambling.com
- debadkamer.com

## Setup (One-Time)

### 1. Create Google Cloud Project

1. Go to: https://console.cloud.google.com/
2. Create new project (or use existing)
3. Enable Search Console API:
   - Go to "APIs & Services" > "Library"
   - Search for "Search Console API"
   - Click "Enable"

### 2. Create OAuth 2.0 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Application type: **Web application**
4. Name: "OpenClaw GSC Integration"
5. Authorized redirect URIs: `http://localhost:8080`
6. Click "Create"
7. Download JSON (save as `credentials.json` in this directory)

### 3. Authorize Access

1. Run the authorization script:
   ```bash
   python authorize.py
   ```
2. Open browser to authorize the app
3. Copy authorization code and paste in terminal
4. Credentials saved automatically

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Pull All Data (Last 7 Days)

```bash
python setup.py
```

This will:
- Connect to GSC API
- Pull analytics data for all sites
- Get index coverage stats
- Save to `output/gsc_data_TIMESTAMP.json`

### Pull Specific Site

```bash
python quick_pull.py crashcasino  # Last 30 days
python quick_pull.py debadkamer 14  # Last 14 days
```

### Generate Summary Report

```bash
python generate_report.py
```

Creates:
- `output/summary.md` - Human-readable report
- `output/top_keywords.csv` - Top performing keywords
- `output/coverage_stats.csv` - Index coverage by site

## Output Structure

```
google-search-console/
├── credentials.json          # OAuth credentials (NOT in git)
├── token.json                # Refresh token (auto-generated)
├── output/
│   ├── gsc_data_20260211_085000.json
│   ├── summary.md
│   ├── top_keywords.csv
│   └── coverage_stats.csv
└── logs/
    └── pull_20260211.log
```

## Data Pulled

### Search Analytics
- Queries (keywords people search for)
- Pages (URLs getting impressions)
- Device breakdown (desktop/mobile/tablet)
- Country breakdown
- Impressions, clicks, CTR, position

### Index Coverage
- Total pages submitted
- Pages indexed
- Pages with errors
- Coverage issues

## Automation

### Cron Job (Daily Pull)

Add to crontab:
```bash
0 8 * * * cd /root/.openclaw/workspace/google-search-console && python setup.py
```

### Integration with Vision Agent

Vision agent can use this data for:
- Keyword research (validate search volume)
- Content performance tracking
- SEO opportunity identification
- Competitor analysis

## Troubleshooting

### "credentials.json not found"
- Run authorization flow first
- Save credentials.json in project root

### "API not enabled"
- Enable Search Console API in GCP console
- Wait 5-10 minutes for changes to propagate

### "Site not verified"
- Add sites in Google Search Console first
- Use domain property or URL prefix property
- Verify ownership (DNS, HTML file, etc.)

### "Quota exceeded"
- Free tier: 5 queries per second (QPS)
- Daily limit: 1,200 queries per day
- Add exponential backoff if needed

## Security

- **NEVER** commit credentials.json to git
- Add to .gitignore
- Use service account for production (instead of OAuth)
- Restrict API key to GSC only

## Next Steps

1. ✅ Complete setup and authorization
2. ✅ Pull initial data for all sites
3. ✅ Generate summary report
4. ⏭️ Integrate with Vision agent for automated SEO monitoring
5. ⏭️ Set up daily cron job
6. ⏭️ Create alerts for ranking drops

## Support

- GSC API Docs: https://developers.google.com/webmaster-tools/
- OAuth Guide: https://developers.google.com/identity/protocols/oauth2
- Python Client: https://github.com/googleapis/python-api-core
