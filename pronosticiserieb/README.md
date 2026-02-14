# Pronosticiserieb.com - Serie B Prediction Platform

## Project Overview
Italian Serie B football prediction platform with AI-powered picks, live odds, and betting insights.

## Tech Stack
- **Frontend:** Next.js 14, TypeScript, Tailwind CSS, shadcn/ui
- **Backend:** Supabase (PostgreSQL, Auth, Storage, Edge Functions)
- **AI:** OpenAI API (predictions, content generation)
- **Data APIs:** Odds-API.io (odds), Firecrawl (scraping), TheSportsDB (team data)
- **Hosting:** Vercel (frontend), Supabase (backend)

## Project Structure
```
pronosticiserieb/
├── frontend/           # Next.js app
│   ├── app/           # App router pages
│   ├── components/    # Reusable UI components
│   ├── lib/           # Utilities, API clients
│   └── public/        # Static assets
├── backend/           # Supabase edge functions
├── prediction-engine/ # ML/prediction models
├── data-pipelines/    # Scrapers, data processors
└── docs/              # Documentation
```

## Core Features

### Phase 1: MVP (Launch in 2 weeks)
- [x] Project structure
- [ ] Prediction model (rule-based)
- [ ] Supabase setup
- [ ] Basic frontend (matches, predictions, table)
- [ ] SEO content pages

### Phase 2: Live Data
- [ ] Odds-API integration
- [ ] Real-time odds display
- [ ] Live match tracking
- [ ] Email alerts

### Phase 3: Monetization
- [ ] Affiliate links (Italian bookmakers)
- [ ] VIP subscription tier
- [ ] Premium picks with higher accuracy

## Prediction Model

### Input Features
- Team form (last 5 games)
- Home/away advantage
- Head-to-head record
- Goal difference
- League position
- Injuries/suspensions (when available)

### Output
- Win/Draw/Loss probabilities
- Confidence score (0-100)
- Recommended bet (Yes/No)
- Value assessment

## Development

### Setup
```bash
# Install dependencies
cd frontend && npm install

# Configure environment
cp .env.example .env.local
# Add: SUPABASE_URL, SUPABASE_ANON_KEY, OPENAI_API_KEY

# Run dev server
npm run dev
```

### Database Schema
```sql
-- Teams
CREATE TABLE teams (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  thesportsdb_id INTEGER,
  league TEXT DEFAULT 'Serie B',
  created_at TIMESTAMP DEFAULT NOW()
);

-- Matches
CREATE TABLE matches (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  home_team_id UUID REFERENCES teams(id),
  away_team_id UUID REFERENCES teams(id),
  match_date TIMESTAMP NOT NULL,
  status TEXT DEFAULT 'scheduled', -- scheduled, live, finished
  home_score INTEGER,
  away_score INTEGER,
  season TEXT DEFAULT '2024-2025',
  created_at TIMESTAMP DEFAULT NOW()
);

-- Predictions
CREATE TABLE predictions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  match_id UUID REFERENCES matches(id),
  home_win_prob DECIMAL(5,2),
  draw_prob DECIMAL(5,2),
  away_win_prob DECIMAL(5,2),
  confidence INTEGER,
  recommended_outcome TEXT, -- home, draw, away
  value_bet BOOLEAN,
  model_version TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Odds (when API available)
CREATE TABLE odds (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  match_id UUID REFERENCES matches(id),
  bookmaker TEXT NOT NULL,
  home_win_odds DECIMAL(10,2),
  draw_odds DECIMAL(10,2),
  away_win_odds DECIMAL(10,2),
  last_updated TIMESTAMP DEFAULT NOW()
);
```

## SEO Strategy

### Target Keywords (Italian)
- "pronostici serie b oggi"
- "scommesse serie b"
- "pronostici calcio serie b"
- "schedine serie b"
- "consigli scommesse serie b"

### Content Pages
1. **Daily predictions** - "Pronostici Serie B [Data]"
2. **Team guides** - All 22 Serie B teams
3. **Betting guides** - How to bet on Serie B
4. **Strategy articles** - Bankroll management, value betting

## Monetization

### Affiliate Partners
- Snai
- Sisal
- BetFlag
- 888Sport IT
- Lottomatica

### Revenue Model
1. **Affiliate CPA** - €50-150 per depositing player
2. **VIP Subscription** - €29-99/month for premium picks
3. **Display Ads** - Once traffic hits 10k+/mo

## Next Steps

1. ✅ Create project structure
2. ⏳ Set up Supabase project
3. ⏳ Build prediction model
4. ⏳ Create frontend components
5. ⏳ Generate SEO content
6. ⏳ Get Odds-API key
7. ⏳ Launch MVP

## Contributors
- Peter Peeters - Product, SEO
- Carlottta (AI) - Development, automation
