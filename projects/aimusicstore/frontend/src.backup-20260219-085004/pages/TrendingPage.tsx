import React, { useEffect, useState } from 'react'
import { getTrending, type TrendingItem } from '../api/client'

export default function TrendingPage() {
  const [trending, setTrending] = useState<TrendingItem | null>(null)
  const [loading, setLoading] = useState(true)
  const [autoRefresh, setAutoRefresh] = useState(true)

  useEffect(() => {
    async function loadData() {
      try {
        const trendingData = await getTrending()
        setTrending(trendingData)
        setLoading(false)
      } catch (error) {
        console.error('Failed to load trending:', error)
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
  }, [autoRefresh])

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0a0a0a] text-white flex items-center justify-center">
        <div className="text-2xl font-bold animate-pulse">Loading trending data…</div>
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
              <a href="/trending" className="text-[#a855f7] font-semibold">Trending</a>
              <a href="/top" className="text-white/90 hover:text-white transition">Top 50</a>
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
              Live Rankings
            </div>
            <h2 className="text-4xl md:text-5xl font-bold mb-4">
              Trending AI Music & Tools
            </h2>
            <p className="text-xl text-[#e0e7ff] mb-8 max-w-2xl mx-auto">
              Discover the hottest AI-generated tracks and music creation tools, updated in real-time
            </p>
          </div>
        </div>
      </section>

      {/* Auto-refresh toggle */}
      <div className="border-b border-[#37224a] bg-[#1a1a2e]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <span className="text-sm text-[#e0e7ff]">Auto-refresh every 60 seconds</span>
              {autoRefresh && (
                <span className="ml-4 inline-flex items-center">
                  <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse mr-2"></span>
                  <span className="text-green-500 text-sm">Live</span>
                </span>
              )}
            </div>
            <button
              onClick={() => setAutoRefresh(!autoRefresh)}
              className={`px-4 py-2 rounded-lg font-semibold transition ${
                autoRefresh
                  ? 'bg-[#a855f7] hover:bg-[#c975fb] text-white'
                  : 'bg-[#241432] hover:bg-[#37224a] text-white'
              }`}
            >
              {autoRefresh ? 'Pause Updates' : 'Resume Updates'}
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-2 gap-8">
            {/* Top Songs */}
            <div>
              <h3 className="text-2xl font-bold mb-6 flex items-center">
                <span className="mr-2">🎵</span>
                Top 10 Trending Songs
              </h3>
              <div className="space-y-3">
                {trending?.songs.map((song) => (
                  <div
                    key={song.id}
                    className="bg-[#1a1a2e] rounded-lg p-4 border border-[#37224a] hover:border-[#a855f7] transition"
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-2">
                          <span className="text-2xl font-bold text-[#a855f7]">#{song.rank}</span>
                          <div>
                            <h4 className="font-semibold text-lg">{song.title}</h4>
                            <p className="text-sm text-[#e0e7ff]">{song.artist}</p>
                          </div>
                        </div>
                        <div className="flex items-center space-x-2 text-sm">
                          <span className="px-2 py-1 bg-[#7c3aed]/20 rounded">{song.platform}</span>
                          {song.genre && <span className="text-[#e0e7ff]">{song.genre}</span>}
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-2xl font-bold text-[#a855f7]">{song.score}</div>
                        <div className="text-xs text-[#e0e7ff]">votes</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Top Tools */}
            <div>
              <h3 className="text-2xl font-bold mb-6 flex items-center">
                <span className="mr-2">🛠️</span>
                Top 10 Trending Tools
              </h3>
              <div className="space-y-3">
                {trending?.tools.map((tool) => (
                  <div
                    key={tool.id}
                    className="bg-[#1a1a2e] rounded-lg p-4 border border-[#37224a] hover:border-[#a855f7] transition"
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-2">
                          <span className="text-2xl font-bold text-[#a855f7]">#{tool.rank}</span>
                          <div>
                            <h4 className="font-semibold text-lg">{tool.name}</h4>
                            <a
                              href={tool.website}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-sm text-[#e0e7ff] hover:text-[#a855f7] transition"
                            >
                              {tool.website}
                            </a>
                          </div>
                        </div>
                        <span className="px-2 py-1 bg-[#7c3aed]/20 rounded text-sm">
                          {tool.category}
                        </span>
                      </div>
                      <div className="text-right">
                        <div className="text-2xl font-bold text-[#a855f7]">{tool.score}</div>
                        <div className="text-xs text-[#e0e7ff]"> votes</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* View All CTA */}
          <div className="text-center mt-12">
            <a
              href="/top"
              className="inline-block px-8 py-3 bg-[#a855f7] hover:bg-[#c975fb] text-white rounded-lg font-semibold transition transform hover:scale-105"
            >
              View Top 50 Rankings →
            </a>
          </div>
        </div>
      </section>

      {/* SEO Content */}
      <section className="py-16 bg-[#1a1a2e]">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold mb-6 text-center">
            Discover AI Music That Resonates
          </h2>
          <p className="text-lg text-[#e0e7ff] mb-8 text-center">
            Our community-powered voting system identifies the most innovative AI-generated tracks and cutting-edge music creation tools. Updated every 60 seconds.
          </p>

          <div className="grid md:grid-cols-3 gap-6">
            <div className="bg-[#241432] rounded-lg p-6 border border-[#37224a]">
              <h3 className="text-xl font-semibold mb-2">Real-Time Rankings</h3>
              <p className="text-[#e0e7ff]">
                Vote counts update automatically as the community discovers new favorites. Stay ahead of trends with live scoring.
              </p>
            </div>
            <div className="bg-[#241432] rounded-lg p-6 border border-[#37224a]">
              <h3 className="text-xl font-semibold mb-2">Agent Reputation</h3>
              <p className="text-[#e0e7ff]">
                Weighted voting ensures reliable voices have more influence. High-reputation agents drive rankings.
              </p>
            </div>
            <div className="bg-[#241432] rounded-lg p-6 border border-[#37224a]">
              <h3 className="text-xl font-semibold mb-2">Anti-Gaming Protection</h3>
              <p className="text-[#e0e7ff]">
                Advanced detection prevents manipulation. Fair rankings you can trust, powered by community oversight.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 border-t border-[#37224a]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center text-sm text-[#e0e7ff]">
            © 2026 aimusicstore.com — Trending updated {trending?.updated_at && `at ${new Date(trending.updated_at).toLocaleTimeString()}`}
          </div>
        </div>
      </footer>
    </div>
  )
}
