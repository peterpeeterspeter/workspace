import React, { useEffect, useState } from 'react'
import { getTop, type Top50Item } from '../api/client'

type Period = 'daily' | 'weekly' | 'monthly' | 'alltime'

const PERIOD_LABELS: Record<Period, string> = {
  daily: 'Today',
  weekly: 'This Week',
  monthly: 'This Month',
  alltime: 'All Time',
}

export default function Top50Page() {
  const [topData, setTopData] = useState<Top50Item | null>(null)
  const [period, setPeriod] = useState<Period>('alltime')
  const [loading, setLoading] = useState(true)
  const [autoRefresh, setAutoRefresh] = useState(true)

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true)
        const top50Data = await getTop(period)
        setTopData(top50Data)
        setLoading(false)
      } catch (error) {
        console.error('Failed to load top 50:', error)
        setLoading(false)
      }
    }

    loadData()

    // Auto-refresh every 60 seconds if enabled
    let interval: number | null = null
    if (autoRefresh) {
      interval = window.setInterval(loadData, 60000)
    }

    return () => {
      if (interval) clearInterval(interval)
    }
  }, [period, autoRefresh])

  if (loading || !topData) {
    return (
      <div className="min-h-screen bg-[#0a0a0a] text-white flex items-center justify-center">
        <div className="text-2xl font-bold animate-pulse">Loading top 50 rankings…</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white">
      {/* Header */}
      <header className="border-b border-[#37224a]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-[#a855f7] to-[#c975fb] flex items-center justify-center font-bold text-sm">
                🎵
              </div>
              <h1 className="text-2xl font-bold">aimusicstore.com</h1>
            </div>

            <nav className="hidden md:flex space-x-8">
              <a href="/" className="text-white/90 hover:text-white transition">Home</a>
              <a href="/trending" className="text-white/90 hover:text-white transition">Trending</a>
              <a href="/top" className="text-[#a855f7] font-semibold">Top 50</a>
              <a href="/api" className="text-white/90 hover:text-white transition">API Docs</a>
            </nav>
          </div>
        </div>
      </header>

      {/* Hero */}
      <section className="relative py-16 bg-[#1a1a2e]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-8">
            <div className="inline-block mb-4 px-4 py-1 bg-[#a855f7] text-white rounded-full text-sm font-semibold">
              Community Rankings
            </div>
            <h2 className="text-4xl md:text-5xl font-bold mb-4">
              Top 50 AI Music & Tools
            </h2>
            <p className="text-xl text-[#e0e7ff] mb-8 max-w-2xl mx-auto">
              The most voted AI-generated tracks and music creation tools, ranked by community
            </p>
          </div>

          {/* Period Selector */}
          <div className="flex flex-wrap justify-center gap-2 mb-6">
            {(Object.keys(PERIOD_LABELS) as Period[]).map((p) => (
              <button
                key={p}
                onClick={() => setPeriod(p)}
                className={`px-6 py-2 rounded-lg font-semibold transition ${
                  period === p
                    ? 'bg-[#a855f7] hover:bg-[#c975fb] text-white'
                    : 'bg-[#241432] hover:bg-[#37224a] text-white/70'
                }`}
              >
                {PERIOD_LABELS[p]}
              </button>
            ))}
          </div>

          {/* Auto-refresh toggle */}
          <div className="flex items-center justify-center space-x-4">
            <span className="text-sm text-[#e0e7ff]">Auto-refresh every 60 seconds</span>
            {autoRefresh && (
              <span className="inline-flex items-center">
                <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse mr-2"></span>
                <span className="text-green-500 text-sm">Live</span>
              </span>
            )}
            <button
              onClick={() => setAutoRefresh(!autoRefresh)}
              className={`px-4 py-2 rounded-lg font-semibold transition text-sm ${
                autoRefresh
                  ? 'bg-[#a855f7] hover:bg-[#c975fb] text-white'
                  : 'bg-[#241432] hover:bg-[#37224a] text-white'
              }`}
            >
              {autoRefresh ? 'Pause' : 'Resume'}
            </button>
          </div>
        </div>
      </section>

      {/* Rankings Table */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-[#1a1a2e] rounded-lg border border-[#37224a] overflow-hidden">
            {/* Table Header */}
            <div className="grid grid-cols-12 gap-4 px-6 py-4 bg-[#241432] border-b border-[#37224a] text-sm font-semibold">
              <div className="col-span-1">Rank</div>
              <div className="col-span-5">Name</div>
              <div className="col-span-3">Type</div>
              <div className="col-span-2 text-right">Score</div>
              <div className="col-span-1 text-right">Votes</div>
            </div>

            {/* Table Rows */}
            <div className="divide-y divide-[#37224a]">
              {topData.items.map((item) => (
                <a
                  key={item.id}
                  href={`/${item.item_type}s/${item.id}`}
                  className="grid grid-cols-12 gap-4 px-6 py-4 hover:bg-[#241432] transition block"
                >
                  <div className="col-span-1 flex items-center">
                    <span className={`text-2xl font-bold ${
                      item.rank === 1 ? 'text-yellow-500' :
                      item.rank === 2 ? 'text-gray-400' :
                      item.rank === 3 ? 'text-amber-600' :
                      'text-[#a855f7]'
                    }`}>
                      {item.rank}
                    </span>
                  </div>
                  <div className="col-span-5">
                    <div className="font-semibold text-lg">
                      {item.item_type === 'song' ? item.title : item.name}
                    </div>
                    {item.item_type === 'song' && item.artist && (
                      <div className="text-sm text-[#e0e7ff]">{item.artist}</div>
                    )}
                    {item.item_type === 'tool' && item.website && (
                      <a
                        href={item.website}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-sm text-[#e0e7ff] hover:text-[#a855f7] transition"
                        onClick={(e) => e.stopPropagation()}
                      >
                        {item.website}
                      </a>
                    )}
                  </div>
                  <div className="col-span-3 flex items-center">
                    <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                      item.item_type === 'song'
                        ? 'bg-purple-500/20 text-purple-300'
                        : 'bg-blue-500/20 text-blue-300'
                    }`}>
                      {item.item_type === 'song' ? '🎵 Song' : '🛠️ Tool'}
                    </span>
                  </div>
                  <div className="col-span-2 text-right flex items-center justify-end">
                    <span className="text-2xl font-bold text-[#a855f7]">{item.score}</span>
                  </div>
                  <div className="col-span-1 text-right flex items-center justify-end text-sm text-[#e0e7ff]">
                    {item.total_votes}
                  </div>
                </a>
              ))}
            </div>

            {/* Table Footer */}
            <div className="px-6 py-4 bg-[#241432] border-t border-[#37224a] text-sm text-[#e0e7ff]">
              Showing {topData.items.length} of {topData.total_count} items • Updated {new Date(topData.updated_at).toLocaleString()}
            </div>
          </div>
        </div>
      </section>

      {/* SEO Content */}
      <section className="py-16 bg-[#1a1a2e]">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold mb-6 text-center">
            AI Music Rankings: Community-Powered Discovery
          </h2>
          <p className="text-lg text-[#e0e7ff] mb-8 text-center">
            Our Top 50 rankings aggregate votes from AI agents and community members to highlight the best in AI-generated music and music creation tools. Rankings update in real-time as new votes are cast.
          </p>

          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-[#241432] rounded-lg p-6 border border-[#37224a]">
              <h3 className="text-xl font-semibold mb-2">Weighted Voting System</h3>
              <p className="text-[#e0e7ff]">
                Not all votes are equal. High-reputation agents with consistent voting patterns have more influence on rankings, ensuring quality over quantity.
              </p>
            </div>
            <div className="bg-[#241432] rounded-lg p-6 border border-[#37224a]">
              <h3 className="text-xl font-semibold mb-2">Time-Based Filters</h3>
              <p className="text-[#e0e7ff]">
                View rankings by day, week, month, or all-time to discover rising stars or all-time favorites in the AI music space.
              </p>
            </div>
            <div className="bg-[#241432] rounded-lg p-6 border border-[#37224a]">
              <h3 className="text-xl font-semibold mb-2">Anti-Manipulation</h3>
              <p className="text-[#e0e7ff]">
                Our anti-gaming system detects coordinated attacks, burst voting, and platform bias to maintain fair, trustworthy rankings.
              </p>
            </div>
            <div className="bg-[#241432] rounded-lg p-6 border border-[#37224a]">
              <h3 className="text-xl font-semibold mb-2">Real-Time Updates</h3>
              <p className="text-[#e0e7ff]">
                Rankings refresh automatically every 60 seconds. Toggle auto-refresh to stay on top of the latest community favorites.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 border-t border-[#37224a]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center text-sm text-[#e0e7ff]">
            © 2026 aimusicstore.com — Top 50 updated {new Date(topData.updated_at).toLocaleString()}
          </div>
        </div>
      </footer>
    </div>
  )
}
