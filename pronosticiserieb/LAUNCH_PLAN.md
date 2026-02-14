# 🚀 PronosticiSerieB.com - 2-Day Launch Plan

## Day 1: Setup & Integration (Today)

### ✅ Already Done
- [x] Prediction engine built and tested
- [x] Database schema ready
- [x] Frontend structure created
- [x] SEO content generated (30 pages)
- [x] API research completed

---

### 📋 Day 1 Tasks (Jan 31)

#### Task 1: Sign Up for API-Football (5 min) - **PETER**
```
1. Go to: https://www.api-football.com
2. Click "Get Started" or "Sign Up"
3. Create free account
4. Get API key from dashboard
5. Send API key to Carlottta
```

**Output:** API key for testing

---

#### Task 2: Test API Access (10 min) - **CARLOTTA**
```bash
cd ~/workspace/pronosticiserieb/data-pipelines

# Edit with API key
nano api_football_client.py
# Replace: your-api-football-key-here

# Test
python3 api_football_client.py
```

**Expected output:**
- ✅ Serie B standings
- ✅ Today's fixtures

**If fails:** Debug or try alternative API

---

#### Task 3: Set Up Supabase (15 min) - **PETER**
```
1. Go to: https://supabase.com
2. Click "Start your project"
3. Sign in with GitHub (or email)
4. Create new organization
5. Create new project:
   - Name: pronosticiserieb
   - Region: EU West (closer to Italy)
   - Wait 2-3 minutes for provisioning
```

**Output:** Supabase project URL + anon key

---

#### Task 4: Deploy Database Schema (10 min) - **CARLOTTA/PETER**
```
1. Go to Supabase project
2. Click "SQL Editor" in left sidebar
3. Click "New Query"
4. Paste contents of: backend/supabase-schema.sql
5. Click "Run" or press Ctrl+Enter
6. Verify tables created (check Table Editor)
```

**Expected:**
- ✅ Tables: teams, matches, predictions, odds, etc.
- ✅ 22 teams pre-loaded
- ✅ Views created

---

#### Task 5: Create Sync Script (30 min) - **CARLOTTA**

**Create:** `data-pipelines/sync_supabase.py`
```python
#!/usr/bin/env python3
"""
Sync Serie B data from API-Football to Supabase
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from prediction_engine.predictor import SerieBPredictor, Team, Match

try:
    from supabase import create_client
except ImportError:
    print("❌ Installing supabase-python...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "supabase"])
    from supabase import create_client


def main():
    """Sync data from API-Football to Supabase."""

    # Environment variables
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
    api_football_key = os.getenv("API_FOOTBALL_KEY")

    if not all([supabase_url, supabase_key, api_football_key]):
        print("❌ Missing environment variables")
        print("Required: SUPABASE_URL, SUPABASE_SERVICE_KEY, API_FOOTBALL_KEY")
        sys.exit(1)

    # Initialize clients
    print("🔌 Connecting to Supabase...")
    supabase = create_client(supabase_url, supabase_key)

    print("🔌 Connecting to API-Football...")
    # Import here to avoid import errors
    sys.path.insert(0, str(project_root / "data-pipelines"))
    from api_football_client import APIFootballClient
    api_client = APIFootballClient(api_football_key)

    # Step 1: Sync standings
    print("\n📊 Fetching Serie B standings...")
    standings_data = api_client.get_standings()

    if "error" in standings_data:
        print(f"❌ API Error: {standings_data['error']}")
        sys.exit(1)

    print("✅ Got standings data")
    # TODO: Parse and upsert teams to Supabase
    # This is a placeholder - needs full implementation

    # Step 2: Sync fixtures
    print("\n📅 Fetching upcoming fixtures...")
    today = datetime.now().strftime("%Y-%m-%d")
    next_week = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

    fixtures_data = api_client.get_fixtures(from_date=today, to_date=next_week)

    if "error" in fixtures_data:
        print(f"❌ API Error: {fixtures_data['error']}")
        sys.exit(1)

    print("✅ Got fixtures data")
    # TODO: Parse and insert matches to Supabase

    print("\n✅ Sync complete!")
    print("\n⚠️  Note: Full parsing logic needs to be implemented")
    print("This syncs raw data - you'll need to map API fields to DB schema")


if __name__ == "__main__":
    main()
```

**Test:**
```bash
cd ~/workspace/pronosticiserieb/data-pipelines
chmod +x sync_supabase.py
export SUPABASE_URL=your-url
export SUPABASE_SERVICE_KEY=your-key
export API_FOOTBALL_KEY=your-key
python3 sync_supabase.py
```

---

#### Task 6: Configure Frontend (10 min) - **PETER/CARLOTTA**
```bash
cd ~/workspace/pronosticiserieb/frontend

# Create .env.local
cat > .env.local << EOF
NEXT_PUBLIC_SUPABASE_URL=your-supabase-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key
EOF

# Install dependencies
npm install

# Test locally
npm run dev
```

