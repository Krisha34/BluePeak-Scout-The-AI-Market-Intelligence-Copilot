'use client'

import { useState, useEffect } from 'react'
import { apiClient } from '@/lib/api'
import { Report } from '@/types'
import { FileText, Download, Plus, Loader2 } from 'lucide-react'
import toast from 'react-hot-toast'

export default function ReportsPage() {
  const [reports, setReports] = useState<Report[]>([])
  const [loading, setLoading] = useState(true)
  const [generating, setGenerating] = useState(false)
  const [selectedReport, setSelectedReport] = useState<Report | null>(null)

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

  const generateReport = async () => {
    try {
      setGenerating(true)
      toast.loading('Generating report...', { id: 'generate' })
      const result = await apiClient.generateReport({
        report_type: 'comprehensive',
        industry: 'technology'
      })
      toast.success('Report generated successfully', { id: 'generate' })
      loadReports()
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

  const exportReport = async (reportId: string, format: string) => {
    try {
      toast.loading('Exporting report...', { id: 'export' })
      await apiClient.exportReport(reportId, format)
      toast.success('Report exported successfully', { id: 'export' })
    } catch (error) {
      console.error('Error exporting report:', error)
      toast.error('Failed to export report', { id: 'export' })
    }
  }

  if (selectedReport) {
    return (
      <div className="p-8">
        <div className="mb-6">
          <button
            onClick={() => setSelectedReport(null)}
            className="text-primary-600 hover:text-primary-700 font-medium"
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
                onClick={() => exportReport(selectedReport.id, 'pdf')}
                className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 flex items-center gap-2"
              >
                <Download className="w-4 h-4" />
                Export PDF
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
    <div className="p-8">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Reports</h1>
          <p className="text-gray-600 mt-2">AI-generated intelligence reports</p>
        </div>
        <button
          onClick={generateReport}
          disabled={generating}
          className="px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 flex items-center gap-2"
        >
          {generating ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Generating...
            </>
          ) : (
            <>
              <Plus className="w-5 h-5" />
              Generate New Report
            </>
          )}
        </button>
      </div>

      {loading ? (
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading reports...</p>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {reports.map((report) => (
            <div
              key={report.id}
              onClick={() => viewReport(report)}
              className="bg-white rounded-lg shadow hover:shadow-lg transition-shadow p-6 cursor-pointer"
            >
              <div className="flex items-start gap-4">
                <div className="p-3 bg-primary-100 rounded-lg">
                  <FileText className="w-6 h-6 text-primary-600" />
                </div>
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">{report.title}</h3>
                  <p className="text-sm text-gray-600 line-clamp-3 mb-4">{report.summary}</p>
                  <div className="flex items-center justify-between text-xs text-gray-500">
                    <span className="capitalize">{report.report_type}</span>
                    <span>{new Date(report.created_at).toLocaleDateString()}</span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {!loading && reports.length === 0 && (
        <div className="text-center py-12">
          <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-gray-700 mb-2">No reports yet</h3>
          <p className="text-gray-500 mb-6">Generate your first AI-powered intelligence report</p>
          <button
            onClick={generateReport}
            className="px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 inline-flex items-center gap-2"
          >
            <Plus className="w-5 h-5" />
            Generate Report
          </button>
        </div>
      )}
    </div>
  )
}
