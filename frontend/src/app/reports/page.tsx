'use client'

import { useState, useEffect } from 'react'
import { apiClient } from '@/lib/api'
import { Report } from '@/types'
import { FileText, Download, Loader2, User, Settings, Share2, X, Image, FileCode, Linkedin } from 'lucide-react'
import toast from 'react-hot-toast'

type ReportType = 'weekly_digest' | 'full_market' | 'competitor_deep_dive' | 'custom_query'
type FocusArea = 'ai_features' | 'pricing_strategies' | 'content_marketing' | 'product_launches'
type DateRange = 'last_7_days' | 'last_30_days' | 'last_90_days' | 'last_year'

export default function ReportsPage() {
  const [reports, setReports] = useState<Report[]>([])
  const [loading, setLoading] = useState(true)
  const [generating, setGenerating] = useState(false)
  const [selectedReport, setSelectedReport] = useState<Report | null>(null)
  const [shareModalReport, setShareModalReport] = useState<Report | null>(null)

  // Report generation form state
  const [reportType, setReportType] = useState<ReportType>('full_market')
  const [focusAreas, setFocusAreas] = useState<FocusArea[]>(['ai_features', 'pricing_strategies'])
  const [dateRange, setDateRange] = useState<DateRange>('last_30_days')

  useEffect(() => {
    loadReports()
  }, [])

  const loadReports = async () => {
    try {
      setLoading(true)
      const data = await apiClient.getReports()
      setReports(data)
    } catch (error) {
      console.error('Error loading reports:', error)
      toast.error('Failed to load reports')
    } finally {
      setLoading(false)
    }
  }

  const toggleFocusArea = (area: FocusArea) => {
    setFocusAreas(prev =>
      prev.includes(area)
        ? prev.filter(a => a !== area)
        : [...prev, area]
    )
  }

  const getReportTypeLabel = (type: ReportType) => {
    const labels = {
      weekly_digest: 'Weekly Competitive Digest',
      full_market: 'Full Market Analysis',
      competitor_deep_dive: 'Competitor Deep Dive',
      custom_query: 'Custom Research Query'
    }
    return labels[type]
  }

  const getFocusAreaLabel = (area: FocusArea) => {
    const labels = {
      ai_features: 'AI Features',
      pricing_strategies: 'Pricing Strategies',
      content_marketing: 'Content Marketing',
      product_launches: 'Product Launches'
    }
    return labels[area]
  }

  const getDateRangeLabel = (range: DateRange) => {
    const labels = {
      last_7_days: 'Last 7 Days',
      last_30_days: 'Last 30 Days',
      last_90_days: 'Last 90 Days',
      last_year: 'Last Year'
    }
    return labels[range]
  }

  const getPreviewText = () => {
    const focusText = focusAreas.length > 0
      ? focusAreas.map(getFocusAreaLabel).join(' and ')
      : 'all areas'
    return `${getReportTypeLabel(reportType)} covering ${focusText} from the ${getDateRangeLabel(dateRange).toLowerCase()}`
  }

  const generateReport = async () => {
    try {
      setGenerating(true)
      toast.loading('Generating comprehensive report...', { id: 'generate' })

      const result = await apiClient.generateReport({
        report_type: reportType,
        focus_areas: focusAreas,
        date_range: dateRange
      })

      toast.success('Report generated successfully! (~60 seconds)', { id: 'generate' })
      await loadReports()
    } catch (error) {
      console.error('Error generating report:', error)
      toast.error('Failed to generate report', { id: 'generate' })
    } finally {
      setGenerating(false)
    }
  }

  const viewReport = (report: Report) => {
    setSelectedReport(report)
  }

  const downloadReport = async (reportId: string, reportTitle: string) => {
    try {
      toast.loading('Downloading report...', { id: 'download' })
      await apiClient.exportReport(reportId, 'pdf')
      toast.success('Report downloaded!', { id: 'download' })
    } catch (error) {
      console.error('Error downloading report:', error)
      toast.error('Failed to download report', { id: 'download' })
    }
  }

  const exportAsPDF = (reportId: string) => {
    const url = `http://localhost:8000/api/v1/social-sharing/${reportId}/export/pdf`
    window.open(url, '_blank')
    toast.success('Opening PDF export...')
  }

  const exportAsLinkedInArticle = (reportId: string) => {
    const url = `http://localhost:8000/api/v1/social-sharing/${reportId}/export/linkedin-article`
    window.open(url, '_blank')
    toast.success('Opening LinkedIn article...')
  }

  const exportAsSocialImage = (reportId: string, template: 'stat' | 'insight') => {
    const url = `http://localhost:8000/api/v1/social-sharing/${reportId}/export/social-image?template=${template}`
    window.open(url, '_blank')
    toast.success('Opening social media image...')
  }

  const copyLinkedInArticleURL = (reportId: string) => {
    const url = `http://localhost:8000/api/v1/social-sharing/${reportId}/export/linkedin-article`
    navigator.clipboard.writeText(url)
    toast.success('LinkedIn article URL copied!')
  }

  // Share Modal Component
  const ShareModal = ({ report }: { report: Report }) => (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-3">
              <Share2 className="w-6 h-6 text-blue-600" />
              <h2 className="text-2xl font-bold text-gray-900">Share Report</h2>
            </div>
            <button
              onClick={() => setShareModalReport(null)}
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <X className="w-5 h-5 text-gray-500" />
            </button>
          </div>

          <div className="mb-6">
            <h3 className="font-semibold text-gray-900 mb-2">{report.title}</h3>
            <p className="text-sm text-gray-600">
              Generated on {new Date(report.created_at).toLocaleDateString()}
            </p>
          </div>

          <div className="space-y-4">
            {/* PDF Export */}
            <div className="border border-gray-200 rounded-lg p-4 hover:border-blue-500 transition-colors">
              <div className="flex items-start justify-between">
                <div className="flex items-start gap-3">
                  <div className="p-2 bg-red-100 rounded-lg">
                    <FileText className="w-5 h-5 text-red-600" />
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-1">PDF Report</h4>
                    <p className="text-sm text-gray-600 mb-3">
                      Professional PDF with charts, insights, and analytics
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => exportAsPDF(report.id)}
                  className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 text-sm font-medium"
                >
                  Download
                </button>
              </div>
            </div>

            {/* LinkedIn Article */}
            <div className="border border-gray-200 rounded-lg p-4 hover:border-blue-500 transition-colors">
              <div className="flex items-start justify-between">
                <div className="flex items-start gap-3">
                  <div className="p-2 bg-blue-100 rounded-lg">
                    <Linkedin className="w-5 h-5 text-blue-700" />
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-1">LinkedIn Article</h4>
                    <p className="text-sm text-gray-600 mb-3">
                      HTML formatted article with embedded charts for LinkedIn
                    </p>
                  </div>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => copyLinkedInArticleURL(report.id)}
                    className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 text-sm font-medium"
                  >
                    Copy URL
                  </button>
                  <button
                    onClick={() => exportAsLinkedInArticle(report.id)}
                    className="px-4 py-2 bg-blue-700 text-white rounded-lg hover:bg-blue-800 text-sm font-medium"
                  >
                    Open
                  </button>
                </div>
              </div>
            </div>

            {/* Social Media Images */}
            <div className="border border-gray-200 rounded-lg p-4 hover:border-blue-500 transition-colors">
              <div className="flex items-start gap-3 mb-3">
                <div className="p-2 bg-green-100 rounded-lg">
                  <Image className="w-5 h-5 text-green-600" />
                </div>
                <div>
                  <h4 className="font-semibold text-gray-900 mb-1">Social Media Images</h4>
                  <p className="text-sm text-gray-600">
                    Shareable images optimized for LinkedIn, Facebook (1200x627px)
                  </p>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3 mt-3 pl-11">
                <button
                  onClick={() => exportAsSocialImage(report.id, 'stat')}
                  className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 text-sm font-medium"
                >
                  Stat Card
                </button>
                <button
                  onClick={() => exportAsSocialImage(report.id, 'insight')}
                  className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 text-sm font-medium"
                >
                  Insight Card
                </button>
              </div>
            </div>

            {/* Info Box */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <p className="text-sm text-blue-800">
                <strong>Tip:</strong> All exports are generated from your existing data with real-time sentiment analysis and industry distribution charts.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )

  if (selectedReport) {
    return (
      <div className="p-8">
        <div className="mb-6">
          <button
            onClick={() => setSelectedReport(null)}
            className="text-blue-600 hover:text-blue-700 font-medium"
          >
            ← Back to reports
          </button>
        </div>

        <div className="bg-white rounded-lg shadow p-8">
          <div className="flex items-start justify-between mb-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">{selectedReport.title}</h1>
              <p className="text-gray-600">
                Generated on {new Date(selectedReport.created_at).toLocaleDateString()}
              </p>
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => setShareModalReport(selectedReport)}
                className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 flex items-center gap-2"
              >
                <Share2 className="w-4 h-4" />
                Share
              </button>
              <button
                onClick={() => downloadReport(selectedReport.id, selectedReport.title)}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center gap-2"
              >
                <Download className="w-4 h-4" />
                Download PDF
              </button>
            </div>
          </div>

          <div className="border-t pt-6">
            <div className="prose max-w-none">
              <div className="bg-blue-50 border-l-4 border-blue-500 p-4 mb-6">
                <h3 className="text-lg font-semibold text-blue-900 mb-2">Executive Summary</h3>
                <p className="text-blue-800">{selectedReport.summary}</p>
              </div>

              <div className="whitespace-pre-wrap text-gray-700">
                {selectedReport.content}
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-slate-800 to-slate-900 px-8 py-6 shadow-lg">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-blue-500 rounded-lg flex items-center justify-center">
              <FileText className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white">Report Generation</h1>
              <p className="text-gray-300 text-sm">AI-Powered Market Intelligence Platform</p>
            </div>
          </div>
          <div className="flex gap-4 items-center">
            <button className="flex items-center gap-2 text-white hover:text-gray-200">
              <User className="w-5 h-5" />
              <span className="text-sm">[Profile]</span>
            </button>
            <button className="text-white hover:text-gray-200">
              <Settings className="w-6 h-6" />
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto p-8">
        {/* Main Description */}
        <div className="mb-8">
          <p className="text-lg text-gray-700">
            Generate comprehensive intelligence reports automatically
          </p>
        </div>

        {/* Report Generation Form */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          {/* Report Type */}
          <div className="mb-8">
            <div className="flex items-center gap-2 mb-4">
              <FileText className="w-5 h-5 text-gray-600" />
              <h3 className="text-lg font-semibold text-gray-900">Report Type</h3>
            </div>
            <div className="space-y-3">
              {(['weekly_digest', 'full_market', 'competitor_deep_dive', 'custom_query'] as ReportType[]).map((type) => (
                <label key={type} className="flex items-center gap-3 cursor-pointer">
                  <input
                    type="radio"
                    name="reportType"
                    checked={reportType === type}
                    onChange={() => setReportType(type)}
                    className="w-4 h-4 text-blue-600"
                  />
                  <span className="text-gray-700">{getReportTypeLabel(type)}</span>
                </label>
              ))}
            </div>
          </div>

          <div className="border-t my-6"></div>

          {/* Focus Areas */}
          <div className="mb-8">
            <div className="flex items-center gap-2 mb-4">
              <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              <h3 className="text-lg font-semibold text-gray-900">Focus Areas (Optional)</h3>
            </div>
            <div className="grid grid-cols-2 gap-4">
              {(['ai_features', 'pricing_strategies', 'content_marketing', 'product_launches'] as FocusArea[]).map((area) => (
                <label key={area} className="flex items-center gap-3 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={focusAreas.includes(area)}
                    onChange={() => toggleFocusArea(area)}
                    className="w-4 h-4 text-blue-600 rounded"
                  />
                  <span className="text-gray-700">{getFocusAreaLabel(area)}</span>
                </label>
              ))}
            </div>
          </div>

          <div className="border-t my-6"></div>

          {/* Date Range */}
          <div className="mb-8">
            <div className="flex items-center gap-2 mb-4">
              <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <h3 className="text-lg font-semibold text-gray-900">Date Range</h3>
            </div>
            <select
              value={dateRange}
              onChange={(e) => setDateRange(e.target.value as DateRange)}
              className="w-full md:w-64 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="last_7_days">Last 7 Days</option>
              <option value="last_30_days">Last 30 Days</option>
              <option value="last_90_days">Last 90 Days</option>
              <option value="last_year">Last Year</option>
            </select>
          </div>

          <div className="border-t my-6"></div>

          {/* Preview */}
          <div className="bg-gray-50 rounded-lg p-4 mb-6">
            <p className="text-gray-900 mb-2">{getPreviewText()}</p>
            <p className="text-sm text-gray-600">Estimated generation time: ~60 seconds</p>
          </div>

          {/* Generate Button */}
          <div className="flex justify-center">
            <button
              onClick={generateReport}
              disabled={generating}
              className="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 font-medium text-lg"
            >
              {generating ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Generating Report...
                </>
              ) : (
                'Generate PDF Report'
              )}
            </button>
          </div>
        </div>

        {/* Recent Reports */}
        <div className="bg-white rounded-lg shadow-lg p-8">
          <div className="flex items-center gap-2 mb-6">
            <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <h3 className="text-lg font-semibold text-gray-900">Recent Reports</h3>
          </div>

          {loading ? (
            <div className="flex items-center justify-center py-12">
              <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
            </div>
          ) : reports.length === 0 ? (
            <div className="text-center py-12">
              <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-600">No reports generated yet</p>
            </div>
          ) : (
            <div className="space-y-3">
              {reports.slice(0, 10).map((report) => (
                <div
                  key={report.id}
                  className="flex items-center justify-between p-4 bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors cursor-pointer"
                  onClick={() => viewReport(report)}
                >
                  <div className="flex items-center gap-3 flex-1">
                    <FileText className="w-5 h-5 text-gray-600" />
                    <div>
                      <h4 className="font-medium text-gray-900">{report.title}</h4>
                      <p className="text-sm text-gray-500">
                        {new Date(report.created_at).toLocaleDateString('en-US', {
                          year: 'numeric',
                          month: 'short',
                          day: 'numeric'
                        })}
                      </p>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        setShareModalReport(report)
                      }}
                      className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-sm flex items-center gap-2"
                    >
                      <Share2 className="w-4 h-4" />
                      Share
                    </button>
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        downloadReport(report.id, report.title)
                      }}
                      className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm flex items-center gap-2"
                    >
                      <Download className="w-4 h-4" />
                      Download
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Share Modal */}
      {shareModalReport && <ShareModal report={shareModalReport} />}
    </div>
  )
}
