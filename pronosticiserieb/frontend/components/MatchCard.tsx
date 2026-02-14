'use client'

import { Match } from '@/types/match'

interface MatchCardProps {
  match: Match
}

export function MatchCard({ match }: MatchCardProps) {
  const getOutcomeColor = (outcome: string) => {
    switch (outcome) {
      case 'home': return 'text-green-400'
      case 'draw': return 'text-yellow-400'
      case 'away': return 'text-red-400'
      default: return 'text-gray-400'
    }
  }

  const getOutcomeText = (outcome: string) => {
    switch (outcome) {
      case 'home': return '1'
      case 'draw': return 'X'
      case 'away': return '2'
      default: return '-'
    }
  }

  return (
    <div className="bg-gray-800 rounded-xl p-6 border border-gray-700 hover:border-blue-500 transition">
      {/* Teams */}
      <div className="text-center mb-4">
        <div className="text-lg font-bold text-white">
          {match.homeTeam} vs {match.awayTeam}
        </div>
        <div className="text-sm text-gray-400">
          {new Date(match.date).toLocaleDateString('it-IT', {
            weekday: 'short',
            day: 'numeric',
            month: 'short',
            hour: '2-digit',
            minute: '2-digit'
          })}
        </div>
      </div>

      {/* Prediction */}
      {match.prediction && (
        <div className="space-y-3">
          {/* Probabilities */}
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-gray-400">1</span>
              <div className="flex-1 mx-3 bg-gray-700 rounded-full h-2 overflow-hidden">
                <div
                  className="bg-green-500 h-full rounded-full"
                  style={{ width: `${match.prediction.homeWin}%` }}
                />
              </div>
              <span className="text-white font-semibold">{match.prediction.homeWin}%</span>
            </div>

            <div className="flex justify-between text-sm">
              <span className="text-gray-400">X</span>
              <div className="flex-1 mx-3 bg-gray-700 rounded-full h-2 overflow-hidden">
                <div
                  className="bg-yellow-500 h-full rounded-full"
                  style={{ width: `${match.prediction.draw}%` }}
                />
              </div>
              <span className="text-white font-semibold">{match.prediction.draw}%</span>
            </div>

            <div className="flex justify-between text-sm">
              <span className="text-gray-400">2</span>
              <div className="flex-1 mx-3 bg-gray-700 rounded-full h-2 overflow-hidden">
                <div
                  className="bg-red-500 h-full rounded-full"
                  style={{ width: `${match.prediction.awayWin}%` }}
                />
              </div>
              <span className="text-white font-semibold">{match.prediction.awayWin}%</span>
            </div>
          </div>

          {/* Recommendation */}
          <div className="pt-3 border-t border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-xs text-gray-400">Consigliato</div>
                <div className={`text-2xl font-bold ${getOutcomeColor(match.prediction.recommended)}`}>
                  {getOutcomeText(match.prediction.recommended)}
                </div>
              </div>
              <div className="text-right">
                <div className="text-xs text-gray-400">Confidenza</div>
                <div className="text-lg font-bold text-white">{match.prediction.confidence}%</div>
              </div>
            </div>
            {match.prediction.valueBet && (
              <div className="mt-2 text-xs bg-green-900 text-green-300 px-2 py-1 rounded inline-block">
                💰 Value Bet
              </div>
            )}
          </div>

          {/* Reasoning */}
          {match.prediction.reasoning && (
            <div className="text-xs text-gray-400 mt-2">
              {match.prediction.reasoning}
            </div>
          )}
        </div>
      )}

      {/* CTA */}
      <a
        href={`/partita/${match.id}`}
        className="mt-4 block text-center w-full py-2 bg-blue-600 text-white rounded-lg text-sm font-semibold hover:bg-blue-700 transition"
      >
        Analisi Completa
      </a>
    </div>
  )
}
