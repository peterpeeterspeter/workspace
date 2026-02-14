-- Migration 003: Add weighted_score columns
-- Date: 2026-02-14 07:04 UTC
-- Description: Add weighted_score column to songs and tools tables for reputation-weighted rankings

-- Add weighted_score column to songs table
ALTER TABLE songs ADD COLUMN IF NOT EXISTS weighted_score INTEGER DEFAULT 0;

-- Create index for weighted score (descending order for rankings)
CREATE INDEX IF NOT EXISTS idx_songs_weighted_score ON songs(weighted_score DESC);

-- Add weighted_score column to tools table
ALTER TABLE tools ADD COLUMN IF NOT EXISTS weighted_score INTEGER DEFAULT 0;

-- Create index for weighted score (descending order for rankings)
CREATE INDEX IF NOT EXISTS idx_tools_weighted_score ON tools(weighted_score DESC);

-- Success message
DO $$
BEGIN
    RAISE NOTICE 'Migration 003 completed: weighted_score columns added to songs and tools tables';
END $$;
