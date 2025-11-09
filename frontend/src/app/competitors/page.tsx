'use client'

import { useState, useEffect } from 'react'
import { apiClient } from '@/lib/api'
import { Competitor } from '@/types'
import { Users, Search, Building2, MapPin, Globe, Plus, TrendingUp, AlertTriangle, CheckCircle, Filter, RefreshCw } from 'lucide-react'
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import toast, { Toaster } from 'react-hot-toast'
import AnalysisModal from '@/components/AnalysisModal'

export default function CompetitorsPage() {
  const [competitors, setCompetitors] = useState<Competitor[]>([])
  const [loading, setLoading] = useState(true)
  const [statusFilter, setStatusFilter] = useState<string>('all')
  const [industryFilter, setIndustryFilter] = useState<string>('all')
  const [searchQuery, setSearchQuery] = useState('')
  const [showAddForm, setShowAddForm] = useState(false)
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid')
  const [showAnalysisModal, setShowAnalysisModal] = useState(false)
  const [analysisData, setAnalysisData] = useState<any>(null)
  const [newCompetitor, setNewCompetitor] = useState({
    name: '',
    website: '',
    industry: '',
    description: '',
    founded_year: undefined as number | undefined,
    headquarters: '',
    employee_count: undefined as number | undefined
  })

  useEffect(() => {
    loadCompetitors()
  }, [])

  const loadCompetitors = async () => {
    try {
      setLoading(true)
      const data = await apiClient.getCompetitors()
      setCompetitors(data)
    } catch (error) {
      console.error('Error loading competitors:', error)
      toast.error('Failed to load competitors')
    } finally {
      setLoading(false)
    }
  }

  const handleAddCompetitor = async () => {
    if (!newCompetitor.name || !newCompetitor.industry) {
      toast.error('Name and industry are required')
      return
    }

    try {
      await apiClient.createCompetitor({
        ...newCompetitor,
        status: 'active',
        monitoring_score: 0.5
      })
      toast.success('Competitor added successfully')
      setShowAddForm(false)
      setNewCompetitor({ 
        name: '', 
        website: '', 
        industry: '', 
        description: '', 
        founded_year: undefined, 
        headquarters: '', 
        employee_count: undefined 
      })
      loadCompetitors()
    } catch (error) {
      console.error('Error adding competitor:', error)
      toast.error('Failed to add competitor')
    }
  }

  const handleAnalyze = async (id: string, name: string) => {
    try {
      const loadingToast = toast.loading(`Analyzing ${name}...`)

      // Call automated analysis endpoint
      const response = await apiClient.analyzeCompetitorAutomated(id)

      toast.dismiss(loadingToast)
      toast.success('Analysis complete!')

      // Set analysis data and show modal
      setAnalysisData(response)
      setShowAnalysisModal(true)

      // Reload competitors to update metrics
      loadCompetitors()
    } catch (error) {
      console.error('Error analyzing competitor:', error)
      toast.error('Failed to analyze competitor')
    }
  }

  // Get unique industries for filter
  const industries = Array.from(new Set(competitors.map(c => c.industry)))

  // Apply filters
  const filteredCompetitors = competitors.filter(competitor => {
    const matchesSearch = competitor.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      competitor.industry.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (competitor.description && competitor.description.toLowerCase().includes(searchQuery.toLowerCase()))

    const matchesStatus = statusFilter === 'all' || competitor.status === statusFilter
    const matchesIndustry = industryFilter === 'all' || competitor.industry === industryFilter

    return matchesSearch && matchesStatus && matchesIndustry
  })

  // Prepare data for charts
  const statusDistribution = competitors.reduce((acc, comp) => {
    acc[comp.status] = (acc[comp.status] || 0) + 1
    return acc
  }, {} as Record<string, number>)

  const statusChartData = Object.entries(statusDistribution).map(([status, count]) => ({
    name: status,
    value: count
  }))

  const COLORS = ['#10B981', '#3B82F6', '#F59E0B', '#EF4444']

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800'
      case 'inactive':
        return 'bg-gray-100 text-gray-800'
      case 'monitoring':
        return 'bg-blue-100 text-blue-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active':
        return <CheckCircle className="w-4 h-4 text-green-600" />
      case 'monitoring':
        return <AlertTriangle className="w-4 h-4 text-blue-600" />
      default:
        return <Users className="w-4 h-4 text-gray-600" />
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading competitors...</p>
        </div>
      </div>
    )
  }

  return (
    <>
      {/* Analysis Modal */}
      {analysisData && (
        <AnalysisModal
          isOpen={showAnalysisModal}
          onClose={() => {
            setShowAnalysisModal(false)
            setAnalysisData(null)
          }}
          competitorName={analysisData.competitor_name}
          results={analysisData.analysis_results || []}
          summary={analysisData.summary || ''}
          timestamp={analysisData.timestamp || new Date().toISOString()}
        />
      )}

      <div className="p-4 md:p-8 bg-gray-50 min-h-screen">
        <Toaster position="top-right" />

        {/* Header */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Competitor Monitoring</h1>
            <p className="text-gray-600 mt-2">
              Monitoring {competitors.length} competitors • Last updated: {new Date().toLocaleTimeString()}
            </p>
          </div>
          <div className="flex gap-3 mt-4 md:mt-0">
            <button
              onClick={() => loadCompetitors()}
              className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <RefreshCw className="w-4 h-4" />
              Refresh
            </button>
            <button
              onClick={() => setShowAddForm(true)}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <Plus className="w-4 h-4" />
              Add Competitor
            </button>
          </div>
        </div>

        {/* Analytics Overview */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-sm font-medium text-gray-600">Total Competitors</h3>
            <p className="text-3xl font-bold text-gray-900 mt-2">{competitors.length}</p>
            <div className="mt-4 flex items-center gap-2">
              <span className="text-sm text-green-600 font-medium">↑ 12%</span>
              <span className="text-sm text-gray-500">vs last month</span>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-sm font-medium text-gray-600">Active Monitoring</h3>
            <p className="text-3xl font-bold text-gray-900 mt-2">
              {competitors.filter(c => c.status === 'active').length}
            </p>
            <div className="mt-4">
              <div className="flex justify-between text-sm mb-1">
                <span className="text-gray-600">Activity Rate</span>
                <span className="font-medium">
                  {competitors.length > 0 
                    ? ((competitors.filter(c => c.status === 'active').length / competitors.length) * 100).toFixed(0)
                    : 0}%
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-green-600 h-2 rounded-full"
                  style={{ 
                    width: `${competitors.length > 0 
                      ? (competitors.filter(c => c.status === 'active').length / competitors.length) * 100 
                      : 0}%` 
                  }}
                />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-sm font-medium text-gray-600">Status Distribution</h3>
            {statusChartData.length > 0 ? (
              <>
                <ResponsiveContainer width="100%" height={80}>
                  <PieChart>
                    <Pie
                      data={statusChartData}
                      cx="50%"
                      cy="50%"
                      innerRadius={25}
                      outerRadius={35}
                      paddingAngle={5}
                      dataKey="value"
                    >
                      {statusChartData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                  </PieChart>
                </ResponsiveContainer>
                <div className="mt-2 flex flex-wrap gap-2 text-xs">
                  {statusChartData.map((item, index) => (
                    <span key={item.name} className="flex items-center gap-1">
                      <span className="w-2 h-2 rounded-full" style={{ backgroundColor: COLORS[index % COLORS.length] }} />
                      {item.name}: {item.value}
                    </span>
                  ))}
                </div>
              </>
            ) : (
              <p className="text-sm text-gray-500 mt-4">No data available</p>
            )}
          </div>
        </div>

        {/* Filters */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <div className="flex items-center gap-2 mb-4">
            <Filter className="w-5 h-5 text-gray-600" />
            <h3 className="font-semibold text-gray-900">Filters</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Search</label>
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <input
                  type="text"
                  placeholder="Search competitors..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Status</label>
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="all">All Statuses</option>
                <option value="active">Active</option>
                <option value="monitoring">Monitoring</option>
                <option value="inactive">Inactive</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Industry</label>
              <select
                value={industryFilter}
                onChange={(e) => setIndustryFilter(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="all">All Industries</option>
                {industries.map(industry => (
                  <option key={industry} value={industry}>{industry}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="mt-4 flex items-center justify-between">
            <span className="text-sm text-gray-600">
              Showing {filteredCompetitors.length} of {competitors.length} competitors
            </span>
            <div className="flex gap-2">
              <button
                onClick={() => setViewMode('grid')}
                className={`px-3 py-1 rounded ${viewMode === 'grid' ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-600'}`}
              >
                Grid
              </button>
              <button
                onClick={() => setViewMode('list')}
                className={`px-3 py-1 rounded ${viewMode === 'list' ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-600'}`}
              >
                List
              </button>
            </div>
          </div>
        </div>

        {/* Competitors Grid/List */}
        {filteredCompetitors.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-12 text-center">
            <Users className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">No competitors found</h3>
            <p className="text-gray-600 mb-4">
              {searchQuery ? 'Try adjusting your search' : 'Add your first competitor to get started'}
            </p>
            {!searchQuery && (
              <button
                onClick={() => setShowAddForm(true)}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
              >
                Add Competitor
              </button>
            )}
          </div>
        ) : (
          <div className={viewMode === 'grid' ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6' : 'space-y-4'}>
            {filteredCompetitors.map((competitor, index) => (
              <div
                key={competitor.id}
                className={`bg-white rounded-lg shadow-lg hover:shadow-xl transition-all p-6 ${
                  index < 3 ? 'border-l-4 ' + (
                    index === 0 ? 'border-red-500' :
                    index === 1 ? 'border-yellow-500' :
                    'border-green-500'
                  ) : ''
                }`}
              >
                {index < 3 && (
                  <div className="mb-3">
                    <span className={`inline-flex items-center gap-1 px-2 py-1 rounded text-xs font-medium ${
                      index === 0 ? 'bg-red-100 text-red-700' :
                      index === 1 ? 'bg-yellow-100 text-yellow-700' :
                      'bg-green-100 text-green-700'
                    }`}>
                      <AlertTriangle className="w-3 h-3" />
                      {index === 0 ? 'HIGH PRIORITY (Today)' : index === 1 ? 'Product Launch' : 'Recent Activity'}
                    </span>
                  </div>
                )}

                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center text-white font-bold text-lg">
                      {competitor.name.charAt(0)}
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900 text-lg">{competitor.name}</h3>
                      <p className="text-sm text-gray-500">{competitor.industry}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-1">
                    {getStatusIcon(competitor.status)}
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(competitor.status)}`}>
                      {competitor.status}
                    </span>
                  </div>
                </div>

                {competitor.description && (
                  <p className="text-sm text-gray-600 mb-4 line-clamp-2">{competitor.description}</p>
                )}

                <div className="space-y-2 mb-4">
                  {competitor.website && (
                    <div className="flex items-center gap-2 text-sm text-gray-600">
                      <Globe className="w-4 h-4" />
                      <a 
                        href={competitor.website} 
                        target="_blank" 
                        rel="noopener noreferrer" 
                        className="hover:text-blue-600 truncate"
                      >
                        {competitor.website}
                      </a>
                    </div>
                  )}
                  {competitor.headquarters && (
                    <div className="flex items-center gap-2 text-sm text-gray-600">
                      <MapPin className="w-4 h-4" />
                      {competitor.headquarters}
                    </div>
                  )}
                  {competitor.employee_count && (
                    <div className="flex items-center gap-2 text-sm text-gray-600">
                      <Users className="w-4 h-4" />
                      {competitor.employee_count.toLocaleString()} employees
                    </div>
                  )}
                  {competitor.founded_year && (
                    <div className="flex items-center gap-2 text-sm text-gray-600">
                      <Building2 className="w-4 h-4" />
                      Founded {competitor.founded_year}
                    </div>
                  )}
                </div>

                {index < 3 && (
                  <div className="mb-4 p-3 bg-gray-50 rounded">
                    <p className="text-xs text-gray-700">
                      {index === 0 && '• New blog post on AI and fraud detection'}
                      {index === 1 && '• Malke page updated (9 hours ago)'}
                      {index === 2 && '• Webinar scheduled (Tomorrow)'}
                    </p>
                    <p className="text-xs text-gray-500 mt-1">
                      {new Date(competitor.updated_at).toLocaleString()}
                    </p>
                  </div>
                )}

                <div className="flex gap-2">
                  <button
                    onClick={() => handleAnalyze(competitor.id, competitor.name)}
                    className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
                  >
                    Analyze
                  </button>
                  <button className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors text-sm font-medium">
                    View Details
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Add Competitor Modal */}
        {showAddForm && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
              <div className="p-6">
                <h2 className="text-2xl font-bold text-gray-900 mb-6">Add New Competitor</h2>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Name *</label>
                    <input
                      type="text"
                      value={newCompetitor.name}
                      onChange={(e) => setNewCompetitor({ ...newCompetitor, name: e.target.value })}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Company name"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Industry *</label>
                    <input
                      type="text"
                      value={newCompetitor.industry}
                      onChange={(e) => setNewCompetitor({ ...newCompetitor, industry: e.target.value })}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="e.g., Marketing Technology"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Website</label>
                    <input
                      type="url"
                      value={newCompetitor.website}
                      onChange={(e) => setNewCompetitor({ ...newCompetitor, website: e.target.value })}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="https://example.com"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Description</label>
                    <textarea
                      value={newCompetitor.description}
                      onChange={(e) => setNewCompetitor({ ...newCompetitor, description: e.target.value })}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      rows={3}
                      placeholder="Brief description of the company"
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Founded Year</label>
                      <input
                        type="number"
                        value={newCompetitor.founded_year || ''}
                        onChange={(e) => setNewCompetitor({ ...newCompetitor, founded_year: parseInt(e.target.value) || undefined })}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="2020"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Employee Count</label>
                      <input
                        type="number"
                        value={newCompetitor.employee_count || ''}
                        onChange={(e) => setNewCompetitor({ ...newCompetitor, employee_count: parseInt(e.target.value) || undefined })}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="100"
                      />
                    </div>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Headquarters</label>
                    <input
                      type="text"
                      value={newCompetitor.headquarters}
                      onChange={(e) => setNewCompetitor({ ...newCompetitor, headquarters: e.target.value })}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="San Francisco, CA"
                    />
                  </div>
                </div>
                <div className="flex gap-3 mt-6">
                  <button
                    onClick={handleAddCompetitor}
                    className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                  >
                    Add Competitor
                  </button>
                  <button
                    onClick={() => setShowAddForm(false)}
                    className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </>
  )
}