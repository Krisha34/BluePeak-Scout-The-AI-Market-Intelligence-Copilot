'use client'

import { useEffect, useState } from 'react'
import { apiClient } from '@/lib/api'
import { AnalyticsMetrics, Competitor, Trend, ResearchFinding } from '@/types'
import { Activity, TrendingUp, Users, FileText, AlertCircle, CheckCircle, Bell, RefreshCw } from 'lucide-react'
import { LineChart, Line, AreaChart, Area, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import toast, { Toaster } from 'react-hot-toast'

export default function Dashboard() {
  const [metrics, setMetrics] = useState<AnalyticsMetrics | null>(null)
  const [competitors, setCompetitors] = useState<Competitor[]>([])
  const [trends, setTrends] = useState<Trend[]>([])
  const [findings, setFindings] = useState<ResearchFinding[]>([])
  const [loading, setLoading] = useState(true)
  const [lastUpdate, setLastUpdate] = useState(new Date())

  // Mock data for activity timeline (last 7 days)
  const activityData = [
    { day: 'Mon', activity: 45 },
    { day: 'Tue', activity: 82 },
    { day: 'Wed', activity: 58 },
    { day: 'Thu', activity: 91 },
    { day: 'Fri', activity: 73 },
    { day: 'Sat', activity: 67 },
    { day: 'Sun', activity: 79 }
  ]

  const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444']

  useEffect(() => {
    loadDashboardData()
    // Set up auto-refresh every 30 seconds
    const interval = setInterval(() => {
      loadDashboardData(true)
    }, 30000)
    return () => clearInterval(interval)
  }, [])

  const loadDashboardData = async (isRefresh = false) => {
    try {
      if (!isRefresh) setLoading(true)
      const data = await apiClient.getDashboardData()
      setMetrics(data.metrics)
      setCompetitors(data.recent_competitors || [])
      setTrends(data.trending_topics || [])
      setFindings(data.recent_findings || [])
      setLastUpdate(new Date())
      if (isRefresh) {
        toast.success('Dashboard updated')
      }
    } catch (error) {
      console.error('Error loading dashboard:', error)
      toast.error('Failed to load dashboard data')
    } finally {
      setLoading(false)
    }
  }

  const competitiveHealthScore = metrics ? Math.round(
    (metrics.total_competitors * 0.3) +
    (metrics.active_trends * 0.4) +
    (metrics.findings_this_week * 0.2) +
    (metrics.reports_generated * 0.1)
  ) : 0

  const getHealthStatus = (score: number) => {
    if (score >= 80) return { label: 'Excellent', color: 'text-green-600', bg: 'bg-green-100' }
    if (score >= 60) return { label: 'Good', color: 'text-blue-600', bg: 'bg-blue-100' }
    if (score >= 40) return { label: 'Fair', color: 'text-yellow-600', bg: 'bg-yellow-100' }
    return { label: 'Needs Attention', color: 'text-red-600', bg: 'bg-red-100' }
  }

  const healthStatus = getHealthStatus(competitiveHealthScore)

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="p-4 md:p-8 bg-gray-50 min-h-screen">
      <Toaster position="top-right" />

      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-2">Real-time competitive intelligence</p>
        </div>
        <div className="flex items-center gap-4 mt-4 md:mt-0">
          <span className="text-sm text-gray-500">
            Last updated: {lastUpdate.toLocaleTimeString()}
          </span>
          <button
            onClick={() => loadDashboardData(true)}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <RefreshCw className="w-4 h-4" />
            Refresh
          </button>
        </div>
      </div>

      {/* Metrics Grid */}
      {metrics && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <MetricCard
            title="Total Competitors"
            value={metrics.total_competitors}
            icon={<Users className="w-6 h-6" />}
            trend="+12%"
            trendUp={true}
            color="blue"
          />
          <MetricCard
            title="Active Trends"
            value={metrics.active_trends}
            icon={<TrendingUp className="w-6 h-6" />}
            trend="+8%"
            trendUp={true}
            color="green"
          />
          <MetricCard
            title="Findings This Week"
            value={metrics.findings_this_week}
            icon={<Activity className="w-6 h-6" />}
            trend="+23%"
            trendUp={true}
            color="purple"
          />
          <MetricCard
            title="Reports Generated"
            value={metrics.reports_generated}
            icon={<FileText className="w-6 h-6" />}
            trend="+5"
            trendUp={true}
            color="orange"
          />
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        {/* Competitive Health Score */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-lg font-semibold mb-4">Competitive Health Score</h2>
          <div className="flex flex-col items-center">
            <div className="relative w-32 h-32">
              <svg className="transform -rotate-90 w-32 h-32">
                <circle
                  cx="64"
                  cy="64"
                  r="56"
                  stroke="#E5E7EB"
                  strokeWidth="12"
                  fill="none"
                />
                <circle
                  cx="64"
                  cy="64"
                  r="56"
                  stroke="#3B82F6"
                  strokeWidth="12"
                  fill="none"
                  strokeDasharray={`${(competitiveHealthScore / 100) * 351.86} 351.86`}
                  strokeLinecap="round"
                />
              </svg>
              <div className="absolute inset-0 flex items-center justify-center">
                <span className="text-3xl font-bold text-gray-900">{competitiveHealthScore}</span>
              </div>
            </div>
            <div className={`mt-4 px-4 py-2 rounded-full ${healthStatus.bg}`}>
              <span className={`font-semibold ${healthStatus.color}`}>{healthStatus.label}</span>
            </div>
            <p className="text-sm text-gray-600 mt-3 text-center">
              Market stability is high, but innovation requires attention
            </p>
          </div>

          {/* Quick Stats */}
          <div className="mt-6 space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Competitor Updates (24h)</span>
              <span className="font-semibold text-gray-900 flex items-center gap-1">
                <CheckCircle className="w-4 h-4 text-green-600" /> 5
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">AI Feature Launches (30d)</span>
              <span className="font-semibold text-gray-900 flex items-center gap-1">
                <CheckCircle className="w-4 h-4 text-green-600" /> 3
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">RAG Queries (Weekly)</span>
              <span className="font-semibold text-gray-900">142</span>
            </div>
          </div>
        </div>

        {/* Activity Timeline */}
        <div className="lg:col-span-2 bg-white rounded-lg shadow-lg p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-semibold">Activity Timeline (Last 7 Days)</h2>
            <div className="flex items-center gap-2 text-sm text-blue-600">
              <Bell className="w-4 h-4" />
              <span>Spike on Friday: 3 competitors updated pricing</span>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={200}>
            <AreaChart data={activityData}>
              <defs>
                <linearGradient id="colorActivity" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#3B82F6" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
              <XAxis dataKey="day" stroke="#6B7280" />
              <YAxis stroke="#6B7280" />
              <Tooltip
                contentStyle={{ backgroundColor: '#fff', border: '1px solid #E5E7EB', borderRadius: '0.5rem' }}
              />
              <Area
                type="monotone"
                dataKey="activity"
                stroke="#3B82F6"
                fillOpacity={1}
                fill="url(#colorActivity)"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Competitive Activity Feed */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-semibold">Competitive Activity Feed</h2>
            <span className="text-sm text-gray-500">Real-time</span>
          </div>
          <div className="space-y-4 max-h-96 overflow-y-auto">
            {competitors.slice(0, 5).map((competitor, index) => (
              <div key={competitor.id} className="flex items-start gap-4 p-4 hover:bg-gray-50 rounded-lg transition-colors border border-gray-100">
                <div className="flex-shrink-0">
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
                    index === 0 ? 'bg-red-100' :
                    index === 1 ? 'bg-yellow-100' :
                    index === 2 ? 'bg-green-100' :
                    'bg-blue-100'
                  }`}>
                    <span className="text-lg font-bold">
                      {competitor.name.charAt(0)}
                    </span>
                  </div>
                </div>
                <div className="flex-1">
                  <div className="flex items-center justify-between">
                    <h3 className="font-semibold text-gray-900">{competitor.name}</h3>
                    <span className={`px-2 py-1 rounded-full text-xs ${
                      competitor.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                    }`}>
                      {competitor.status}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mt-1">{competitor.industry}</p>
                  <p className="text-xs text-gray-500 mt-2">
                    {competitor.last_analyzed ?
                      `Analyzed ${new Date(competitor.last_analyzed).toLocaleString()}` :
                      'Not yet analyzed'}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Active Trends & Alerts */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-semibold">Active Trends & Alerts</h2>
            <button className="text-sm text-blue-600 hover:text-blue-700">View All</button>
          </div>
          <div className="space-y-4 max-h-96 overflow-y-auto">
            {/* High Priority Alert */}
            <div className="border-2 border-red-200 bg-red-50 rounded-lg p-4">
              <div className="flex items-start gap-3">
                <AlertCircle className="w-5 h-5 text-red-600 mt-0.5" />
                <div>
                  <h3 className="font-semibold text-red-900">HIGH PRIORITY</h3>
                  <p className="text-sm text-red-800 mt-1">
                    Mailchimp launched Creative Assistant - direct threat to BluePeak's service offering
                  </p>
                  <button className="text-xs text-red-700 font-medium mt-2 hover:underline">
                    Review Report
                  </button>
                </div>
              </div>
            </div>

            {trends.slice(0, 5).map((trend) => (
              <div key={trend.id} className="p-4 hover:bg-gray-50 rounded-lg transition-colors border border-gray-100">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="font-semibold text-gray-900">{trend.title}</h3>
                    <p className="text-sm text-gray-600 mt-1 line-clamp-2">{trend.description}</p>
                    <div className="flex items-center gap-3 mt-2">
                      <span className={`px-2 py-1 rounded-full text-xs ${
                        trend.status === 'growing' ? 'bg-green-100 text-green-800' :
                        trend.status === 'emerging' ? 'bg-blue-100 text-blue-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {trend.status}
                      </span>
                      <span className="text-xs text-gray-500">
                        {(trend.confidence_score * 100).toFixed(0)}% confidence
                      </span>
                    </div>
                  </div>
                  <TrendingUp className="w-5 h-5 text-green-600" />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Industry Distribution */}
      {metrics && metrics.top_industries.length > 0 && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-lg font-semibold mb-4">Industry Distribution</h2>
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={metrics.top_industries}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, count }) => `${name}: ${count}`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="count"
                >
                  {metrics.top_industries.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-lg font-semibold mb-4">Sentiment Analysis</h2>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={[
                { name: 'Positive', value: metrics.sentiment_breakdown.positive || 5 },
                { name: 'Neutral', value: metrics.sentiment_breakdown.neutral || 12 },
                { name: 'Negative', value: metrics.sentiment_breakdown.negative || 2 }
              ]}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                <XAxis dataKey="name" stroke="#6B7280" />
                <YAxis stroke="#6B7280" />
                <Tooltip
                  contentStyle={{ backgroundColor: '#fff', border: '1px solid #E5E7EB', borderRadius: '0.5rem' }}
                />
                <Bar dataKey="value" fill="#3B82F6" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
    </div>
  )
}

// Metric Card Component
function MetricCard({ title, value, icon, trend, trendUp, color }: {
  title: string
  value: number
  icon: React.ReactNode
  trend: string
  trendUp: boolean
  color: 'blue' | 'green' | 'purple' | 'orange'
}) {
  const colorClasses = {
    blue: 'bg-blue-100 text-blue-600',
    green: 'bg-green-100 text-green-600',
    purple: 'bg-purple-100 text-purple-600',
    orange: 'bg-orange-100 text-orange-600'
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow">
      <div className="flex items-center justify-between">
        <div className={`p-3 rounded-lg ${colorClasses[color]}`}>
          {icon}
        </div>
        <span className={`text-sm font-medium ${trendUp ? 'text-green-600' : 'text-red-600'}`}>
          {trend}
        </span>
      </div>
      <h3 className="text-gray-600 text-sm mt-4">{title}</h3>
      <p className="text-3xl font-bold text-gray-900 mt-2">{value}</p>
    </div>
  )
}
