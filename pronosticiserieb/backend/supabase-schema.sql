-- Serie B Prediction Platform - Supabase Schema
-- Run this in Supabase SQL Editor

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Teams table
CREATE TABLE teams (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  slug TEXT UNIQUE,
  thesportsdb_id INTEGER,
  badge_url TEXT,
  league TEXT DEFAULT 'Serie B',
  league_position INTEGER,
  points INTEGER DEFAULT 0,
  played INTEGER DEFAULT 0,
  won INTEGER DEFAULT 0,
  drawn INTEGER DEFAULT 0,
  lost INTEGER DEFAULT 0,
  goals_for INTEGER DEFAULT 0,
  goals_against INTEGER DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index on team name
CREATE INDEX idx_teams_name ON teams(name);
CREATE INDEX idx_teams_slug ON teams(slug);

-- Matches table
CREATE TABLE matches (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  home_team_id UUID REFERENCES teams(id) ON DELETE CASCADE,
  away_team_id UUID REFERENCES teams(id) ON DELETE CASCADE,
  match_date TIMESTAMP WITH TIME ZONE NOT NULL,
  status TEXT DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'live', 'finished', 'postponed')),
  home_score INTEGER,
  away_score INTEGER,
  season TEXT DEFAULT '2024-2025',
  round INTEGER,
  week INTEGER,
  venue TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(home_team_id, away_team_id, match_date)
);

-- Create indexes for matches
CREATE INDEX idx_matches_date ON matches(match_date);
CREATE INDEX idx_matches_status ON matches(status);
CREATE INDEX idx_matches_season ON matches(season);
CREATE INDEX idx_matches_teams ON matches(home_team_id, away_team_id);

-- Predictions table
CREATE TABLE predictions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  match_id UUID REFERENCES matches(id) ON DELETE CASCADE,
  home_win_prob DECIMAL(5,4) NOT NULL,
  draw_prob DECIMAL(5,4) NOT NULL,
  away_win_prob DECIMAL(5,4) NOT NULL,
  confidence INTEGER CHECK (confidence >= 0 AND confidence <= 100),
  recommended_outcome TEXT CHECK (recommended_outcome IN ('home', 'draw', 'away')),
  value_bet BOOLEAN DEFAULT FALSE,
  reasoning TEXT,
  model_version TEXT DEFAULT 'v1.0',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(match_id)
);

-- Odds table (for when API is available)
CREATE TABLE odds (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  match_id UUID REFERENCES matches(id) ON DELETE CASCADE,
  bookmaker TEXT NOT NULL,
  home_win_odds DECIMAL(10,2),
  draw_odds DECIMAL(10,2),
  away_win_odds DECIMAL(10,2),
  over_25_odds DECIMAL(10,2),
  both_teams_to_score_yes_odds DECIMAL(10,2),
  last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(match_id, bookmaker)
);

-- Create index for odds
CREATE INDEX idx_odds_match ON odds(match_id);
CREATE INDEX idx_odds_bookmaker ON odds(bookmaker);

-- Prediction accuracy tracking
CREATE TABLE prediction_results (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  prediction_id UUID REFERENCES predictions(id) ON DELETE CASCADE,
  actual_outcome TEXT CHECK (actual_outcome IN ('home', 'draw', 'away')),
  correct BOOLEAN,
  confidence_when_predicted INTEGER,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- SEO content pages
CREATE TABLE content_pages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  content TEXT,
  meta_description TEXT,
  keywords TEXT[],
  page_type TEXT CHECK (page_type IN ('daily', 'team', 'guide', 'blog')),
  published BOOLEAN DEFAULT FALSE,
  published_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for content
CREATE INDEX idx_content_slug ON content_pages(slug);
CREATE INDEX idx_content_type ON content_pages(page_type);
CREATE INDEX idx_content_published ON content_pages(published);

-- Email subscribers
CREATE TABLE subscribers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  status TEXT DEFAULT 'active' CHECK (status IN ('active', 'unsubscribed', 'bounced')),
  tier TEXT DEFAULT 'free' CHECK (tier IN ('free', 'vip')),
  subscribed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  unsubscribed_at TIMESTAMP WITH TIME ZONE
);

-- Create index for subscribers
CREATE INDEX idx_subscribers_email ON subscribers(email);
CREATE INDEX idx_subscribers_status ON subscribers(status);
CREATE INDEX idx_subscribers_tier ON subscribers(tier);

-- Functions for automatic updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply updated_at triggers
CREATE TRIGGER update_teams_updated_at BEFORE UPDATE ON teams
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_matches_updated_at BEFORE UPDATE ON matches
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_content_updated_at BEFORE UPDATE ON content_pages
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Row Level Security (RLS) policies
ALTER TABLE teams ENABLE ROW LEVEL SECURITY;
ALTER TABLE matches ENABLE ROW LEVEL SECURITY;
ALTER TABLE predictions ENABLE ROW LEVEL SECURITY;
ALTER TABLE odds ENABLE ROW LEVEL SECURITY;
ALTER TABLE content_pages ENABLE ROW LEVEL SECURITY;
ALTER TABLE subscribers ENABLE ROW LEVEL SECURITY;

