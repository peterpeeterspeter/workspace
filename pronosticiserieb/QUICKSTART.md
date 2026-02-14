# Quick Start Guide - Pronosticiserieb.com

## Option A: Deploy Now (No API Key)

### 1. Set Up Supabase (Free)

```bash
# Go to https://supabase.com
# Create new project
# Get: Project URL + anon key

# In Supabase SQL Editor, paste:
cat backend/supabase-schema.sql
# Run it
```

### 2. Configure Frontend

```bash
cd frontend
npm install

# Create .env.local
cp .env.example .env.local
# Edit: Add your Supabase URL + key

# Test locally
npm run dev
# Open http://localhost:3000
```

### 3. Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd frontend
vercel
```

### 4. Generate Content

```bash
cd ../data-pipelines
python3 content-generator.py
# Import content-pages.json to Supabase/WordPress
```

---

## Option B: Test with Odds API (When You Have Key)

```bash
# Set API key
export ODDS_API_KEY=your_key

# Test Serie B access
cd ../skills_backup/odds-checker-api
python3 scripts/odds_api.py sports

# Search Serie B events
python3 scripts/odds_api.py search --query "Serie B" --sport football
```

---

## Option C: Hybrid (Launch Now, Add API Later)

1. Deploy with mock data (today)
2. Add SEO content (this week)
3. Integrate live odds (when key ready)

---

## Database Connection (Supabase)

```typescript
// frontend/lib/supabase.ts
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient(supabaseUrl, supabaseKey)

// Fetch today's matches
const { data: matches } = await supabase
  .from('matches')
  .select('*, home_team(*), away_team(*), predictions(*)')
  .gte('match_date', new Date().toISOString())
  .order('match_date')
```

---

## Testing Prediction Model

```bash
cd prediction-engine
python3 predictor.py

# Output:
# Match: Brescia vs Palermo
# Probabilities: Home 52%, Draw 28%, Away 20%
# Recommended: HOME (65% confidence)
# Value Bet: ✅ Yes
```

---

## Monetization Setup

### Affiliate Links (Italian Bookmakers)

```html
<!-- Example: BetFlag affiliate link -->
<a href="https://betflag.it/aff/your-ref-code">
  Quota Brescia @ 2.10 su BetFlag
</a>

<!-- Other partners: -->
<!-- Snai: https://snai.it/aff/your-ref-code -->
<!-- Sisal: https://sisal.it/aff/your-ref-code -->
<!-- 888Sport IT: https://888sport.it/aff/your-ref-code -->
```

### Email Capture (Mailchimp / ConvertKit)

```html
<!-- Add to frontend/components/EmailSignup.tsx -->
<form onSubmit={handleSubmit}>
  <input type="email" placeholder="La tua email" />
  <button>Iscriviti Gratis</button>
</form>
```

---

## SEO Checklist

- [x] Generate 30 content pages
- [ ] Add meta tags to Next.js
- [ ] Create sitemap.xml
- [ ] Submit to Google Search Console
- [ ] Build backlinks (Italian betting forums)
- [ ] Optimize for Core Web Vitals

---

## Deploy Checklist

- [x] Supabase schema ready
- [x] Next.js frontend structure
- [x] Prediction model working
- [x] SEO content generated
- [ ] Set up Vercel project
- [ ] Configure domain (pronosticiserieb.com)
- [ ] Test live deployment
- [ ] Set up analytics (GA4)
- [ ] Add affiliate links

---

## Expected Timeline

**Week 1:**
- Supabase setup ✅
- Frontend deployment
- Content publishing

**Week 2-4:**
- SEO optimization
- Content indexing
- Start seeing organic traffic

**Month 2:**
- Add odds integration (if key ready)
- Launch VIP newsletter
- First affiliate commissions

**Month 3+:**
- Optimize prediction model
- Scale content production
- Build email list

---

## Questions?

Ask Carlottta about:
- Supabase setup issues
- Frontend deployment
- Content strategy
- Monetization optimization
