import { Trend } from '@/types'
import { TrendingUp, TrendingDown } from 'lucide-react'

interface TrendCardProps {
  trend: Trend
}

export default function TrendCard({ trend }: TrendCardProps) {
  const isGrowing = trend.status === 'growing' || trend.status === 'emerging'

  return (
    <div className="p-4 rounded-lg border border-gray-200 hover:border-primary-500 transition-colors">
      <div className="flex items-start justify-between mb-2">
        <h3 className="font-semibold text-gray-900">{trend.title}</h3>
        {isGrowing ? (
          <TrendingUp className="w-5 h-5 text-green-600" />
        ) : (
          <TrendingDown className="w-5 h-5 text-red-600" />
        )}
      </div>
      <p className="text-sm text-gray-600 mb-3 line-clamp-2">{trend.description}</p>
      <div className="flex items-center justify-between">
        <div className="flex flex-wrap gap-1">
          {trend.keywords.slice(0, 3).map((keyword, i) => (
            <span key={i} className="text-xs px-2 py-1 bg-gray-100 text-gray-700 rounded">
              {keyword}
            </span>
          ))}
        </div>
        <span className="text-xs text-gray-500">{(trend.confidence_score * 100).toFixed(0)}%</span>
      </div>
    </div>
  )
}
