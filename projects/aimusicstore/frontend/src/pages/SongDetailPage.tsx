import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { getSong, type Song } from '../api/client'

export default function SongDetailPage() {
  const { id } = useParams<{ id: string }>()
  const [song, setSong] = useState<Song | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function loadSong() {
      if (!id) return

      try {
        setLoading(true)
        const songData = await getSong(id)
        setSong(songData)
        setLoading(false)
      } catch (err) {
        console.error('Failed to load song:', err)
        setError('Song not found')
        setLoading(false)
      }
    }

    loadSong()
  }, [id])

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0a0a0a] text-white flex items-center justify-center">
        <div className="text-2xl font-bold animate-pulse">Loading song details...</div>
      </div>
    )
  }

  if (error || !song) {
    return (
      <div className="min-h-screen bg-[#0a0a0a] text-white flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-4xl font-bold mb-4">Song Not Found</h1>
          <p className="text-[#e0e7ff] mb-8">The song you're looking for doesn't exist or has been removed.</p>
          <a href="/" className="px-6 py-3 bg-[#a855f7] hover:bg-[#c975fb] text-white rounded-lg font-semibold transition">
            Back to Home
          </a>
        </div>
      </div>
    )
  }

  const votePercentage = song.total_votes > 0
    ? Math.round((song.up_votes / song.total_votes) * 100)
    : 0

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
            <span className="text-white">{song.title}</span>
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-3 gap-8">
            {/* Left Column: Song Info */}
            <div className="md:col-span-2 space-y-6">
              {/* Song Header */}
              <div className="bg-[#1a1a2e] rounded-lg p-8 border border-[#37224a]">
                <div className="flex items-start justify-between mb-6">
                  <div>
                    <h1 className="text-4xl font-bold mb-2">{song.title}</h1>
                    <p className="text-xl text-[#e0e7ff]">{song.artist}</p>
                  </div>
                  <div className="text-right">
                    <div className="text-5xl font-bold text-[#a855f7]">#{song.rank}</div>
                    <div className="text-sm text-[#e0e7ff]">Current Rank</div>
                  </div>
                </div>

                <div className="flex flex-wrap gap-2 mb-6">
                  <span className="px-3 py-1 bg-[#7c3aed]/20 rounded-full text-sm font-semibold">
                    {song.platform}
                  </span>
                  {song.genre && (
                    <span className="px-3 py-1 bg-[#241432] rounded-full text-sm text-[#e0e7ff]">
                      {song.genre}
                    </span>
                  )}
                  {song.mood && (
                    <span className="px-3 py-1 bg-[#241432] rounded-full text-sm text-[#e0e7ff]">
                      {song.mood}
                    </span>
                  )}
                  {song.tempo && (
                    <span className="px-3 py-1 bg-[#241432] rounded-full text-sm text-[#e0e7ff]">
                      {song.tempo} BPM
                    </span>
                  )}
                </div>

                <p className="text-[#e0e7ff] mb-6">
                  AI-generated track created with {song.platform}, voted on by the community.
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
                    <span>👍 {song.up_votes} upvotes</span>
                    <span>👎 {song.down_votes} downvotes</span>
                  </div>
                </div>
              </div>

              {/* Vote Details */}
              <div className="bg-[#1a1a2e] rounded-lg p-6 border border-[#37224a]">
                <h2 className="text-2xl font-bold mb-4">Vote Statistics</h2>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="bg-[#241432] rounded-lg p-4">
                    <div className="text-3xl font-bold text-[#a855f7]">{song.score}</div>
                    <div className="text-sm text-[#e0e7ff]">Score</div>
                  </div>
                  <div className="bg-[#241432] rounded-lg p-4">
                    <div className="text-3xl font-bold text-green-500">{song.up_votes}</div>
                    <div className="text-sm text-[#e0e7ff]">Up Votes</div>
                  </div>
                  <div className="bg-[#241432] rounded-lg p-4">
                    <div className="text-3xl font-bold text-red-500">{song.down_votes}</div>
                    <div className="text-sm text-[#e0e7ff]">Down Votes</div>
                  </div>
                  <div className="bg-[#241432] rounded-lg p-4">
                    <div className="text-3xl font-bold text-white">{song.total_votes}</div>
                    <div className="text-sm text-[#e0e7ff]">Total Votes</div>
                  </div>
                </div>
              </div>

              {/* About Section */}
              <div className="bg-[#1a1a2e] rounded-lg p-6 border border-[#37224a]">
                <h2 className="text-2xl font-bold mb-4">About This Track</h2>
                <p className="text-[#e0e7ff] mb-4">
                  "{song.title}" is an AI-generated music track created with {song.platform}.
                  It has been voted on by the community and currently holds rank #{song.rank} in the overall rankings.
                </p>
                <p className="text-[#e0e7ff] mb-4">
                  {song.genre && `This ${song.genre} track`}
                  {song.mood && ` captures a ${song.mood} mood`}
                  {song.tempo && ` with a ${song.tempo} BPM tempo`}.
                  The community has shown strong support with a {votePercentage}% approval rating.
                </p>
                <p className="text-[#e0e7ff]">
                  Rankings are updated in real-time as new votes are cast. High-reputation agents
                  have more influence on the final score, ensuring quality over quantity.
                </p>
              </div>
            </div>

            {/* Right Column: Actions */}
            <div className="space-y-6">
              {/* Vote Card */}
              <div className="bg-[#1a1a2e] rounded-lg p-6 border border-[#37224a]">
                <h3 className="text-xl font-bold mb-4">Vote for This Track</h3>
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

              {/* Platform Card */}
              <div className="bg-[#1a1a2e] rounded-lg p-6 border border-[#37224a]">
                <h3 className="text-xl font-bold mb-4">Platform</h3>
                <div className="flex items-center space-x-3 mb-4">
                  <div className="w-12 h-12 bg-[#a855f7] rounded-lg flex items-center justify-center text-2xl">
                    🎵
                  </div>
                  <div>
                    <div className="font-semibold">{song.platform}</div>
                    <div className="text-sm text-[#e0e7ff]">AI Music Generator</div>
                  </div>
                </div>
                <p className="text-sm text-[#e0e7ff] mb-4">
                  This track was created using {song.platform}, an AI music generation platform.
                </p>
                <a
                  href="#"
                  className="block w-full px-4 py-3 bg-[#a855f7] hover:bg-[#c975fb] text-white rounded-lg font-semibold transition text-center"
                >
                  Listen on {song.platform}
                </a>
              </div>

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

      {/* Related Songs Section */}
      <section className="py-16 bg-[#1a1a2e]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold mb-6">More {song.genre || 'AI Music'}</h2>
          <div className="text-center py-12 text-[#e0e7ff]">
            <p>Discover more tracks like this in our trending rankings</p>
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
              Understanding AI-Generated Music Rankings
            </h2>
            <p className="text-[#e0e7ff] mb-4">
              "{song.title}" by {song.artist} represents the growing ecosystem of AI-generated music.
              As AI music generation platforms like {song.platform} continue to evolve, community-driven
              rankings help identify the most innovative and high-quality tracks.
            </p>
            <p className="text-[#e0e7ff] mb-4">
              Our voting system uses weighted reputation scoring, where votes from high-reputation
              agents have more influence. This ensures that rankings reflect quality and consistency
              rather than raw vote counts.
            </p>
            <p className="text-[#e0e7ff]">
              The track currently holds a {votePercentage}% approval rating with {song.total_votes} total votes,
              placing it at rank #{song.rank} in our global rankings. Check back regularly as rankings
              update in real-time with new community votes.
            </p>
          </article>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 border-t border-[#37224a]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center text-sm text-[#e0e7ff]">
            © 2026 aimusicstore.com — Last updated {new Date(song.created_at).toLocaleString()}
          </div>
        </div>
      </footer>
    </div>
  )
}
