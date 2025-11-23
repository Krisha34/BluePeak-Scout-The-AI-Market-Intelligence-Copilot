'use client'

import { useState, useEffect } from 'react'
import { apiClient } from '@/lib/api'
import { Trend } from '@/types'
import { TrendingUp, TrendingDown, Minus, Search } from 'lucide-react'
import toast from 'react-hot-toast'

export default function TrendsPage() {
  const [trends, setTrends] = useState<Trend[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<string>('all')
  const [searchQuery, setSearchQuery] = useState('')

  useEffect(() => {
    loadTrends()
  }, [filter])

  const loadTrends = async () => {
    try {
      setLoading(true)
      const filters: any = {}
      if (filter !== 'all') {
        filters.status = filter
      }
      const data = await apiClient.getTrends(filters)
      setTrends(data)
    } catch (error) {
      console.error('Error loading trends:', error)
      toast.error('Failed to load trends')
    } finally {
      setLoading(false)
    }
  }

  const filteredTrends = trends.filter(trend =>
    trend.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    trend.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
    trend.keywords.some(k => k.toLowerCase().includes(searchQuery.toLowerCase()))
  )

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'growing':
        return <TrendingUp className="w-5 h-5 text-green-600" />
      case 'declining':
        return <TrendingDown className="w-5 h-5 text-red-600" />
      case 'emerging':
        return <TrendingUp className="w-5 h-5 text-blue-600" />
      default:
        return <Minus className="w-5 h-5 text-gray-600" />
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'growing':
        return 'bg-green-100 text-green-800'
      case 'declining':
        return 'bg-red-100 text-red-800'
      case 'emerging':
        return 'bg-blue-100 text-blue-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Market Trends</h1>
        <p className="text-gray-600 mt-2">Track emerging trends and market dynamics</p>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                placeholder="Search trends..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>
          </div>
          <div className="flex gap-2">
            {['all', 'emerging', 'growing', 'stable', 'declining'].map((status) => (
              <button
                key={status}
                onClick={() => setFilter(status)}
                className={`px-4 py-2 rounded-lg capitalize ${
                  filter === status
                    ? 'bg-primary-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {status}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Trends Grid */}
      {loading ? (
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading trends...</p>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredTrends.map((trend) => (
            <div key={trend.id} className="bg-white rounded-lg shadow hover:shadow-lg transition-shadow p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-2">
                  {getStatusIcon(trend.status)}
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(trend.status)}`}>
                    {trend.status}
                  </span>
                </div>
                <span className="text-sm text-gray-500">{(trend.confidence_score * 100).toFixed(0)}%</span>
              </div>

              <h3 className="text-lg font-semibold text-gray-900 mb-2">{trend.title}</h3>
              <p className="text-gray-600 text-sm mb-4 line-clamp-3">{trend.description}</p>

              <div className="flex flex-wrap gap-2 mb-4">
                {trend.keywords.slice(0, 5).map((keyword, i) => (
                  <span key={i} className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs">
                    {keyword}
                  </span>
                ))}
              </div>

              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-500">{trend.mention_count} mentions</span>
                <span className={`font-medium ${trend.growth_rate > 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {trend.growth_rate > 0 ? '+' : ''}{trend.growth_rate}%
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
