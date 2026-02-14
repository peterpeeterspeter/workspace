# Google Search Console API Integration

**Status:** 🔧 SETUP REQUIRED

**Location:** `/root/.openclaw/workspace/google-search-console/`

## What This Does

Pulls SEO data directly from Google Search Console for all your sites:
- Search analytics (clicks, impressions, CTR, position)
- Top queries and pages
- Device and country breakdowns
- Index coverage stats

## Sites Configured

1. crashcasino.io
2. crashgamegambling.com
3. freecrashgames.com
4. cryptocrashgambling.com
5. debadkamer.com
6. + any other sites you have in GSC

## Setup Steps

### Step 1: Install Dependencies

```bash
cd /root/.openclaw/workspace/google-search-console
pip install -r requirements.txt
```

### Step 2: Create Google Cloud Project (One-Time)

1. Go to: https://console.cloud.google.com/
2. Create new project (or use existing)
3. Enable Search Console API:
   - APIs & Services > Library
   - Search for "Search Console API"
   - Click "Enable"

### Step 3: Create OAuth Credentials

1. Go to: APIs & Services > Credentials
2. Click "Create Credentials" > "OAuth client ID"
3. Application type: **Web application**
4. Name: "OpenClaw GSC Integration"
5. Authorized redirect URIs: `http://localhost:8080`
6. Click "Create"
7. Download JSON (save as `credentials.json` in this directory)

### Step 4: Authorize Application

```bash
python authorize.py
```

This will:
1. Open browser
2. Ask you to sign in to Google
3. Request permission to access Search Console
4. Save token automatically

### Step 5: Pull Data

```bash
python setup.py
```

This pulls the last 7 days of data for all configured sites.

## What You Get

**Output files in `output/` directory:**
- `gsc_data_TIMESTAMP.json` - Raw data dump
- `summary.md` - Human-readable summary
- `top_keywords.csv` - Best performing keywords
- `coverage_stats.csv` - Index coverage by site

## Example Output

```json
{
  "crashcasino": {
    "url": "https://crashcasino.io",
    "analytics": [
      {
        "keys": ["crash gambling", "/crash-gambling-guide", "desktop", "USA"],
        "clicks": 142,
        "impressions": 3841,
        "ctr": 0.037,
        "position": 12.4
      }
    ],
    "coverage": {
      "total": 856,
      "indexed": 792,
      "errors": 12
    }
  }
}
```

## Integration with Vision Agent

Vision agent can use this data for:
- ✅ Validate keyword research with real search volume
- ✅ Track content performance over time
- ✅ Identify low-hanging fruit (high impressions, low clicks)
- ✅ Find technical SEO issues (coverage errors)
- ✅ Monitor ranking changes

## Automation

**Daily data pull (cron):**
```bash
# Add to crontab: crontab -e
0 8 * * * cd /root/.openclaw/workspace/google-search-console && python setup.py
```

## Troubleshooting

**"credentials.json not found"**
- Run Step 3 first to get OAuth credentials

**"API not enabled"**
- Enable Search Console API in Google Cloud Console
- Wait 5-10 minutes for propagation

**"Site not found"**
- Sites must be added in Google Search Console first
- Verify ownership (DNS, HTML tag, or GA)

**"Authorization failed"**
- Check that credentials.json is valid JSON
- Verify redirect URI includes http://localhost:8080
- Ensure OAuth consent screen is configured

## Next Actions

1. ✅ Complete Steps 1-4 above
2. ✅ Run first data pull
3. ✅ Review output files
4. ⏭️ Set up daily cron job
5. ⏭️ Integrate with Vision agent for automated SEO monitoring

## Files

- `authorize.py` - OAuth authorization flow
- `setup.py` - Main data pull script
- `requirements.txt` - Python dependencies
- `README.md` - Detailed documentation
- `.gitignore` - Protects credentials

## Security Notes

- `credentials.json` and `token.json` are NOT in git
- Never commit these files
- Tokens refresh automatically
- Read-only access (no write permissions)

---

**Ready to set up?** Start with Step 1 above.
