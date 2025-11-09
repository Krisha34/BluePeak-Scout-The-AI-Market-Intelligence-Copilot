# Fix Monitoring Score Issue

## Problem
Existing competitors in the database have `monitoring_score = 0.0` because the original schema defaulted to 0.0.

## Solution
Run the migration script to update existing data and fix the default value.

## Steps to Fix

### 1. Run the Migration Script

Open your Supabase Dashboard:
1. Go to https://supabase.com
2. Select your project
3. Click on **SQL Editor** in the left sidebar
4. Click **New Query**
5. Copy and paste the contents of `migration_fix_monitoring_score.sql`
6. Click **Run** or press `Ctrl/Cmd + Enter`

### 2. Verify the Fix

After running the migration, check the results:

```sql
SELECT id, name, monitoring_score, last_analyzed
FROM competitors
ORDER BY created_at DESC;
```

You should see:
- All existing competitors now have `monitoring_score = 0.5` (50%)
- New competitors will automatically get `0.5` as default

### 3. Test the Feature

1. Go to the **Competitors** page in your app
2. Click **Analyse** on any competitor
3. The monitoring score should increment by 10% (0.5 → 0.6)
4. Run analysis multiple times to see it increase: 0.6 → 0.7 → 0.8, etc.
5. Maximum value is 1.0 (100%)

### 4. Verify in the UI

- **View Details** button: Shows the monitoring score with a progress bar
- Scores are categorized as:
  - 🔴 0-30%: "Needs analysis"
  - 🟡 30-70%: "Moderate activity"
  - 🟢 70-100%: "Actively monitored"

## What Monitoring Score Means

**Monitoring Score** tracks how actively you're monitoring each competitor:

- **Starts at 50%** when you add a new competitor
- **Increases by 10%** each time you run an analysis
- **Maxes at 100%** (actively monitored)
- Helps prioritize which competitors need more attention

## Backend Logs

To see monitoring score updates in action, check your backend logs:

```bash
cd backend
# You should see logs like:
# INFO: Updating competitor HubSpot: monitoring_score from 0.5 to 0.6
```

## Troubleshooting

### If scores are still showing 0:

1. **Check database connection**: Make sure your Supabase credentials are correct in `.env`
2. **Verify migration ran**: Query the database to check values
3. **Clear browser cache**: Sometimes old data is cached
4. **Restart backend**: `cd backend && uvicorn app.main:app --reload`
5. **Check backend logs**: Look for the monitoring_score update messages

### Common Issues:

**Q: Score not updating after analysis?**
- Check backend logs for errors
- Verify the update query succeeded in database

**Q: Still seeing 0 in the UI?**
- Run the migration script if you haven't
- Refresh the page (F5)
- Check browser console for errors

## Migration Script Content

The migration does two things:

```sql
-- 1. Change default for new records
ALTER TABLE competitors
ALTER COLUMN monitoring_score SET DEFAULT 0.5;

-- 2. Fix existing records
UPDATE competitors
SET monitoring_score = 0.5
WHERE monitoring_score = 0.0 OR monitoring_score IS NULL;
```

## Success Criteria

✅ All competitors show 50% or higher monitoring score
✅ Score increases by 10% after each analysis
✅ "View Details" modal shows the score correctly
✅ Backend logs show score updates
✅ Score caps at 100%