-- Public read access for teams, matches, predictions
CREATE POLICY "Public read access to teams" ON teams
  FOR SELECT USING (true);

CREATE POLICY "Public read access to matches" ON matches
  FOR SELECT USING (true);

CREATE POLICY "Public read access to predictions" ON predictions
  FOR SELECT USING (true);

CREATE POLICY "Public read access to odds" ON odds
  FOR SELECT USING (true);

CREATE POLICY "Public read access to published content" ON content_pages
  FOR SELECT USING (published = true);

-- Service role can do everything (for backend)
-- This is handled by Supabase automatically with service_role key

-- Views for common queries

-- View: Today's matches with predictions
CREATE VIEW todays_matches_with_predictions AS
SELECT
  m.id,
  m.match_date,
  ht.name AS home_team,
  at.name AS away_team,
  m.status,
  m.home_score,
  m.away_score,
  p.home_win_prob,
  p.draw_prob,
  p.away_win_prob,
  p.confidence,
  p.recommended_outcome,
  p.value_bet
FROM matches m
JOIN teams ht ON m.home_team_id = ht.id
JOIN teams at ON m.away_team_id = at.id
LEFT JOIN predictions p ON m.id = p.match_id
WHERE DATE(m.match_date) = CURRENT_DATE
ORDER BY m.match_date;

-- View: League table
CREATE VIEW league_table AS
SELECT
  name,
  league_position,
  played,
  won,
  drawn,
  lost,
  goals_for,
  goals_against,
  goals_for - goals_against AS goal_difference,
  points
FROM teams
WHERE league = 'Serie B'
ORDER BY points DESC, goal_difference DESC, goals_for DESC;

-- View: Prediction accuracy
CREATE VIEW model_accuracy AS
SELECT
  COUNT(*) AS total_predictions,
  SUM(CASE WHEN correct THEN 1 ELSE 0 END) AS correct_predictions,
  ROUND(SUM(CASE WHEN correct THEN 1 ELSE 0 END)::NUMERIC / COUNT(*) * 100, 2) AS accuracy_percentage,
  AVG(confidence_when_predicted) AS avg_confidence,
  model_version
FROM prediction_results
GROUP BY model_version;

-- Insert sample Serie B teams (2024-25 season)
INSERT INTO teams (name, slug, league_position, points, played, won, drawn, lost, goals_for, goals_against) VALUES
('Brescia', 'brescia', 1, 52, 24, 16, 4, 4, 48, 22),
('Parma', 'parma', 2, 49, 24, 15, 4, 5, 45, 24),
('Venezia', 'venezia', 3, 47, 24, 14, 5, 5, 42, 26),
('Palermo', 'palermo', 4, 45, 24, 13, 6, 5, 38, 25),
('Catanzaro', 'catanzaro', 5, 43, 24, 12, 7, 5, 35, 23),
('Cremonese', 'cremonese', 6, 42, 24, 12, 6, 6, 40, 28),
('Sudtirol', 'sudtirol', 7, 40, 24, 11, 7, 6, 32, 24),
('Bari', 'bari', 8, 39, 24, 11, 6, 7, 33, 26),
('Como', 'como', 9, 38, 24, 10, 8, 6, 35, 28),
('Modena', 'modena', 10, 37, 24, 10, 7, 7, 30, 25),
('Cittadella', 'cittadella', 11, 36, 24, 9, 9, 6, 32, 29),
('Spezia', 'spezia', 12, 35, 24, 9, 8, 7, 34, 31),
('Reggiana', 'reggiana', 13, 34, 24, 9, 7, 8, 30, 30),
('Ternana', 'ternana', 14, 33, 24, 8, 9, 7, 28, 29),
('Cosenza', 'cosenza', 15, 32, 24, 8, 8, 8, 26, 28),
('Benevento', 'benevento', 16, 31, 24, 8, 7, 9, 27, 32),
('Sampdoria', 'sampdoria', 17, 28, 24, 7, 7, 10, 25, 33),
('Ascoli', 'ascoli', 18, 26, 24, 6, 8, 10, 24, 35),
('Lecco', 'lecco', 19, 23, 24, 5, 8, 11, 22, 37),
('Feralpisalo', 'feralpisalo', 20, 20, 24, 4, 8, 12, 20, 38),
('Sudtirol Bolzano', 'sudtirol-bolzano', 21, 18, 24, 4, 6, 14, 18, 40),
('Padova', 'padova', 22, 15, 24, 3, 6, 15, 17, 42)
ON CONFLICT DO NOTHING;

-- Success message
DO $$
BEGIN
  RAISE NOTICE '✅ Schema created successfully!';
  RAISE NOTICE 'Next steps:';
  RAISE NOTICE '1. Set up authentication in Supabase dashboard';
  RAISE NOTICE '2. Configure environment variables in Next.js app';
  RAISE NOTICE '3. Run: npm install @supabase/supabase-js';
END $$;
