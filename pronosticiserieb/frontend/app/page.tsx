import { MatchCard } from '@/components/MatchCard'
import { PredictionStats } from '@/components/PredictionStats'

export default function HomePage() {
  // Mock data - will be replaced with Supabase fetch
  const todayMatches = [
    {
      id: '1',
      homeTeam: 'Brescia',
      awayTeam: 'Palermo',
      date: new Date('2025-02-01T15:00:00'),
      status: 'scheduled' as const,
      prediction: {
        homeWin: 52,
        draw: 28,
        awayWin: 20,
        confidence: 65,
        recommended: 'home' as const,
        valueBet: true,
        reasoning: 'Brescia in ottima forma, vantaggio casa'
      }
    },
    {
      id: '2',
      homeTeam: 'Parma',
      awayTeam: 'Venezia',
      date: new Date('2025-02-01T18:00:00'),
      status: 'scheduled' as const,
      prediction: {
        homeWin: 42,
        draw: 32,
        awayWin: 26,
        confidence: 48,
        recommended: 'home' as const,
        valueBet: false,
        reasoning: 'Partita equilibrata, leggero vantaggio Parma'
      }
    },
    {
      id: '3',
      homeTeam: 'Catanzaro',
      awayTeam: 'Cremonese',
      date: new Date('2025-02-01T20:45:00'),
      status: 'scheduled' as const,
      prediction: {
        homeWin: 38,
        draw: 34,
        awayWin: 28,
        confidence: 42,
        recommended: 'draw' as const,
        valueBet: false,
        reasoning: 'Squadre vicine in classifica, X probabile'
      }
    }
  ]

  const stats = {
    totalPredictions: 245,
    accuracy: 67.3,
    activeSubscribers: 1200
  }

  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <section className="text-center py-12">
        <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">
          Pronostici Serie B Oggi
        </h2>
        <p className="text-xl text-gray-400 mb-6">
          Previsioni AI basate su statistiche avanzate
        </p>
        <PredictionStats stats={stats} />
      </section>

      {/* Today's Matches */}
      <section>
        <h3 className="text-2xl font-bold text-white mb-6">
          Partite di Oggi
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {todayMatches.map(match => (
            <MatchCard key={match.id} match={match} />
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-gradient-to-r from-blue-900 to-purple-900 rounded-xl p-8 text-center">
        <h3 className="text-2xl font-bold text-white mb-3">
          Vuoi Pronostici Più Accurati?
        </h3>
        <p className="text-gray-300 mb-6">
          Iscriviti alla VIP newsletter per ricevere pronostici premium con analisi detailed
        </p>
        <form className="max-w-md mx-auto flex gap-3">
          <input
            type="email"
            placeholder="La tua email"
            className="flex-1 px-4 py-3 rounded-lg bg-gray-800 text-white border border-gray-700 focus:border-blue-500 focus:outline-none"
          />
          <button
            type="submit"
            className="px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition"
          >
            Iscriviti
          </button>
        </form>
      </section>

      {/* Features */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-gray-800 rounded-xl p-6">
          <div className="text-3xl mb-3">🤖</div>
          <h4 className="text-lg font-bold text-white mb-2">AI-Powered</h4>
          <p className="text-gray-400 text-sm">
            Modelli machine learning che analizzano forma, statistiche e storico
          </p>
        </div>
        <div className="bg-gray-800 rounded-xl p-6">
          <div className="text-3xl mb-3">📊</div>
          <h4 className="text-lg font-bold text-white mb-2">Statistiche Advanced</h4>
          <p className="text-gray-400 text-sm">
            Dati detailed su gol, forma casa/trasferta, testa a testa
          </p>
        </div>
        <div className="bg-gray-800 rounded-xl p-6">
          <div className="text-3xl mb-3">✅</div>
          <h4 className="text-lg font-bold text-white mb-2">67% Accuratezza</h4>
          <p className="text-gray-400 text-sm">
            I nostri pronostici colpiscono il bersaglio nel 67% dei casi
          </p>
        </div>
      </section>
    </div>
  )
}
