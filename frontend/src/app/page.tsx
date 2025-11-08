'use client'

import { useEffect, useState } from 'react'
import { apiClient } from '@/lib/api'
import { AnalyticsMetrics, Competitor, Trend, ResearchFinding } from '@/types'
import MetricsCard from '@/components/dashboard/MetricsCard'
import CompetitorCard from '@/components/dashboard/CompetitorCard'
import TrendCard from '@/components/dashboard/TrendCard'
import { Activity, TrendingUp, Users, FileText } from 'lucide-react'

export default function Dashboard() {
  const [metrics, setMetrics] = useState<AnalyticsMetrics | null>(null)
  const [competitors, setCompetitors] = useState<Competitor[]>([])
  const [trends, setTrends] = useState<Trend[]>([])
  const [findings, setFindings] = useState<ResearchFinding[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    try {
      setLoading(true)
      const data = await apiClient.getDashboardData()
      setMetrics(data.metrics)
      setCompetitors(data.recent_competitors || [])
      setTrends(data.trending_topics || [])
      setFindings(data.recent_findings || [])
    } catch (error) {
      console.error('Error loading dashboard:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-2">Competitive intelligence at a glance</p>
      </div>

      {/* Metrics Grid */}
      {metrics && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <MetricsCard
            title="Total Competitors"
            value={metrics.total_competitors}
            icon={<Users className="w-6 h-6" />}
            trend="+12% from last month"
            color="blue"
          />
          <MetricsCard
            title="Active Trends"
            value={metrics.active_trends}
            icon={<TrendingUp className="w-6 h-6" />}
            trend="+8% from last week"
            color="green"
          />
          <MetricsCard
            title="Findings This Week"
            value={metrics.findings_this_week}
            icon={<Activity className="w-6 h-6" />}
            trend="+23% from last week"
            color="purple"
          />
          <MetricsCard
            title="Reports Generated"
            value={metrics.reports_generated}
            icon={<FileText className="w-6 h-6" />}
            trend="+5 this month"
            color="orange"
          />
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Recent Competitors */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Recent Competitors</h2>
          <div className="space-y-4">
            {competitors.slice(0, 5).map((competitor) => (
              <CompetitorCard key={competitor.id} competitor={competitor} />
            ))}
          </div>
        </div>

        {/* Trending Topics */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Trending Topics</h2>
          <div className="space-y-4">
            {trends.slice(0, 5).map((trend) => (
              <TrendCard key={trend.id} trend={trend} />
            ))}
          </div>
        </div>
      </div>

      {/* Recent Findings */}
      <div className="mt-8 bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Recent Findings</h2>
        <div className="space-y-3">
          {findings.slice(0, 10).map((finding) => (
            <div key={finding.id} className="border-l-4 border-primary-500 pl-4 py-2">
              <h3 className="font-medium text-gray-900">{finding.title}</h3>
              <p className="text-sm text-gray-600 mt-1">{finding.content.substring(0, 150)}...</p>
              <div className="flex items-center gap-4 mt-2 text-xs text-gray-500">
                <span className="capitalize">{finding.finding_type}</span>
                <span>•</span>
                <span className={`capitalize ${
                  finding.sentiment === 'positive' ? 'text-green-600' :
                  finding.sentiment === 'negative' ? 'text-red-600' :
                  'text-gray-600'
                }`}>
                  {finding.sentiment}
                </span>
                <span>•</span>
                <span>{new Date(finding.created_at).toLocaleDateString()}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
