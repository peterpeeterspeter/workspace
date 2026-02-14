-- Migration 002: Add affiliate_link to songs table
-- For US-004: Song Detail Endpoint
-- Created: 2026-02-13

-- Add affiliate_link column to songs table
ALTER TABLE songs
ADD COLUMN affiliate_link TEXT;

-- Add comment for documentation
COMMENT ON COLUMN songs.affiliate_link IS 'Affiliate link for monetization (e.g., Spotify, Apple Music)';

-- Add index for affiliate link queries (optional, for future filtering)
-- CREATE INDEX idx_songs_affiliate_link ON songs(affiliate_link);

-- Verify the change
-- SELECT column_name, data_type, is_nullable
-- FROM information_schema.columns
-- WHERE table_name = 'songs'
-- AND column_name = 'affiliate_link';
