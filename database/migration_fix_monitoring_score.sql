-- Migration to fix monitoring_score values
-- Run this in your Supabase SQL Editor

-- Update the default value for new records
ALTER TABLE competitors
ALTER COLUMN monitoring_score SET DEFAULT 0.5;

-- Update existing competitors that have 0 monitoring score to 0.5
UPDATE competitors
SET monitoring_score = 0.5
WHERE monitoring_score = 0.0 OR monitoring_score IS NULL;

-- Verify the changes
SELECT id, name, monitoring_score, last_analyzed
FROM competitors
ORDER BY created_at DESC;
