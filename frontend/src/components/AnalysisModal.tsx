'use client'

import { X, CheckCircle, AlertCircle } from 'lucide-react'

interface AnalysisResult {
  question: string
  answer: string
  sources: any[]
  confidence: number
}

interface AnalysisModalProps {
  isOpen: boolean
  onClose: () => void
  competitorName: string
  results: AnalysisResult[]
  summary: string
  timestamp: string
}

export default function AnalysisModal({
  isOpen,
  onClose,
  competitorName,
  results,
  summary,
  timestamp
}: AnalysisModalProps) {
  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4">
      <div className="bg-white rounded-xl shadow-2xl max-w-5xl w-full max-h-[90vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 to-indigo-600 px-6 py-4 flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-white">
              Automated Analysis: {competitorName}
            </h2>
            <p className="text-blue-100 text-sm mt-1">
              {new Date(timestamp).toLocaleString()}
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-white hover:bg-white hover:bg-opacity-20 rounded-full p-2 transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Summary Banner */}
        <div className="bg-blue-50 border-b border-blue-100 px-6 py-4">
          <div className="flex items-start gap-3">
            <CheckCircle className="w-6 h-6 text-green-600 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold text-gray-900">Analysis Complete</h3>
              <p className="text-gray-700 text-sm mt-1">{summary}</p>
            </div>
          </div>
        </div>

        {/* Results Content */}
        <div className="flex-1 overflow-y-auto px-6 py-6">
          <div className="space-y-6">
            {results.map((result, index) => (
              <div
                key={index}
                className="bg-gray-50 rounded-lg p-5 border border-gray-200 hover:shadow-md transition-shadow"
              >
                {/* Question */}
                <div className="flex items-start gap-3 mb-4">
                  <div className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold flex-shrink-0">
                    {index + 1}
                  </div>
                  <div className="flex-1">
                    <h4 className="font-semibold text-gray-900 text-lg">
                      {result.question}
                    </h4>
                  </div>
                  {result.confidence && (
                    <div className="flex items-center gap-1 bg-white px-3 py-1 rounded-full border border-gray-300">
                      <AlertCircle className="w-4 h-4 text-gray-600" />
                      <span className="text-sm font-medium text-gray-700">
                        {(result.confidence * 100).toFixed(0)}%
                      </span>
                    </div>
                  )}
                </div>

                {/* Answer */}
                <div className="ml-11 space-y-3">
                  <div className="bg-white rounded-lg p-4 border border-gray-200">
                    <p className="text-gray-800 leading-relaxed whitespace-pre-wrap">
                      {result.answer}
                    </p>
                  </div>

                  {/* Sources */}
                  {result.sources && result.sources.length > 0 && (
                    <div className="bg-blue-50 rounded-lg p-3 border border-blue-100">
                      <p className="text-xs font-semibold text-gray-700 mb-2">
                        Sources ({result.sources.length}):
                      </p>
                      <div className="space-y-1">
                        {result.sources.map((source, idx) => (
                          <div key={idx} className="text-xs text-gray-600">
                            • {source.title || source.type || 'Source'}
                            {source.relevance && (
                              <span className="text-blue-600 ml-1">
                                ({(source.relevance * 100).toFixed(0)}% relevant)
                              </span>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Footer */}
        <div className="border-t border-gray-200 px-6 py-4 bg-gray-50">
          <div className="flex items-center justify-between">
            <p className="text-sm text-gray-600">
              {results.length} questions analyzed
            </p>
            <button
              onClick={onClose}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
