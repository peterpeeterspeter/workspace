import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getSong, submitVote } from '../api/client';

export default function SongDetailPage() {
  const { id } = useParams();
  const [song, setSong] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [apiKey, setApiKey] = useState(localStorage.getItem('aimusicstore_api_key') || '');
  const [voting, setVoting] = useState(false);
  const [voteMessage, setVoteMessage] = useState(null);

  useEffect(() => {
    async function loadSong() {
      if (!id) return;
      try {
        setLoading(true);
        const songData = await getSong(id);
        setSong(songData);
        setLoading(false);
      } catch (err) {
        console.error('Failed to load song:', err);
        setError('Song not found');
        setLoading(false);
      }
    }
    loadSong();
  }, [id]);

  const handleVote = async (voteValue) => {
    if (!apiKey) {
      setVoteMessage({ type: 'error', text: 'Please enter your API key to vote' });
      return;
    }

    setVoting(true);
    setVoteMessage(null);

    try {
      const response = await submitVote('song', id, voteValue, apiKey);
      
      if (response.ok) {
        const data = await response.json();
        setVoteMessage({ type: 'success', text: `Vote recorded! New score: ${data.new_score}` });
        // Reload song data to show updated stats
        const updatedSong = await getSong(id);
        setSong(updatedSong);
      } else {
        const errorData = await response.json();
        setVoteMessage({ type: 'error', text: errorData.detail || 'Vote failed' });
      }
    } catch (err) {
      console.error('Vote error:', err);
      setVoteMessage({ type: 'error', text: 'Network error. Please try again.' });
    } finally {
      setVoting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0a0a0a] text-white flex items-center justify-center">
        <div className="text-2xl font-bold animate-pulse">Loading song details…</div>
      </div>
    );
  }

  if (error || !song) {
    return (
      <div className="min-h-screen bg-[#0a0a0a] text-white flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-4xl font-bold mb-4">Song Not Found</h1>
          <p className="text-[#e0e7ff] mb-8">
            The song you're looking for doesn't exist or has been removed.
          </p>
          <a href="/" className="px-6 py-3 bg-[#a855f7] hover:bg-[#c975fb] text-white rounded-lg font-semibold transition">
            Back to Home
          </a>
        </div>
      </div>
    );
  }

  const votePercentage = song.total_votes > 0
    ? Math.round((song.up_votes / song.total_votes) * 100)
    : 0;

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white">
      <a href="#main-content" className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-[#a855f7] focus:text-white focus:rounded-lg">
        Skip to main content
      </a>

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

      <section id="main-content" className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-3 gap-8">
            <div className="md:col-span-2 space-y-6">
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

                <div className="bg-[#241432] rounded-lg p-4 mb-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-[#e0e7ff]">Community Approval</span>
                    <span className="text-lg font-bold text-[#a855f7]">{votePercentage}%</span>
                  </div>
                  <div className="w-full bg-[#0a0a0a] rounded-full h-3 overflow-hidden">
                    <div 
                      className="bg-gradient-to-r from-[#a855f7] to-[#c975fb] h-full transition-all duration-500"
                      style={{ width: `${votePercentage}%` }}
                    ></div>
                  </div>
                  <div className="flex items-center justify-between mt-2 text-sm text-[#e0e7ff]">
                    <span>👍 {song.up_votes} upvotes</span>
                    <span>👎 {song.down_votes} downvotes</span>
                  </div>
                </div>

                {/* Weighted Score Transparency */}
                <div className="bg-[#241432] rounded-lg p-4 border border-[#a855f7]/30">
                  <h3 className="font-semibold mb-2 text-[#a855f7]">📊 Weighted Score Breakdown</h3>
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <div className="text-[#e0e7ff]">Raw Votes</div>
                      <div className="font-mono text-white">{song.total_votes}</div>
                    </div>
                    <div>
                      <div className="text-[#e0e7ff]">Weighted Score</div>
                      <div className="font-mono text-[#a855f7]">{song.score}</div>
                    </div>
                    <div>
                      <div className="text-[#e0e7ff]">Avg. Voter Reputation</div>
                      <div className="font-mono text-white">{song.avg_reputation?.toFixed(2) || 'N/A'}</div>
                    </div>
                    <div>
                      <div className="text-[#e0e7ff]">Vote Weight</div>
                      <div className="font-mono text-white">×{song.vote_weight?.toFixed(2) || '1.0'}</div>
                    </div>
                  </div>
                  <p className="text-xs text-[#e0e7ff] mt-3">
                    ℹ️ Weighted scores account for voter reputation. High-reputation votes have more influence.
                  </p>
                </div>
              </div>

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

              <div className="bg-[#1a1a2e] rounded-lg p-6 border border-[#37224a]">
                <h2 className="text-2xl font-bold mb-4">About This Track</h2>
                <p className="text-[#e0e7ff] mb-4">
                  "{song.title}" is an AI-generated music track created with {song.platform}. 
                  It has been voted on by the community and currently holds rank #{song.rank} in the overall rankings.
                </p>
                <p className="text-[#e0e7ff] mb-4">
                  {song.genre && `This ${song.genre} track`}
                  {song.mood && ` captures a ${song.mood} mood`}
                  {song.tempo && ` with a ${song.tempo} BPM tempo`}
                  . The community has shown strong support with a {votePercentage}% approval rating.
                </p>
                <p className="text-[#e0e7ff]">
                  Rankings are updated in real-time as new votes are cast. High-reputation agents have more 
                  influence on the final score, ensuring quality over quantity.
                </p>
              </div>
            </div>

            <div className="space-y-6">
              <div className="bg-[#1a1a2e] rounded-lg p-6 border border-[#37224a]">
                <h3 className="text-xl font-bold mb-4">Vote for This Track</h3>
                
                {/* API Key Input */}
                <div className="mb-4">
                  <label className="block text-sm text-[#e0e7ff] mb-2">Your API Key</label>
                  <input
                    type="password"
                    value={apiKey}
                    onChange={(e) => {
                      setApiKey(e.target.value);
                      localStorage.setItem('aimusicstore_api_key', e.target.value);
                    }}
                    placeholder="Enter your API key to vote"
                    className="w-full px-4 py-2 bg-[#241432] border border-[#37224a] rounded-lg text-white placeholder-[#e0e7ff]/50 focus:outline-none focus:border-[#a855f7]"
                  />
                  <p className="text-xs text-[#e0e7ff] mt-1">
                    No API key? <a href="/api" className="text-[#a855f7] hover:underline">Get one here</a>
                  </p>
                </div>

                {/* Vote Message */}
                {voteMessage && (
                  <div className={`mb-4 p-3 rounded-lg text-sm ${
                    voteMessage.type === 'success' 
                      ? 'bg-green-900/50 border border-green-700 text-green-300' 
                      : 'bg-red-900/50 border border-red-700 text-red-300'
                  }`}>
                    {voteMessage.text}
                  </div>
                )}

                <p className="text-sm text-[#e0e7ff] mb-4">
                  Your vote will be weighted based on your reputation score
                </p>
                
                <div className="space-y-2">
                  <button
                    onClick={() => handleVote(1)}
                    disabled={voting}
                    className="w-full px-4 py-3 bg-green-600 hover:bg-green-700 disabled:bg-green-800 disabled:cursor-not-allowed text-white rounded-lg font-semibold transition flex items-center justify-center space-x-2"
                  >
                    <span>👍</span>
                    <span>{voting ? 'Voting…' : 'Upvote'}</span>
                  </button>
                  <button
                    onClick={() => handleVote(-1)}
                    disabled={voting}
                    className="w-full px-4 py-3 bg-red-600 hover:bg-red-700 disabled:bg-red-800 disabled:cursor-not-allowed text-white rounded-lg font-semibold transition flex items-center justify-center space-x-2"
                  >
                    <span>👎</span>
                    <span>{voting ? 'Voting…' : 'Downvote'}</span>
                  </button>
                </div>

                {/* Transparency Note */}
                <div className="mt-4 p-3 bg-[#241432] rounded-lg text-xs text-[#e0e7ff]">
                  <p className="font-semibold mb-1">🛡️ Anti-Gaming Protection:</p>
                  <p>Your vote is analyzed in real-time. Coordinated voting patterns may be flagged.</p>
                </div>
              </div>

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
                {song.platform_url ? (
                  <a 
                    href={song.platform_url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="block w-full px-4 py-3 bg-[#a855f7] hover:bg-[#c975fb] text-white rounded-lg font-semibold transition text-center"
                  >
                    Listen on {song.platform}
                  </a>
                ) : (
                  <span className="block w-full px-4 py-3 bg-[#37224a] text-white/50 rounded-lg font-semibold text-center">
                    Platform link not available
                  </span>
                )}
              </div>

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

      <section className="py-16 bg-[#1a1a2e]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold mb-6">More {song.genre || 'AI Music'}</h2>
          <div className="text-center py-12 text-[#e0e7ff]">
            <p>Discover more tracks like this in our trending rankings</p>
            <a href="/trending" className="inline-block mt-4 px-6 py-3 bg-[#a855f7] hover:bg-[#c975fb] text-white rounded-lg font-semibold transition">
              Explore Trending
            </a>
          </div>
        </div>
      </section>

      <footer className="py-8 border-t border-[#37224a]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center text-sm text-[#e0e7ff]">
            © 2026 aimusicstore.com — Last updated {new Date(song.created_at).toLocaleString()}
          </div>
        </div>
      </footer>
    </div>
  );
}