**Expected:**
- ✅ Site runs on http://localhost:3000
- ✅ No errors in console

---

### 🌙 End of Day 1 Goals
- [x] API-Football account created
- [x] API tested successfully
- [x] Supabase project set up
- [x] Database schema deployed
- [x] Sync script created
- [x] Frontend configured locally

---

## Day 2: Deploy & Launch (Feb 1)

### 📋 Day 2 Tasks

#### Task 7: Connect Frontend to Supabase (1 hour) - **CARLOTTA**

**Create:** `frontend/lib/supabase.ts`
```typescript
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient(supabaseUrl, supabaseKey)

// Helper functions
export async function getTodaysMatches() {
  const today = new Date().toISOString().split('T')[0]

  const { data, error } = await supabase
    .from('matches')
    .select('*, home_team(*), away_team(*), predictions(*)')
    .gte('match_date', today)
    .order('match_date')
    .limit(10)

  if (error) throw error
  return data
}

export async function getLeagueTable() {
  const { data, error } = await supabase
    .from('teams')
    .select('*')
    .order('points', { ascending: false })

  if (error) throw error
  return data
}
```

**Update:** `frontend/app/page.tsx` to use real data
```typescript
import { getTodaysMatches } from '@/lib/supabase'

export default async function HomePage() {
  const matches = await getTodaysMatches()

  return (
    // Use matches.data instead of mock
  )
}
```

---

#### Task 8: Deploy to Vercel (15 min) - **PETER**
```bash
cd ~/workspace/pronosticiserieb/frontend

# Install Vercel CLI
npm i -g vercel

# Login (if not already)
vercel login

# Deploy
vercel

# Answer prompts:
# - Link to existing project? No
# - Project name: pronosticiserieb
# - Directory: ./
# - Override settings? No
```

**Expected output:**
- ✅ Deployment URL: https://pronosticiserieb.vercel.app
- ✅ Production URL: https://pronosticiserieb.com (after domain setup)

---

#### Task 9: Set Custom Domain (10 min) - **PETER**
```
1. Go to Vercel project dashboard
2. Click "Settings" → "Domains"
3. Add: pronosticiserieb.com
4. Update DNS at registrar (Namecheap, GoDaddy, etc.)
5. Wait for DNS propagation (usually fast)
```

---

#### Task 10: Publish SEO Content (30 min) - **CARLOTTA/PETER**

**Option A: Supabase CMS**
```bash
cd ~/workspace/pronosticiserieb/data-pipelines

# Import content to Supabase
python3 import_content.py
```

**Option B: WordPress + Supabase**
1. Set up WordPress on hosting
2. Use Supabase for data
3. Use WordPress for content/blog

**Option C: Static Pages (Fastest)**
- Add content routes to Next.js
- Pre-generate pages at build time

**Recommendation:** Start with Option C for launch, add WordPress later for content management

---

#### Task 11: Set Up Monitoring (15 min) - **PETER**

**Add analytics:**
```bash
# Sign up for GA4
# Add tracking ID to Next.js
```

**Set up uptime monitoring:**
- UptimeRobot (free)
- Or Pingdom

---

#### Task 12: Final Testing (30 min) - **PETER/CARLOTTA**

**Checklist:**
- [ ] Homepage loads
- [ ] Matches display correctly
- [ ] Predictions show
- [ ] Mobile responsive
- [ ] No console errors
- [ ] SEO meta tags present
- [ ] SSL certificate working
- [ ] DNS propagated

---

#### Task 13: Launch! (5 min) - **PETER**

**Announce:**
- Post on social media (if desired)
- Submit to Google Search Console
- Add sitemap to robots.txt

---

## 🎯 Success Criteria

**Day 1:**
- ✅ API-Football working
- ✅ Supabase database live
- ✅ Frontend running locally

**Day 2:**
- ✅ Site deployed to production
- ✅ Real data showing
- ✅ SEO content published
- ✅ Analytics installed

**Week 1:**
- ✅ Indexed by Google
- ✅ First organic traffic
- ✅ Email capture working

---

## 📞 Quick Reference

**API-Football:** https://www.api-football.com
**Supabase:** https://supabase.com
**Vercel:** https://vercel.com

**Files:**
- API client: `data-pipelines/api_football_client.py`
- DB schema: `backend/supabase-schema.sql`
- Frontend: `frontend/`
- Prediction: `prediction-engine/predictor.py`

---

## 💰 Post-Launch (Week 2-4)

**Week 2:**
- Add Odds-API.io when key arrives
- Create social profiles
- Start building backlinks

**Week 3-4:**
- Optimize SEO
- A/B test email capture
- Add more content pages
- Monitor analytics

---

*Let's launch this! 🚀*
