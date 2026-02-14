# PronosticiSerieB.com - Launch Checklist

## Pre-Launch (Before We Start)

### Environment Setup
- [ ] API-Football account created
- [ ] API-Football API key obtained
- [ ] Supabase account created
- [ ] Supabase project created
- [ ] Supabase URL + keys obtained
- [ ] Vercel account ready (optional, can sign up during deploy)

### Domain & DNS
- [ ] pronosticiserieb.com DNS accessible
- [ ] Can update DNS records
- [ ] DNS propagation time understood (usually 1-48 hours)

---

## Day 1: Setup (Jan 31)

### Task 1: API-Football Setup (Peter) - 5 min
- [ ] Sign up at https://www.api-football.com
- [ ] Verify email
- [ ] Get API key from dashboard
- [ ] Send API key to Carlottta

**Output:** API key string (starts with letters/numbers)

### Task 2: Test API (Carlottta) - 10 min
- [ ] Update api_football_client.py with API key
- [ ] Run: python3 api_football_client.py
- [ ] Verify Serie B standings returned
- [ ] Verify fixtures returned
- [ ] Note any rate limits or errors

**Output:** Successful API response

### Task 3: Supabase Setup (Peter) - 15 min
- [ ] Go to https://supabase.com
- [ ] Sign up/in (GitHub or email)
- [ ] Create organization
- [ ] Create project: "pronosticiserieb"
- [ ] Choose region: EU West
- [ ] Wait for provisioning (2-3 min)
- [ ] Get: Project URL, anon key, service_role key

**Output:** Three connection strings

### Task 4: Database Deploy (Peter/Carlottta) - 10 min
- [ ] Open Supabase SQL Editor
- [ ] Copy backend/supabase-schema.sql
- [ ] Paste into SQL Editor
- [ ] Run query (Ctrl+Enter)
- [ ] Verify in Table Editor:
  - [ ] teams table has 22 rows
  - [ ] matches table exists
  - [ ] predictions table exists
  - [ ] odds table exists
  - [ ] views created

**Output:** All tables present with sample data

### Task 5: Frontend Config (Carlottta) - 10 min
- [ ] Create frontend/.env.local
- [ ] Add NEXT_PUBLIC_SUPABASE_URL
- [ ] Add NEXT_PUBLIC_SUPABASE_ANON_KEY
- [ ] Run: cd frontend && npm install
- [ ] Run: npm run dev
- [ ] Open http://localhost:3000
- [ ] Verify page loads without errors

**Output:** Site running locally

### Task 6: Supabase Client Setup (Carlottta) - 15 min
- [ ] Create frontend/lib/supabase.ts
- [ ] Add createClient code
- [ ] Add helper functions:
  - [ ] getTodaysMatches()
  - [ ] getLeagueTable()
- [ ] Test in dev environment

**Output:** Can fetch data from Supabase

---

## Day 2: Deploy & Launch (Feb 1)

### Task 7: Real Data Integration (Carlottta) - 30 min
- [ ] Update home page to use getTodaysMatches()
- [ ] Update prediction display
- [ ] Add error handling
- [ ] Test with real data from Supabase

**Output:** Home page shows database data

### Task 8: Sync Script (Carlottta) - 20 min
- [ ] Create sync_supabase.py
- [ ] Implement standings sync
- [ ] Implement fixtures sync
- [ ] Test end-to-end
- [ ] Set up cron for hourly sync

**Output:** Automated data pipeline

### Task 9: Vercel Deploy (Peter) - 15 min
- [ ] Install Vercel CLI: npm i -g vercel
- [ ] cd frontend
- [ ] Run: vercel login
- [ ] Run: vercel
- [ ] Follow prompts
- [ ] Get deployment URL

**Output:** Site live on Vercel

### Task 10: Custom Domain (Peter) - 15 min
- [ ] Go to Vercel dashboard
- [ ] Settings → Domains → Add domain
- [ ] Add: pronosticiserieb.com
- [ ] Copy DNS records from Vercel
- [ ] Update DNS at domain registrar
- [ ] Wait for propagation

**Output:** Domain pointing to Vercel

### Task 11: SEO Content (Peter/Carlottta) - 30 min
- [ ] Choose CMS approach:
  - [ ] Static Next.js pages (fastest)
  - [ ] WordPress + API
  - [ ] Supabase CMS
- [ ] Generate/publish content-pages.json
- [ ] Create sitemap.xml
- [ ] Add robots.txt

**Output:** 30 content pages accessible

### Task 12: Analytics (Peter) - 10 min
- [ ] Set up Google Analytics 4
- [ ] Add tracking ID to site
- [ ] Test real-time data
- [ ] Set up Search Console
- [ ] Submit sitemap

**Output:** Analytics tracking

### Task 13: Pre-Launch Testing (Peter/Carlottta) - 20 min
- [ ] Test on mobile devices
- [ ] Test all pages load
- [ ] Check console for errors
- [ ] Test email capture (if set up)
- [ ] Verify predictions display
- [ ] Check responsive design

**Output:** Site production-ready

### Task 14: Launch! (Peter) - 5 min
- [ ] DNS verified (green check in Vercel)
- [ ] Final smoke test
- [ ] Announce (optional)
- [ ] Submit sitemap to Google

**Output:** 🚀 SITE LIVE!

---

## Post-Launch (Week 1)

### Day 3-7: Monitoring & Optimization
- [ ] Check analytics daily
- [ ] Monitor for errors
- [ ] Verify data syncing
- [ ] Check SEO indexing
- [ ] Gather feedback
- [ ] Plan improvements

---

## Critical Variables (Save These!)

```
API-Football Key: __________________________________

Supabase URL: ______________________________________

Supabase Anon Key: _________________________________

Supabase Service Key: _______________________________

Vercel URL: _________________________________________

GA4 Tracking ID: ____________________________________
```

---

## Troubleshooting

**API-Football errors:**
- Check key is correct
- Verify not rate limited
- Check Serie B league ID (135)

**Supabase connection errors:**
- Verify URL format
- Check anon key permissions
- Ensure RLS policies allow public read

**Vercel deploy errors:**
- Check .env.local variables
- Verify build logs
- Ensure package.json scripts correct

**DNS not propagating:**
- Wait 24-48 hours
- Check DNS records match Vercel
- Verify registrar settings

---

## Quick Commands

```bash
# Test API
cd ~/workspace/pronosticiserieb/data-pipelines
python3 api_football_client.py

# Run frontend locally
cd ~/workspace/pronosticiserieb/frontend
npm run dev

# Deploy to Vercel
cd ~/workspace/pronosticiserieb/frontend
vercel

# Sync data
cd ~/workspace/pronosticiserieb/data-pipelines
python3 sync_supabase.py
```

---

*Check off each task as we go! ✅*
