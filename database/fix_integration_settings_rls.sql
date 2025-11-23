-- Fix RLS policies for integration_settings table
-- Run this in your Supabase SQL Editor: https://supabase.com/dashboard/project/YOUR_PROJECT/sql

-- Add missing policies for integration_settings table
CREATE POLICY "Enable read access for all users" ON integration_settings FOR SELECT USING (true);
CREATE POLICY "Enable insert access for all users" ON integration_settings FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update access for all users" ON integration_settings FOR UPDATE USING (true);
CREATE POLICY "Enable delete access for all users" ON integration_settings FOR DELETE USING (true);

-- Verify policies were created
SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual
FROM pg_policies
WHERE tablename = 'integration_settings';
