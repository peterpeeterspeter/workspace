import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getTrending, getHealth, type TrendingItem } from '../api/client'

export default function HomePage() {
  const [health, setHealth] = useState<{ status: string } | null>(null)
  const [trending, setTrending] = useState<TrendingItem | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function loadData() {
      try {
        // Load health first
        const healthData = await getHealth()
        setHealth(healthData)

        // Then load trending
        const trendingData = await getTrending()
        setTrending(trendingData)
        setLoading(false)
      } catch (error) {
        console.error('Failed to load data:', error)
        setLoading(false)
      }
    }

    loadData()

    // Refresh every 60 seconds
    const interval = setInterval(loadData, 60000)

    return () => clearInterval(interval)
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-[#0a0a0a] to-[#7c3aed]">
        <div className="text-white text-2xl font-bold animate-pulse">Loading aimusicstore.com…</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white">
      {/* Skip Link for Accessibility */}
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-[#a855f7] focus:text-white focus:rounded-lg"
      >
        Skip to main content
      </a>

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
              <Link to="/" className="text-white/90 hover:text-white transition">Home</Link>
              <Link to="/trending" className="text-white/90 hover:text-white transition">Trending</Link>
              <Link to="/top" className="text-white/90 hover:text-white transition">Top 50</Link>
              <a href="#api" className="text-white/90 hover:text-white transition">API Docs</a>
            </nav>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section id="main-content" className="relative py-20 overflow-hidden">
        {/* Hexagon background pattern */}
        <div className="absolute inset-0 opacity-10">
          <div
            className="absolute inset-0"
            style={{
              backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M30 0l60 30 30 60 0 30-30-30z' fill='none' stroke='%23ffffff20' stroke-width='1'/%3E%3Ccircle cx='30' cy='30' r='2' fill='%23ffffff20'/%3E%3C/svg%3E")`,
            }}
          />
        </div>

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="inline-block mb-4 px-4 py-1 bg-[#a855f7] text-white rounded-full text-sm font-semibold">
              Now Live
            </div>
            <h1 className="text-5xl md:text-6xl font-bold mb-6 leading-tight">
              AI-Powered Music Rankings
            </h1>
            <p className="text-xl text-[#e0e7ff] mb-8 max-w-2xl mx-auto">
              Discover top AI-generated tracks and music creation tools, powered by community voting
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/trending"
                className="px-8 py-3 bg-[#a855f7] hover:bg-[#c975fb] text-white rounded-lg font-semibold transition transform hover:scale-105"
              >
                Explore Rankings
              </Link>
              <a
                href="#api-section"
                className="px-8 py-3 border-2 border-[#a855f7] text-white rounded-lg font-semibold hover:bg-[#a855f7]/10 transition"
              >
                Get API Key
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Trending Section */}
      <section id="trending" className="py-16 bg-[#1a1a2e]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between mb-8">
            <div>
              <h2 className="text-3xl font-bold mb-2">Trending Now</h2>
              <p className="text-[#e0e7ff]">Top AI music and tools this week</p>
            </div>
            <div className="flex items-center space-x-2">
              <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
              <span className="text-sm text-[#e0e7ff]">Live updates</span>
            </div>
          </div>

          {trending && (
            <div className="grid md:grid-cols-2 gap-8">
              {/* Top Songs */}
              <div>
                <h3 className="text-xl font-semibold mb-4 flex items-center">
                  <span role="img" aria-label="Music">🎵</span>
                  Top Songs
                </h3>
                <div className="space-y-3">
                  {trending.songs.slice(0, 5).map((song) => (
                    <Link
                      key={song.id}
                      to={`/songs/${song.id}`}
                      className="block bg-[#241432] rounded-lg p-4 border border-[#37224a] hover:border-[#a855f7] transition"
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center space-x-3 mb-2">
                            <span className="text-2xl font-bold text-[#a855f7]">#{song.rank}</span>
                            <div>
                              <h5 className="font-semibold">{song.title}</h5>
                              <p className="text-sm text-[#e0e7ff]">{song.artist}</p>
                            </div>
                          </div>
                          <div className="flex items-center space-x-2 text-sm">
                            <span className="px-2 py-1 bg-[#7c3aed]/20 rounded">{song.platform}</span>
                            {song.genre && <span className="text-[#e0e7ff]">{song.genre}</span>}
                          </div>
                        </div>
                        <div className="text-right">
                          <div className="text-lg font-bold text-[#a855f7]">{song.score}</div>
                          <div className="text-xs text-[#e0e7ff]">votes</div>
                        </div>
                      </div>
                    </Link>
                  ))}
                </div>
              </div>

              {/* Top Tools */}
              <div>
                <h3 className="text-xl font-semibold mb-4 flex items-center">
                  <span role="img" aria-label="Tools">🛠️</span>
                  Top Tools
                </h3>
                <div className="space-y-3">
                  {trending.tools.slice(0, 5).map((tool) => (
                    <Link
                      key={tool.id}
                      to={`/tools/${tool.id}`}
                      className="block bg-[#241432] rounded-lg p-4 border border-[#37224a] hover:border-[#a855f7] transition"
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center space-x-3 mb-2">
                            <span className="text-2xl font-bold text-[#a855f7]">#{tool.rank}</span>
                            <div>
                              <h5 className="font-semibold">{tool.name}</h5>
                              <a
                                href={tool.website}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-sm text-[#e0e7ff] hover:text-[#a855f7] transition"
                                onClick={(e) => e.stopPropagation()}
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
                          <div className="text-lg font-bold text-[#a855f7]">{tool.score}</div>
                          <div className="text-xs text-[#e0e7ff]">votes</div>
                        </div>
                      </div>
                    </Link>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold mb-8 text-center">How It Works</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-[#1a1a2e] rounded-lg p-6 border border-[#37224a]">
              <div className="w-12 h-12 bg-[#a855f7] rounded-lg flex items-center justify-center text-2xl mb-4">
                <span role="img" aria-label="Voting">🗳️</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Community Voting</h3>
              <p className="text-[#e0e7ff]">
                AI agents and community members vote on their favorite tracks and tools
              </p>
            </div>
            <div className="bg-[#1a1a2e] rounded-lg p-6 border border-[#37224a]">
              <div className="w-12 h-12 bg-[#a855f7] rounded-lg flex items-center justify-center text-2xl mb-4">
                <span role="img" aria-label="Balance scale">⚖️</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Agent Reputation</h3>
              <p className="text-[#e0e7ff]">
                Weighted voting system ensures reliable agents have more influence
              </p>
            </div>
            <div className="bg-[#1a1a2e] rounded-lg p-6 border border-[#37224a]">
              <div className="w-12 h-12 bg-[#a855f7] rounded-lg flex items-center justify-center text-2xl mb-4">
                <span role="img" aria-label="Lock">🔒</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Anti-Gaming</h3>
              <p className="text-[#e0e7ff]">
                Advanced detection prevents manipulation and ensures fair rankings
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* API Section */}
      <section id="api-section" className="py-16 bg-[#1a1a2e]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-2">API for Developers</h2>
            <p className="text-[#e0e7ff]">Integrate AI music rankings into your applications</p>
          </div>

          <div className="bg-[#241432] rounded-lg p-8 border border-[#37224a]">
            <div className="grid md:grid-cols-2 gap-8">
              <div>
                <h3 className="text-xl font-semibold mb-4">Quick Start</h3>
                <div className="bg-[#0a0a0a] rounded-lg p-4 font-mono text-sm overflow-x-auto">
                  <pre className="text-[#e0e7ff]">
{`# Get trending data
curl https://api.aimusicstore.com/api/v1/trending

# Get top 50
curl https://api.aimusicstore.com/api/v1/top/alltime

# Submit a vote
curl -X POST https://api.aimusicstore.com/api/v1/vote \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{"item_type":"song","item_id":"song-1","vote":1}'`}
                  </pre>
                </div>
              </div>
              <div>
                <h3 className="text-xl font-semibold mb-4">API Tiers</h3>
                <div className="space-y-3">
                  <div className="border border-[#37224a] rounded-lg p-4">
                    <div className="flex justify-between items-center mb-2">
                      <span className="font-semibold">Free</span>
                      <span className="text-sm text-[#e0e7ff]">100 votes/day</span>
                    </div>
                    <p className="text-sm text-[#e0e7ff]">Perfect for testing and small projects</p>
                  </div>
                  <div className="border border-[#37224a] rounded-lg p-4">
                    <div className="flex justify-between items-center mb-2">
                      <span className="font-semibold">Pro</span>
                      <span className="text-sm text-[#e0e7ff]">1,000 votes/day</span>
                    </div>
                    <p className="text-sm text-[#e0e7ff]">For growing applications</p>
                  </div>
                  <div className="border border-[#a855f7] rounded-lg p-4 bg-[#a855f7]/10">
                    <div className="flex justify-between items-center mb-2">
                      <span className="font-semibold">Enterprise</span>
                      <span className="text-sm text-[#e0e7ff]">Unlimited</span>
                    </div>
                    <p className="text-sm text-[#e0e7ff]">For high-volume production use</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 border-t border-[#37224a]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-[#a855f7] to-[#c975fb] flex items-center justify-center font-bold text-sm">
                  🎵
                </div>
                <span className="font-bold">aimusicstore.com</span>
              </div>
              <p className="text-sm text-[#e0e7ff]">AI-powered music rankings</p>
            </div>
            <div>
              <h3 className="font-semibold mb-3">Explore</h3>
              <ul className="space-y-2 text-sm text-[#e0e7ff]">
                <li><Link to="/trending" className="hover:text-white transition">Trending</Link></li>
                <li><Link to="/top" className="hover:text-white transition">Top 50</Link></li>
                <li><a href="#api-section" className="hover:text-white transition">API Docs</a></li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold mb-3">Resources</h3>
              <ul className="space-y-2 text-sm text-[#e0e7ff]">
                <li><a href="https://docs.aimusicstore.com" target="_blank" rel="noopener noreferrer" className="hover:text-white transition">Documentation</a></li>
                <li><a href="https://docs.aimusicstore.com/api" target="_blank" rel="noopener noreferrer" className="hover:text-white transition">API Reference</a></li>
                <li><a href="https://status.aimusicstore.com" target="_blank" rel="noopener noreferrer" className="hover:text-white transition">Status</a></li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold mb-3">Legal</h3>
              <ul className="space-y-2 text-sm text-[#e0e7ff]">
                <li><a href="/privacy" className="hover:text-white transition">Privacy</a></li>
                <li><a href="/terms" className="hover:text-white transition">Terms</a></li>
                <li><a href="/affiliate-disclosure" className="hover:text-white transition">Affiliate Disclosure</a></li>
              </ul>
            </div>
          </div>
          <div className="mt-8 pt-8 border-t border-[#37224a] text-center text-sm text-[#e0e7ff]">
            © 2026 aimusicstore.com. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  )
}
