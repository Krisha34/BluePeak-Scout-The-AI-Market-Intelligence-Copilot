import { Competitor } from '@/types'
import { Building, ExternalLink } from 'lucide-react'

interface CompetitorCardProps {
  competitor: Competitor
}

export default function CompetitorCard({ competitor }: CompetitorCardProps) {
  return (
    <div className="flex items-center gap-4 p-4 rounded-lg border border-gray-200 hover:border-primary-500 transition-colors">
      <div className="p-3 bg-gray-100 rounded-lg">
        <Building className="w-6 h-6 text-gray-600" />
      </div>
      <div className="flex-1">
        <div className="flex items-center gap-2">
          <h3 className="font-semibold text-gray-900">{competitor.name}</h3>
          {competitor.website && (
            <a href={competitor.website} target="_blank" rel="noopener noreferrer">
              <ExternalLink className="w-4 h-4 text-gray-400 hover:text-primary-600" />
            </a>
          )}
        </div>
        <p className="text-sm text-gray-600 mt-1">{competitor.industry}</p>
        <div className="flex items-center gap-4 mt-2">
          <span className={`text-xs px-2 py-1 rounded-full ${
            competitor.status === 'active' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'
          }`}>
            {competitor.status}
          </span>
          <span className="text-xs text-gray-500">
            Score: {(competitor.monitoring_score * 100).toFixed(0)}%
          </span>
        </div>
      </div>
    </div>
  )
}
