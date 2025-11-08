/**
 * TypeScript type definitions
 */

export interface Competitor {
  id: string;
  name: string;
  website?: string;
  description?: string;
  industry: string;
  founded_year?: number;
  headquarters?: string;
  employee_count?: number;
  status: 'active' | 'inactive' | 'monitoring';
  monitoring_score: number;
  last_analyzed?: string;
  created_at: string;
  updated_at: string;
}

export interface Trend {
  id: string;
  title: string;
  description: string;
  industry: string;
  status: 'emerging' | 'growing' | 'declining' | 'stable';
  confidence_score: number;
  keywords: string[];
  mention_count: number;
  growth_rate: number;
  created_at: string;
  updated_at: string;
}

export interface ResearchFinding {
  id: string;
  competitor_id: string;
  finding_type: string;
  title: string;
  content: string;
  source_url?: string;
  sentiment: 'positive' | 'negative' | 'neutral';
  importance_score: number;
  metadata: Record<string, any>;
  created_at: string;
}

export interface Report {
  id: string;
  title: string;
  report_type: string;
  content: string;
  summary: string;
  competitor_ids: string[];
  trend_ids: string[];
  generated_by: string;
  created_at: string;
}

export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
}

export interface Conversation {
  id: string;
  user_id: string;
  title?: string;
  messages: ChatMessage[];
  context_ids: string[];
  created_at: string;
  updated_at: string;
}

export interface AnalyticsMetrics {
  total_competitors: number;
  active_trends: number;
  findings_this_week: number;
  reports_generated: number;
  sentiment_breakdown: {
    positive: number;
    neutral: number;
    negative: number;
  };
  top_industries: Array<{
    name: string;
    count: number;
  }>;
}

export interface IntegrationSettings {
  slack: {
    enabled: boolean;
    channel_id?: string;
    webhook_url?: string;
    notification_types: string[];
  };
  email: {
    enabled: boolean;
    recipients: string[];
    frequency: string;
    notification_types: string[];
  };
}
