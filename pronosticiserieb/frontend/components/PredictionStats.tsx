interface PredictionStatsProps {
  stats: {
    totalPredictions: number
    accuracy: number
    activeSubscribers: number
  }
}

export function PredictionStats({ stats }: PredictionStatsProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
      <div className="bg-gray-800 rounded-xl p-6">
        <div className="text-3xl font-bold text-white">
          {stats.totalPredictions}
        </div>
        <div className="text-gray-400 text-sm">
          Pronostici Totali
        </div>
      </div>

      <div className="bg-gray-800 rounded-xl p-6">
        <div className="text-3xl font-bold text-green-400">
          {stats.accuracy}%
        </div>
        <div className="text-gray-400 text-sm">
          Accuratezza
        </div>
      </div>

      <div className="bg-gray-800 rounded-xl p-6">
        <div className="text-3xl font-bold text-blue-400">
          {stats.activeSubscribers.toLocaleString()}
        </div>
        <div className="text-gray-400 text-sm">
          Iscritti Attivi
        </div>
      </div>
    </div>
  )
}
