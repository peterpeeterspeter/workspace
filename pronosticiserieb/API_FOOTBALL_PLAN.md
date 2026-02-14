# Updated Implementation Plan with API-Football

## 🎯 New Recommendation: Use API-Football First

Based on research, **API-Football is the best starting point**:

### Why API-Football?

✅ **Has Serie B** (verified in coverage list)
✅ **Free tier available** (no credit card needed)
✅ **Built-in Predictions API** (upgrade tier)
✅ **Built-in Odds API** (upgrade tier)
✅ **H2H statistics** (upgrade tier)
✅ **Fixtures & standings** (free tier)

---

## 📊 Updated Stack

### Phase 1: Launch with API-Football Free Tier

```python
# What you get for FREE:
- Serie B fixtures (upcoming matches)
- Serie B standings (league table)
- Basic team information
- ~100 requests/day (verify exact limit)

# What you can build:
✅ Today's predictions page
✅ League table display
✅ Team pages with basic stats
✅ SEO content (30 pages ready)
```

### Phase 2: Upgrade to Paid (When You Have Traffic)

```python
# Paid tier adds:
- H2H statistics (improve predictions)
- Odds data (bookmaker quotes)
- Predictions API (their AI vs yours)
- More requests per day
- Historical data
```

---

## 🚀 Updated Launch Plan

### Step 1: Sign Up for API-Football (5 minutes)

```
1. Go to: https://www.api-football.com
2. Click "Get Started" or "Sign Up"
3. Create free account
4. Get API key from dashboard
5. No credit card required for free tier
```

### Step 2: Test API Access (5 minutes)

```bash
cd ~/workspace/pronosticiserieb/data-pipelines

# Edit the script with your API key
nano api_football_client.py
# Replace: your-api-football-key-here

# Run test
python3 api_football_client.py

# Should see:
# ✅ Serie B standings
# ✅ Today's fixtures
```

### Step 3: Integrate with Prediction Engine (30 minutes)

**Update predictor.py to use real data:**

```python
# Before: Mock data
brescia = Team(name="Brescia", ...)

# After: Real data from API
api_client = APIFootballClient(api_key)
standings = api_client.get_standings()
fixtures = api_client.get_fixtures()

# Parse and feed into prediction model
```

### Step 4: Deploy to Supabase + Vercel (1 hour)

**Same as before, now with live data:**

1. Set up Supabase (database)
2. Create sync job (API-Football → Supabase)
3. Deploy frontend to Vercel
4. Test live site

---

## 💰 Cost Comparison

| API | Free Tier | Paid Tier | When to Pay |
|-----|-----------|-----------|-------------|
| **API-Football** | ~100 req/day | $TBD | When you hit limit |
| **Odds-API.io** | 500 req total | $9-99/mo | If you want odds now |
| **Football-Data.org** | Top leagues only | $TBD | Serie B likely paid |

**Recommendation:** Start with API-Football free, upgrade when needed.

---

## 🔧 Technical Implementation

### API-Football → Supabase Sync Script

```python
# data-pipelines/sync_api_football.py

import os
from datetime import datetime
from api_football_client import APIFootballClient
from supabase import create_client

# Initialize clients
api_key = os.getenv("API_FOOTBALL_KEY")
api_client = APIFootballClient(api_key)

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
supabase = create_client(supabase_url, supabase_key)

def sync_standings():
    """Sync Serie B standings to Supabase."""

    # Fetch from API
    data = api_client.get_standings()

    # Parse teams
    teams = []
    for team_data in data["response"][0]["league"]["standings"][0]:
        teams.append({
            "name": team_data["team"]["name"],
            "league_position": team_data["rank"],
            "points": team_data["points"],
            "played": team_data["all"]["played"],
            "won": team_data["all"]["win"],
            "drawn": team_data["all"]["draw"],
            "lost": team_data["all"]["lose"],
            "goals_for": team_data["all"]["goals"]["for"],
            "goals_against": team_data["all"]["goals"]["against"]
        })

    # Upsert to Supabase
    for team in teams:
        supabase.table("teams").upsert(team).execute()

    print(f"✅ Synced {len(teams)} teams")

def sync_fixtures():
    """Sync upcoming fixtures to Supabase."""

    # Next 7 days
    from_date = datetime.now().strftime("%Y-%m-%d")
    to_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

    # Fetch from API
    data = api_client.get_fixtures(from_date=from_date, to_date=to_date)

    # Parse fixtures
    fixtures = []
    for match in data["response"]:
        fixtures.append({
            "home_team": match["teams"]["home"]["name"],
            "away_team": match["teams"]["away"]["name"],
            "match_date": match["fixture"]["date"],
            "status": "scheduled"
        })

    # Insert to Supabase
    for fixture in fixtures:
        supabase.table("matches").insert(fixture).execute()

    print(f"✅ Synced {len(fixtures)} fixtures")

if __name__ == "__main__":
    sync_standings()
    sync_fixtures()
```

### Cron Job (Hourly Sync)

```bash
# Add to crontab
0 * * * * cd ~/workspace/pronosticiserieb/data-pipelines && python3 sync_api_football.py
```

---

## 📋 Updated Checklist

- [ ] Sign up for API-Football
- [ ] Get API key
- [ ] Test with `api_football_client.py`
- [ ] Update `predictor.py` to use real data
- [ ] Create sync script for Supabase
- [ ] Set up cron job (hourly sync)
- [ ] Deploy frontend to Vercel
- [ ] Test live data on site
- [ ] Publish SEO content

---

## 🎯 Summary: What Changed

**Before (without API):**
- ❌ Mock data only
- ❌ No live fixtures
- ❌ Manual updates

**After (with API-Football Free):**
- ✅ Real Serie B fixtures
- ✅ Live standings
- ✅ Automatic updates
- ✅ Ready to launch

---

## 🚀 Ready to Launch?

**Yes!** With API-Football free tier, you can:

1. **Today:** Sign up and get API key
2. **Tomorrow:** Test integration
3. **In 2 days:** Launch with live data
4. **When growing:** Upgrade to paid for odds/H2H

---

*Updated: 31 Jan 2025 - API-Football research complete*
