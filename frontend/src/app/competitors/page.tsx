'use client'

import { useState, useEffect } from 'react'
import { apiClient } from '@/lib/api'
import { Competitor } from '@/types'
import { Users, Search, Building2, MapPin, Globe, Plus } from 'lucide-react'
import toast from 'react-hot-toast'

export default function CompetitorsPage() {
  const [competitors, setCompetitors] = useState<Competitor[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<string>('all')
  const [searchQuery, setSearchQuery] = useState('')
  const [showAddForm, setShowAddForm] = useState(false)
  const [newCompetitor, setNewCompetitor] = useState({
    name: '',
    website: '',
    industry: '',
    description: ''
  })

  useEffect(() => {
    loadCompetitors()
  }, [filter])

  const loadCompetitors = async () => {
    try {
      setLoading(true)
      const filters: any = {}
      if (filter !== 'all') {
        filters.status = filter
      }
      const data = await apiClient.getCompetitors(filters)
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
      setNewCompetitor({ name: '', website: '', industry: '', description: '' })
      loadCompetitors()
    } catch (error) {
      console.error('Error adding competitor:', error)
      toast.error('Failed to add competitor')
    }
  }

  const handleAnalyze = async (id: string, name: string) => {
    try {
      toast.loading(`Analyzing ${name}...`)
      await apiClient.analyzeCompetitor(id)
      toast.dismiss()
      toast.success('Analysis complete!')
      loadCompetitors()
    } catch (error) {
      toast.dismiss()
      console.error('Error analyzing competitor:', error)
      toast.error('Failed to analyze competitor')
    }
  }

  const filteredCompetitors = competitors.filter(competitor =>
    competitor.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    competitor.industry.toLowerCase().includes(searchQuery.toLowerCase()) ||
    (competitor.description && competitor.description.toLowerCase().includes(searchQuery.toLowerCase()))
  )

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

  return (
    <div className="p-8">
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Competitors</h1>
            <p className="text-gray-600 mt-2">Track and analyze your competition</p>
          </div>
          <button
            onClick={() => setShowAddForm(!showAddForm)}
            className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
          >
            <Plus className="w-5 h-5" />
            Add Competitor
          </button>
        </div>
      </div>

      {/* Add Competitor Form */}
      {showAddForm && (
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h3 className="text-lg font-semibold mb-4">Add New Competitor</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <input
              type="text"
              placeholder="Company Name *"
              value={newCompetitor.name}
              onChange={(e) => setNewCompetitor({ ...newCompetitor, name: e.target.value })}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
            <input
              type="text"
              placeholder="Website"
              value={newCompetitor.website}
              onChange={(e) => setNewCompetitor({ ...newCompetitor, website: e.target.value })}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
            <input
              type="text"
              placeholder="Industry *"
              value={newCompetitor.industry}
              onChange={(e) => setNewCompetitor({ ...newCompetitor, industry: e.target.value })}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
            <input
              type="text"
              placeholder="Description"
              value={newCompetitor.description}
              onChange={(e) => setNewCompetitor({ ...newCompetitor, description: e.target.value })}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>
          <div className="flex gap-2 mt-4">
            <button
              onClick={handleAddCompetitor}
              className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
            >
              Add Competitor
            </button>
            <button
              onClick={() => setShowAddForm(false)}
              className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
            >
              Cancel
            </button>
          </div>
        </div>
      )}

      {/* Filters */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                placeholder="Search competitors..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>
          </div>
          <div className="flex gap-2">
            {['all', 'active', 'monitoring', 'inactive'].map((status) => (
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

      {/* Competitors Grid */}
      {loading ? (
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading competitors...</p>
          </div>
        </div>
      ) : filteredCompetitors.length === 0 ? (
        <div className="bg-white rounded-lg shadow p-12 text-center">
          <Users className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-gray-900 mb-2">No competitors found</h3>
          <p className="text-gray-600 mb-4">
            {searchQuery ? 'Try adjusting your search' : 'Add your first competitor to get started'}
          </p>
          {!searchQuery && (
            <button
              onClick={() => setShowAddForm(true)}
              className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
            >
              Add Competitor
            </button>
          )}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredCompetitors.map((competitor) => (
            <div key={competitor.id} className="bg-white rounded-lg shadow hover:shadow-lg transition-shadow p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-2">
                  <Building2 className="w-5 h-5 text-primary-600" />
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(competitor.status)}`}>
                    {competitor.status}
                  </span>
                </div>
                <div className="text-sm text-gray-500">
                  Score: {(competitor.monitoring_score * 100).toFixed(0)}
                </div>
              </div>

              <h3 className="text-lg font-semibold text-gray-900 mb-2">{competitor.name}</h3>

              {competitor.description && (
                <p className="text-gray-600 text-sm mb-4 line-clamp-2">{competitor.description}</p>
              )}

              <div className="space-y-2 mb-4">
                <div className="flex items-center gap-2 text-sm text-gray-600">
                  <Building2 className="w-4 h-4" />
                  <span>{competitor.industry}</span>
                </div>
                {competitor.website && (
                  <div className="flex items-center gap-2 text-sm text-gray-600">
                    <Globe className="w-4 h-4" />
                    <a
                      href={competitor.website}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="hover:text-primary-600 truncate"
                    >
                      {competitor.website}
                    </a>
                  </div>
                )}
                {competitor.headquarters && (
                  <div className="flex items-center gap-2 text-sm text-gray-600">
                    <MapPin className="w-4 h-4" />
                    <span>{competitor.headquarters}</span>
                  </div>
                )}
              </div>

              <button
                onClick={() => handleAnalyze(competitor.id, competitor.name)}
                className="w-full px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 text-sm"
              >
                Analyze
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
