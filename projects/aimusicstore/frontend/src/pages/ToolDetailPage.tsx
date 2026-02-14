import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { getTool, type Tool } from '../api/client'

export default function ToolDetailPage() {
  const { id } = useParams<{ id: string }>()
  const [tool, setTool] = useState<Tool | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function loadTool() {
      if (!id) return

      try {
        setLoading(true)
        const toolData = await getTool(id)
        setTool(toolData)
        setLoading(false)
      } catch (err) {
        console.error('Failed to load tool:', err)
        setError('Tool not found')
        setLoading(false)
      }
    }

    loadTool()
  }, [id])

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0a0a0a] text-white flex items-center justify-center">
        <div className="text-2xl font-bold animate-pulse">Loading tool details...</div>
      </div>
    )
  }

  if (error || !tool) {
    return (
      <div className="min-h-screen bg-[#0a0a0a] text-white flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-4xl font-bold mb-4">Tool Not Found</h1>
          <p className="text-[#e0e7ff] mb-8">The tool you're looking for doesn't exist or has been removed.</p>
          <a href="/" className="px-6 py-3 bg-[#a855f7] hover:bg-[#c975fb] text-white rounded-lg font-semibold transition">
            Back to Home
          </a>
        </div>
      </div>
    )
  }

  const votePercentage = tool.total_votes > 0
    ? Math.round((tool.up_votes / tool.total_votes) * 100)
    : 0

  const features = tool.features ? JSON.parse(tool.features) : []
  const pricing = tool.pricing ? JSON.parse(tool.pricing) : null

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
              <a href="/top" className="text-white/90 hover:text-white transition">Top 50</a>
              <a href="/api" className="text-white/90 hover:text-white transition">API Docs</a>
            </nav>
          </div>
        </div>
      </header>

      {/* Breadcrumb */}
      <div className="bg-[#1a1a2e] border-b border-[#37224a]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3">
          <nav className="text-sm text-[#e0e7ff]">
            <a href="/" className="hover:text-white transition">Home</a>
            <span className="mx-2">/</span>
            <a href="/top" className="hover:text-white transition">Top 50</a>
            <span className="mx-2">/</span>
            <span className="text-white">{tool.name}</span>
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-3 gap-8">
            {/* Left Column: Tool Info */}
            <div className="md:col-span-2 space-y-6">
              {/* Tool Header */}
              <div className="bg-[#1a1a2e] rounded-lg p-8 border border-[#37224a]">
                <div className="flex items-start justify-between mb-6">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <h1 className="text-4xl font-bold">{tool.name}</h1>
                      {tool.rating && (
                        <div className="flex items-center space-x-1 bg-yellow-500/20 px-2 py-1 rounded">
                          <span className="text-yellow-500">★</span>
                          <span className="text-sm font-semibold">{tool.rating}</span>
                        </div>
                      )}
                    </div>
                    <a
                      href={tool.website}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-[#e0e7ff] hover:text-[#a855f7] transition"
                    >
                      {tool.website}
                    </a>
                  </div>
                  <div className="text-right ml-4">
                    <div className="text-5xl font-bold text-[#a855f7]">#{tool.rank}</div>
                    <div className="text-sm text-[#e0e7ff]">Current Rank</div>
                  </div>
                </div>

                <div className="flex flex-wrap gap-2 mb-6">
                  <span className="px-3 py-1 bg-[#a855f7] text-white rounded-full text-sm font-semibold">
                    {tool.category}
                  </span>
                  {tool.review_count && tool.review_count > 0 && (
                    <span className="px-3 py-1 bg-[#241432] rounded-full text-sm text-[#e0e7ff]">
                      {tool.review_count} reviews
                    </span>
                  )}
                </div>

                <p className="text-[#e0e7ff] mb-6">
                  {tool.name} is a {tool.category.toLowerCase()} tool for AI music generation.
                  Voted as one of the top tools in its category by the community.
                </p>

                {/* Vote Bar */}
                <div className="bg-[#241432] rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-[#e0e7ff]">Community Approval</span>
                    <span className="text-lg font-bold text-[#a855f7]">{votePercentage}%</span>
                  </div>
                  <div className="w-full bg-[#0a0a0a] rounded-full h-3 overflow-hidden">
                    <div
                      className="bg-gradient-to-r from-[#a855f7] to-[#c975fb] h-full transition-all duration-500"
                      style={{ width: `${votePercentage}%` }}
                    />
                  </div>
                  <div className="flex items-center justify-between mt-2 text-sm text-[#e0e7ff]">
                    <span>👍 {tool.up_votes} upvotes</span>
                    <span>👎 {tool.down_votes} downvotes</span>
                  </div>
                </div>
              </div>

              {/* Features Section */}
              {features.length > 0 && (
                <div className="bg-[#1a1a2e] rounded-lg p-6 border border-[#37224a]">
                  <h2 className="text-2xl font-bold mb-4">Features</h2>
                  <ul className="grid md:grid-cols-2 gap-3">
                    {features.map((feature: string, index: number) => (
                      <li key={index} className="flex items-start space-x-2">
                        <span className="text-[#a855f7] mt-1">✓</span>
                        <span className="text-[#e0e7ff]">{feature}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Pricing Section */}
              {pricing && (
                <div className="bg-[#1a1a2e] rounded-lg p-6 border border-[#37224a]">
                  <h2 className="text-2xl font-bold mb-4">Pricing</h2>
                  <div className="space-y-3">
                    {Object.entries(pricing).map(([tier, info]: [string, any]) => (
                      <div key={tier} className="bg-[#241432] rounded-lg p-4">
                        <div className="flex justify-between items-center mb-2">
                          <span className="font-semibold capitalize">{tier}</span>
                          <span className="text-[#a855f7] font-bold">{info.price}</span>
                        </div>
                        <p className="text-sm text-[#e0e7ff]">{info.description}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* About Section */}
              <div className="bg-[#1a1a2e] rounded-lg p-6 border border-[#37224a]">
                <h2 className="text-2xl font-bold mb-4">About {tool.name}</h2>
                <p className="text-[#e0e7ff] mb-4">
                  {tool.name} is a leading {tool.category.toLowerCase()} tool in the AI music generation space.
                  It has been voted on by the community and currently holds rank #{tool.rank} among all music creation tools.
                </p>
                <p className="text-[#e0e7ff] mb-4">
                  The tool has received {tool.total_votes} total votes with a {votePercentage}% approval rating,
                  indicating strong community support for its capabilities and features.
                </p>
                <p className="text-[#e0e7ff]">
                  Rankings are determined by weighted voting, where high-reputation agents have more influence.
                  This ensures that tools are ranked based on genuine quality and user experience rather than raw vote counts.
                </p>
              </div>
            </div>

            {/* Right Column: Actions */}
            <div className="space-y-6">
              {/* Vote Card */}
              <div className="bg-[#1a1a2e] rounded-lg p-6 border border-[#37224a]">
                <h3 className="text-xl font-bold mb-4">Vote for This Tool</h3>
                <p className="text-sm text-[#e0e7ff] mb-4">
                  Sign in to vote and help shape the rankings
                </p>
                <div className="space-y-2">
                  <button className="w-full px-4 py-3 bg-green-600 hover:bg-green-700 text-white rounded-lg font-semibold transition flex items-center justify-center space-x-2">
                    <span>👍</span>
                    <span>Upvote</span>
                  </button>
                  <button className="w-full px-4 py-3 bg-red-600 hover:bg-red-700 text-white rounded-lg font-semibold transition flex items-center justify-center space-x-2">
                    <span>👎</span>
                    <span>Downvote</span>
                  </button>
                </div>
              </div>

              {/* Visit Website Card */}
              <div className="bg-[#1a1a2e] rounded-lg p-6 border border-[#37224a]">
                <h3 className="text-xl font-bold mb-4">Visit Website</h3>
                <p className="text-sm text-[#e0e7ff] mb-4">
                  Try {tool.name} and create AI-generated music
                </p>
                <a
                  href={tool.website}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block w-full px-4 py-3 bg-[#a855f7] hover:bg-[#c975fb] text-white rounded-lg font-semibold transition text-center"
                >
                  Go to {tool.name}
                </a>
              </div>

              {/* Rating & Reviews Card */}
              {tool.rating && (
                <div className="bg-[#1a1a2e] rounded-lg p-6 border border-[#37224a]">
                  <h3 className="text-xl font-bold mb-4">Rating & Reviews</h3>
                  <div className="flex items-center space-x-3 mb-4">
                    <div className="text-5xl font-bold text-yellow-500">{tool.rating}</div>
                    <div>
                      <div className="flex text-yellow-500">★★★★★</div>
                      <div className="text-sm text-[#e0e7ff]">
                        {tool.review_count || 0} reviews
                      </div>
                    </div>
                  </div>
                  <p className="text-sm text-[#e0e7ff]">
                    Based on user reviews and community feedback
                  </p>
                </div>
              )}

              {/* Share Card */}
              <div className="bg-[#1a1a2e] rounded-lg p-6 border border-[#37224a]">
                <h3 className="text-xl font-bold mb-4">Share</h3>
                <div className="space-y-2">
                  <button className="w-full px-4 py-2 bg-[#241432] hover:bg-[#37224a] text-white rounded-lg font-semibold transition">
                    Copy Link
                  </button>
                  <button className="w-full px-4 py-2 bg-[#241432] hover:bg-[#37224a] text-white rounded-lg font-semibold transition">
                    Share on Twitter
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Related Tools Section */}
      <section className="py-16 bg-[#1a1a2e]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold mb-6">More {tool.category} Tools</h2>
          <div className="text-center py-12 text-[#e0e7ff]">
            <p>Discover more music creation tools in our trending rankings</p>
            <a
              href="/trending"
              className="inline-block mt-4 px-6 py-3 bg-[#a855f7] hover:bg-[#c975fb] text-white rounded-lg font-semibold transition"
            >
              Explore Trending
            </a>
          </div>
        </div>
      </section>

      {/* SEO Content */}
      <section className="py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <article className="prose prose-invert prose-lg max-w-none">
            <h2 className="text-3xl font-bold mb-6">
              AI Music Creation Tools: Community-Driven Rankings
            </h2>
            <p className="text-[#e0e7ff] mb-4">
              {tool.name} is a {tool.category.toLowerCase()} platform that has earned its place in the AI music generation ecosystem.
              With rank #{tool.rank} and a {votePercentage}% community approval rating, it represents one of the most trusted tools for creators.
            </p>
            <p className="text-[#e0e7ff] mb-4">
              Our weighted voting system ensures that high-reputation agents have more influence on rankings,
              preventing manipulation and highlighting genuinely useful tools. {tool.name} has demonstrated
              consistent quality and user satisfaction to achieve its current position.
            </p>
            <p className="text-[#e0e7ff] mb-4">
              Key features include powerful {tool.category.toLowerCase()} capabilities, making it suitable for
              musicians, producers, and content creators looking to leverage AI in their workflow.
            </p>
            <p className="text-[#e0e7ff]">
              Check back regularly as rankings update in real-time. Join the community, vote for your favorite tools,
              and help others discover the best AI music creation platforms available.
            </p>
          </article>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 border-t border-[#37224a]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center text-sm text-[#e0e7ff]">
            © 2026 aimusicstore.com — Last updated {new Date(tool.created_at).toLocaleString()}
          </div>
        </div>
      </footer>
    </div>
  )
}
