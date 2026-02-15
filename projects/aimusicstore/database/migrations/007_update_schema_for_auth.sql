-- Migration 007: Update schema for auth dependency + enhanced votes
-- 
-- Changes:
-- 1. api_keys: is_active BOOLEAN → status TEXT ('active'|'revoked')
-- 2. agents: Add status TEXT default 'active'
-- 3. votes: Add reasoning, confidence, weight_applied, vote_source
-- 4. votes: Update unique constraint to include item_type
--
-- Author: Carlottta
-- Date: 2026-02-15

-- Transaction for safety
BEGIN;

-- ============================================
-- 1. Update api_keys table
-- ============================================

-- Add status column (temporary allow NULL)
ALTER TABLE api_keys ADD COLUMN IF NOT EXISTS status TEXT;

-- Backfill status from is_active
UPDATE api_keys SET status = 'active' WHERE is_active = TRUE;
UPDATE api_keys SET status = 'revoked' WHERE is_active = FALSE OR is_active IS NULL;

-- Set NOT NULL constraint
ALTER TABLE api_keys ALTER COLUMN status SET NOT NULL;

-- Set default value
ALTER TABLE api_keys ALTER COLUMN status SET DEFAULT 'active';

-- Add check constraint
ALTER TABLE api_keys ADD CONSTRAINT check_api_keys_status 
  CHECK (status IN ('active', 'revoked'));

-- Drop old is_active column (after migration)
-- ALTER TABLE api_keys DROP COLUMN IF EXISTS is_active;

-- ============================================
-- 2. Update agents table
-- ============================================

-- Add status column
ALTER TABLE agents ADD COLUMN IF NOT EXISTS status TEXT DEFAULT 'active';

-- Add check constraint
ALTER TABLE agents ADD CONSTRAINT check_agents_status 
  CHECK (status IN ('active', 'suspended'));

-- Optional: Add name and description columns (commented out for MVP)
-- ALTER TABLE agents ADD COLUMN IF NOT EXISTS name TEXT;
-- ALTER TABLE agents ADD COLUMN IF NOT EXISTS description TEXT;

-- ============================================
-- 3. Update votes table
-- ============================================

-- Add reasoning column (nullable for existing votes, NOT NULL for new votes)
ALTER TABLE votes ADD COLUMN IF NOT EXISTS reasoning TEXT;

-- Add confidence column (0.0-1.0)
ALTER TABLE votes ADD COLUMN IF NOT EXISTS confidence REAL;

-- Add check constraint for confidence (only applies to non-NULL values)
ALTER TABLE votes ADD CONSTRAINT check_votes_confidence 
  CHECK (confidence IS NULL OR (confidence >= 0 AND confidence <= 1));

-- Add weight_applied column (snapshot of agent.reputation_score at vote time)
ALTER TABLE votes ADD COLUMN IF NOT EXISTS weight_applied REAL DEFAULT 0;

-- Add vote_source column ('external', 'bootstrap', 'internal')
ALTER TABLE votes ADD COLUMN IF NOT EXISTS vote_source TEXT DEFAULT 'external';

-- Add check constraint for vote_source
ALTER TABLE votes ADD CONSTRAINT check_votes_vote_source 
  CHECK (vote_source IN ('external', 'bootstrap', 'internal'));

-- Backfill vote_source for existing votes
UPDATE votes SET vote_source = 'bootstrap' WHERE vote_source IS NULL;

-- ============================================
-- 4. Update votes unique constraint
-- ============================================

-- Drop old unique constraint (agent_id, item_id)
-- Note: PostgreSQL doesn't support "IF EXISTS" for constraint drops
-- We'll use a DO block to handle this safely

DO $$
BEGIN
    -- Drop old unique constraint if it exists
    IF EXISTS (
        SELECT 1 FROM pg_constraint 
        WHERE conname = 'votes_agent_id_item_id_key'
    ) THEN
        ALTER TABLE votes DROP CONSTRAINT votes_agent_id_item_id_key;
    END IF;
    
    -- Drop other possible names for the constraint
    IF EXISTS (
        SELECT 1 FROM pg_constraint 
        WHERE conname = 'unique_vote_per_agent'
    ) THEN
        ALTER TABLE votes DROP CONSTRAINT unique_vote_per_agent;
    END IF;
END $$;

-- Add new unique constraint (agent_id, item_id, item_type)
-- This ensures one vote per agent per item (regardless of song vs tool)
ALTER TABLE votes ADD CONSTRAINT unique_vote_per_agent_and_type 
  UNIQUE (agent_id, item_id, item_type);

-- ============================================
-- 5. Create indexes for new columns
-- ============================================

-- Index for api_keys.status
CREATE INDEX IF NOT EXISTS idx_api_keys_status ON api_keys(status);

-- Index for agents.status
CREATE INDEX IF NOT EXISTS idx_agents_status ON agents(status);

-- Index for votes.vote_source
CREATE INDEX IF NOT EXISTS idx_votes_vote_source ON votes(vote_source);

-- Index for votes.confidence (for queries filtering by confidence)
CREATE INDEX IF NOT EXISTS idx_votes_confidence ON votes(confidence) WHERE confidence IS NOT NULL;

-- ============================================
-- 6. Update comments on columns
-- ============================================

COMMENT ON COLUMN api_keys.status IS 'Key status: active or revoked';
COMMENT ON COLUMN agents.status IS 'Agent status: active or suspended';
COMMENT ON COLUMN votes.reasoning IS 'Vote reasoning (min 30 chars for external votes)';
COMMENT ON COLUMN votes.confidence IS 'Vote confidence (0.0-1.0, optional)';
COMMENT ON COLUMN votes.weight_applied IS 'Agent reputation score at vote time (snapshot)';
COMMENT ON COLUMN votes.vote_source IS 'Vote source: external (API), bootstrap (initial), internal (admin)';

COMMIT;

-- ============================================
-- Verification Queries
-- ============================================

-- Check api_keys structure
-- SELECT column_name, data_type, column_default 
-- FROM information_schema.columns 
-- WHERE table_name = 'api_keys' 
-- AND column_name IN ('status', 'is_active');

-- Check agents structure
-- SELECT column_name, data_type, column_default 
-- FROM information_schema.columns 
-- WHERE table_name = 'agents' 
-- AND column_name = 'status';

-- Check votes structure
-- SELECT column_name, data_type, column_default 
-- FROM information_schema.columns 
-- WHERE table_name = 'votes' 
-- AND column_name IN ('reasoning', 'confidence', 'weight_applied', 'vote_source');

-- Check unique constraint
-- SELECT conname FROM pg_constraint 
-- WHERE conname LIKE '%unique_vote%' 
-- AND conrelid = 'votes'::regclass;
