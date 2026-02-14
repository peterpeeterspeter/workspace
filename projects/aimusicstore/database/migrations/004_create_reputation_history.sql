-- Migration 004: Create reputation_history table
-- Date: 2026-02-14 07:04 UTC
-- Description: Track reputation score changes over time for transparency and admin oversight

-- Create reputation_history table
CREATE TABLE IF NOT EXISTS reputation_history (
    id SERIAL PRIMARY KEY,
    agent_id VARCHAR(255) NOT NULL,
    old_score INTEGER NOT NULL,
    new_score INTEGER NOT NULL,
    change_reason TEXT,
    timestamp TIMESTAMP DEFAULT NOW(),

    -- Foreign key constraint
    CONSTRAINT fk_reputation_history_agent
        FOREIGN KEY (agent_id)
        REFERENCES agents(id)
        ON DELETE CASCADE
);

-- Create index for fast agent lookups
CREATE INDEX IF NOT EXISTS idx_reputation_history_agent_id
    ON reputation_history(agent_id);

-- Create index for time-based queries (recent history)
CREATE INDEX IF NOT EXISTS idx_reputation_history_timestamp
    ON reputation_history(timestamp DESC);

-- Create composite index for agent + timestamp queries
CREATE INDEX IF NOT EXISTS idx_reputation_history_agent_timestamp
    ON reputation_history(agent_id, timestamp DESC);

-- Success message
DO $$
BEGIN
    RAISE NOTICE 'Migration 004 completed: reputation_history table created';
END $$;
