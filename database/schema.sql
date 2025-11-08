-- BluePeak Compass Database Schema for Supabase
-- Run this script in your Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Competitors Table
CREATE TABLE IF NOT EXISTS competitors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    website VARCHAR(500),
    description TEXT,
    industry VARCHAR(100) NOT NULL,
    founded_year INTEGER,
    headquarters VARCHAR(255),
    employee_count INTEGER,
    status VARCHAR(50) DEFAULT 'active',
    monitoring_score DECIMAL(3, 2) DEFAULT 0.0,
    last_analyzed TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Trends Table
CREATE TABLE IF NOT EXISTS trends (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    industry VARCHAR(100) NOT NULL,
    status VARCHAR(50) DEFAULT 'emerging',
    confidence_score DECIMAL(3, 2) NOT NULL,
    keywords TEXT[], -- Array of keywords
    mention_count INTEGER DEFAULT 0,
    growth_rate DECIMAL(5, 2) DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Research Findings Table
CREATE TABLE IF NOT EXISTS research_findings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    competitor_id UUID REFERENCES competitors(id) ON DELETE CASCADE,
    finding_type VARCHAR(100) NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    source_url VARCHAR(500),
    sentiment VARCHAR(50) DEFAULT 'neutral',
    importance_score DECIMAL(3, 2) NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Reports Table
CREATE TABLE IF NOT EXISTS reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    report_type VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    summary TEXT NOT NULL,
    competitor_ids UUID[],
    trend_ids UUID[],
    generated_by VARCHAR(100) DEFAULT 'ai_agent',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Conversations Table (for chat)
CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(255),
    messages JSONB DEFAULT '[]',
    context_ids UUID[],
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Integration Settings Table
CREATE TABLE IF NOT EXISTS integration_settings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(255) NOT NULL UNIQUE,
    slack_enabled BOOLEAN DEFAULT FALSE,
    slack_channel_id VARCHAR(255),
    slack_webhook_url VARCHAR(500),
    email_enabled BOOLEAN DEFAULT FALSE,
    email_recipients TEXT[],
    email_frequency VARCHAR(50) DEFAULT 'daily',
    notification_types TEXT[],
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Social Mentions Table
CREATE TABLE IF NOT EXISTS social_mentions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    competitor_id UUID REFERENCES competitors(id) ON DELETE CASCADE,
    platform VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    author VARCHAR(255),
    sentiment VARCHAR(50) DEFAULT 'neutral',
    engagement_score INTEGER DEFAULT 0,
    url VARCHAR(500),
    mentioned_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Product Information Table
CREATE TABLE IF NOT EXISTS products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    competitor_id UUID REFERENCES competitors(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    pricing JSONB,
    features TEXT[],
    launch_date DATE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for better query performance
CREATE INDEX idx_competitors_industry ON competitors(industry);
CREATE INDEX idx_competitors_status ON competitors(status);
CREATE INDEX idx_trends_industry ON trends(industry);
CREATE INDEX idx_trends_status ON trends(status);
CREATE INDEX idx_findings_competitor ON research_findings(competitor_id);
CREATE INDEX idx_findings_created ON research_findings(created_at DESC);
CREATE INDEX idx_reports_created ON reports(created_at DESC);
CREATE INDEX idx_conversations_user ON conversations(user_id);
CREATE INDEX idx_social_mentions_competitor ON social_mentions(competitor_id);
CREATE INDEX idx_products_competitor ON products(competitor_id);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_competitors_updated_at BEFORE UPDATE ON competitors
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_trends_updated_at BEFORE UPDATE ON trends
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_conversations_updated_at BEFORE UPDATE ON conversations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_products_updated_at BEFORE UPDATE ON products
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Enable Row Level Security (RLS)
ALTER TABLE competitors ENABLE ROW LEVEL SECURITY;
ALTER TABLE trends ENABLE ROW LEVEL SECURITY;
ALTER TABLE research_findings ENABLE ROW LEVEL SECURITY;
ALTER TABLE reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE integration_settings ENABLE ROW LEVEL SECURITY;
ALTER TABLE social_mentions ENABLE ROW LEVEL SECURITY;
ALTER TABLE products ENABLE ROW LEVEL SECURITY;

-- Create policies (for now, allow all authenticated users)
-- In production, you'd want more granular policies

CREATE POLICY "Enable read access for all users" ON competitors FOR SELECT USING (true);
CREATE POLICY "Enable insert access for all users" ON competitors FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update access for all users" ON competitors FOR UPDATE USING (true);

CREATE POLICY "Enable read access for all users" ON trends FOR SELECT USING (true);
CREATE POLICY "Enable insert access for all users" ON trends FOR INSERT WITH CHECK (true);

CREATE POLICY "Enable read access for all users" ON research_findings FOR SELECT USING (true);
CREATE POLICY "Enable insert access for all users" ON research_findings FOR INSERT WITH CHECK (true);

CREATE POLICY "Enable read access for all users" ON reports FOR SELECT USING (true);
CREATE POLICY "Enable insert access for all users" ON reports FOR INSERT WITH CHECK (true);

CREATE POLICY "Enable read access for all users" ON conversations FOR SELECT USING (true);
CREATE POLICY "Enable insert access for all users" ON conversations FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update access for all users" ON conversations FOR UPDATE USING (true);

CREATE POLICY "Enable read access for all users" ON social_mentions FOR SELECT USING (true);
CREATE POLICY "Enable insert access for all users" ON social_mentions FOR INSERT WITH CHECK (true);

CREATE POLICY "Enable read access for all users" ON products FOR SELECT USING (true);
CREATE POLICY "Enable insert access for all users" ON products FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update access for all users" ON products FOR UPDATE USING (true);
