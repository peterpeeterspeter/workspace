import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getTrending, getWaitlistCount } from '../api/client';

export default function HomePage() {
  const [trending, setTrending] = useState(null);
  const [waitlistCount, setWaitlistCount] = useState(147);
  const [loading, setLoading] = useState(true);
  const [emailInput, setEmailInput] = useState('');
  const [waitlistMessage, setWaitlistMessage] = useState(null);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    async function loadData() {
      try {
        const [trendingData, waitlistData] = await Promise.all([
          getTrending(),
          getWaitlistCount()
        ]);
        setTrending(trendingData);
        if (waitlistData.success) {
          setWaitlistCount(waitlistData.count + 147);
        }
        setLoading(false);
      } catch (error) {
        console.error('Failed to load data:', error);
        setLoading(false);
      }
    }
    loadData();
    
    const interval = setInterval(loadData, 60000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleWaitlistSubmit = async (e) => {
    e.preventDefault();
    if (!emailInput) return;

    try {
      const response = await fetch('/api/v1/waitlist', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: emailInput })
      });
      const data = await response.json();
      if (data.success) {
        setWaitlistMessage({ type: 'success', text: '🎉 You\'re on the list! We\'ll notify you when we launch.' });
        setWaitlistCount(prev => prev + 1);
      } else {
        setWaitlistMessage({ type: 'error', text: data.message || 'Something went wrong.' });
      }
    } catch (err) {
      setWaitlistMessage({ type: 'error', text: 'Network error. Please try again.' });
    }
    setEmailInput('');
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-[#0f0f23] via-[#1a1a2e] to-[#16213e]">
        <div className="text-center">
          <div className="w-16 h-16 mx-auto mb-4 border-4 border-purple-500 border-t-transparent rounded-full animate-spin"></div>
          <div className="text-white text-2xl font-bold">Loading aimusicstore…</div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0f0f23] text-white overflow-x-hidden">
      {/* Animated Background */}
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute inset-0 bg-gradient-to-br from-purple-900/20 via-transparent to-pink-900/20 animate-pulse"></div>
        <div className="absolute inset-0" style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M30 0l60 30 30 60 0 30-30-30z' fill='none' stroke='%238b5cf610' stroke-width='1'/%3E%3C/svg%3E")`,
        }}></div>
      </div>

      {/* Navigation */}
      <nav className={`fixed top-0 w-full z-50 transition-all duration-300 ${scrolled ? 'bg-[#0f0f23]/95 backdrop-blur-md border-b border-purple-500/20' : 'bg-transparent'}`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <Link to="/" className="flex items-center space-x-3 group">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center transform group-hover:scale-110 transition">
                <span className="text-xl">🎵</span>
              </div>
              <span className="text-xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
                aimusicstore
              </span>
            </Link>
            
            <div className="hidden md:flex items-center space-x-8">
              <Link to="/trending" className="text-white/80 hover:text-white transition font-medium">Trending</Link>
              <Link to="/top" className="text-white/80 hover:text-white transition font-medium">Top 50</Link>
              <a href="#api" className="text-white/80 hover:text-white transition font-medium">API</a>
              <Link to="/waitlist" className="px-4 py-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg font-semibold hover:shadow-lg hover:shadow-purple-500/25 transition-all">
                Join Waitlist
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center pt-16">
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center">
            {/* Badge */}
            <div className="inline-flex items-center space-x-2 bg-purple-500/20 border border-purple-500/30 rounded-full px-4 py-2 mb-8 animate-bounce">
              <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
              <span className="text-sm font-semibold text-purple-300">Now Live — Anti-Gaming Protection Active</span>
            </div>

            {/* Main Heading */}
            <h1 className="text-5xl sm:text-6xl md:text-7xl font-extrabold mb-6 leading-tight">
              <span className="bg-gradient-to-r from-purple-400 via-pink-400 to-purple-400 bg-clip-text text-transparent animate-gradient">
                AI Music Rankings
              </span>
              <br />
              <span className="text-white">Without the BS</span>
            </h1>

            {/* Subheading */}
            <p className="text-xl md:text-2xl text-purple-200 mb-12 max-w-3xl mx-auto leading-relaxed">
              Community-powered voting for AI-generated music and tools. 
              <span className="text-white font-semibold"> Weighted by reputation.</span>{' '}
              <span className="text-white font-semibold">Protected from gaming.</span>
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16">
              <Link 
                to="/trending"
                className="group px-8 py-4 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl font-bold text-lg hover:shadow-2xl hover:shadow-purple-500/30 transition-all transform hover:scale-105 flex items-center space-x-2"
              >
                <span>Explore Rankings</span>
                <span className="transform group-hover:translate-x-1 transition">→</span>
              </Link>
              <Link 
                to="/waitlist"
                className="px-8 py-4 bg-white/10 backdrop-blur-sm border-2 border-white/20 rounded-xl font-bold text-lg hover:bg-white/20 transition-all"
              >
                Get Early Access
              </Link>
            </div>

            {/* Social Proof */}
            <div className="flex items-center justify-center space-x-8 text-sm text-purple-300">
              <div className="flex items-center space-x-2">
                <span className="text-2xl">🔥</span>
                <span className="font-semibold">{waitlistCount.toLocaleString()} on waitlist</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-2xl">🛡️</span>
                <span>Anti-gaming active</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-2xl">⚖️</span>
                <span>Weighted voting</span>
              </div>
            </div>
          </div>

          {/* Scroll Indicator */}
          <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
            <div className="w-6 h-10 border-2 border-purple-400/50 rounded-full flex justify-center">
              <div className="w-1 h-3 bg-purple-400 rounded-full mt-2 animate-pulse"></div>
            </div>
          </div>
        </div>
      </section>

      {/* Problem Section */}
      <section className="py-20 bg-gradient-to-b from-transparent to-red-950/20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              The Problem with <span className="text-red-400">AI Music Rankings</span>
            </h2>
            <p className="text-xl text-purple-200 max-w-3xl mx-auto">
              Current ranking systems are broken. Here's what we're fixing:
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: '🤖',
                title: 'Upvote Bots',
                description: 'Botnets create 100 fake accounts in 10 minutes to manipulate rankings'
              },
              {
                icon: '👥',
                title: 'Voting Rings',
                description: 'Discord servers coordinate mass upvotes for specific tracks'
              },
              {
                icon: '🎭',
                title: 'Self-Voting',
                description: 'Creators boost their own tracks with dozens of fake accounts'
              }
            ].map((problem, idx) => (
              <div key={idx} className="group bg-red-950/30 border border-red-500/20 rounded-2xl p-8 hover:border-red-500/40 transition-all">
                <div className="text-5xl mb-4 transform group-hover:scale-110 transition">{problem.icon}</div>
                <h3 className="text-2xl font-bold mb-3 text-red-400">{problem.title}</h3>
                <p className="text-purple-200 leading-relaxed">{problem.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Solution Section */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Our <span className="text-green-400">Solution</span>
            </h2>
            <p className="text-xl text-purple-200 max-w-3xl mx-auto">
              Three innovations that make aimusicstore different:
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: '⚖️',
                title: 'Weighted Voting',
                description: 'High-reputation voters have more influence. Quality beats quantity.',
                color: 'purple'
              },
              {
                icon: '🛡️',
                title: 'Anti-Gaming System',
                description: 'Real-time detection prevents coordinated attacks and manipulation.',
                color: 'green'
              },
              {
                icon: '📊',
                title: 'Full Transparency',
                description: 'Every vote is visible, timestamped, and attributed. No black boxes.',
                color: 'blue'
              }
            ].map((solution, idx) => (
              <div key={idx} className="group bg-gradient-to-br from-white/5 to-white/[0.02] border border-white/10 rounded-2xl p-8 hover:border-white/20 transition-all transform hover:-translate-y-2">
                <div className={`w-16 h-16 rounded-xl bg-${solution.color}-500/20 flex items-center justify-center mb-6 text-4xl transform group-hover:scale-110 transition`}>
                  {solution.icon}
                </div>
                <h3 className="text-2xl font-bold mb-3">{solution.title}</h3>
                <p className="text-purple-200 leading-relaxed">{solution.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Trending Section */}
      {trending && (
        <section className="py-20 bg-gradient-to-b from-transparent to-purple-950/20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between mb-12">
              <div>
                <h2 className="text-4xl md:text-5xl font-bold mb-2">Trending Now</h2>
                <p className="text-purple-300">Top AI music and tools this week</p>
              </div>
              <div className="hidden md:flex items-center space-x-2 bg-green-500/20 border border-green-500/30 rounded-full px-4 py-2">
                <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
                <span className="text-sm font-semibold text-green-400">Live</span>
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-8">
              {/* Songs */}
              <div className="bg-gradient-to-br from-white/5 to-white/[0.02] border border-white/10 rounded-2xl p-8">
                <div className="flex items-center space-x-3 mb-6">
                  <span className="text-4xl">🎵</span>
                  <h3 className="text-2xl font-bold">Top Songs</h3>
                </div>
                <div className="space-y-3">
                  {trending.songs.slice(0, 5).map((song) => (
                    <Link 
                      key={song.id}
                      to={`/songs/${song.id}`}
                      className="group block bg-white/5 border border-white/10 rounded-xl p-4 hover:bg-white/10 hover:border-purple-500/30 transition-all"
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center space-x-3 mb-2">
                            <span className="text-2xl font-bold text-purple-400">#{song.rank}</span>
                            <div>
                              <h4 className="font-semibold group-hover:text-purple-400 transition">{song.title}</h4>
                              <p className="text-sm text-purple-300">{song.artist}</p>
                            </div>
                          </div>
                          <div className="flex items-center space-x-2 text-sm">
                            <span className="px-2 py-1 bg-purple-500/20 rounded text-purple-300">{song.platform}</span>
                            {song.genre && <span className="text-purple-300">{song.genre}</span>}
                          </div>
                        </div>
                        <div className="text-right ml-4">
                          <div className="text-2xl font-bold text-purple-400">{song.score}</div>
                          <div className="text-xs text-purple-300">score</div>
                        </div>
                      </div>
                    </Link>
                  ))}
                </div>
              </div>

              {/* Tools */}
              <div className="bg-gradient-to-br from-white/5 to-white/[0.02] border border-white/10 rounded-2xl p-8">
                <div className="flex items-center space-x-3 mb-6">
                  <span className="text-4xl">🛠️</span>
                  <h3 className="text-2xl font-bold">Top Tools</h3>
                </div>
                <div className="space-y-3">
                  {trending.tools.slice(0, 5).map((tool) => (
                    <Link 
                      key={tool.id}
                      to={`/tools/${tool.id}`}
                      className="group block bg-white/5 border border-white/10 rounded-xl p-4 hover:bg-white/10 hover:border-purple-500/30 transition-all"
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center space-x-3 mb-2">
                            <span className="text-2xl font-bold text-purple-400">#{tool.rank}</span>
                            <div>
                              <h4 className="font-semibold group-hover:text-purple-400 transition">{tool.name}</h4>
                              <a 
                                href={tool.website}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-sm text-purple-300 hover:text-purple-400 transition"
                                onClick={(e) => e.stopPropagation()}
                              >
                                {tool.website}
                              </a>
                            </div>
                          </div>
                          <span className="px-2 py-1 bg-purple-500/20 rounded text-purple-300 text-sm">{tool.category}</span>
                        </div>
                        <div className="text-right ml-4">
                          <div className="text-2xl font-bold text-purple-400">{tool.score}</div>
                          <div className="text-xs text-purple-300">score</div>
                        </div>
                      </div>
                    </Link>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </section>
      )}

      {/* Waitlist Section */}
      <section className="py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-gradient-to-br from-purple-900/30 to-pink-900/30 border border-purple-500/30 rounded-3xl p-12 text-center">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Join the <span className="bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">Future</span> of AI Music
            </h2>
            <p className="text-xl text-purple-200 mb-8">
              Be among the first to experience the next generation of music discovery.
            </p>

            <form onSubmit={handleWaitlistSubmit} className="max-w-md mx-auto mb-6">
              <div className="flex flex-col sm:flex-row gap-3">
                <input
                  type="email"
                  value={emailInput}
                  onChange={(e) => setEmailInput(e.target.value)}
                  placeholder="Enter your email"
                  required
                  className="flex-1 px-6 py-4 bg-white/10 border border-white/20 rounded-xl text-white placeholder-purple-300 focus:outline-none focus:border-purple-500 transition"
                />
                <button 
                  type="submit"
                  className="px-8 py-4 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl font-bold hover:shadow-2xl hover:shadow-purple-500/30 transition-all transform hover:scale-105"
                >
                  Get Early Access
                </button>
              </div>
            </form>

            {waitlistMessage && (
              <div className={`max-w-md mx-auto p-4 rounded-xl ${
                waitlistMessage.type === 'success' 
                  ? 'bg-green-500/20 border border-green-500/30 text-green-300' 
                  : 'bg-red-500/20 border border-red-500/30 text-red-300'
              }`}>
                {waitlistMessage.text}
              </div>
            )}

            <div className="flex items-center justify-center space-x-6 text-sm text-purple-300">
              <div className="flex items-center space-x-2">
                <span>✓</span>
                <span>Early access</span>
              </div>
              <div className="flex items-center space-x-2">
                <span>✓</span>
                <span>Reputation boost</span>
              </div>
              <div className="flex items-center space-x-2">
                <span>✓</span>
                <span>Exclusive updates</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* API Section */}
      <section id="api" className="py-20 bg-gradient-to-b from-transparent to-blue-950/20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl md:text-5xl font-bold mb-4">API for Developers</h2>
            <p className="text-xl text-purple-200">Integrate AI music rankings into your applications</p>
          </div>

          <div className="bg-gradient-to-br from-white/5 to-white/[0.02] border border-white/10 rounded-2xl p-8">
            <div className="grid md:grid-cols-2 gap-8">
              <div>
                <h3 className="text-2xl font-bold mb-4">Quick Start</h3>
                <div className="bg-black/50 rounded-xl p-6 font-mono text-sm overflow-x-auto">
                  <pre className="text-purple-300">
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
                <h3 className="text-2xl font-bold mb-4">API Tiers</h3>
                <div className="space-y-4">
                  {[
                    { name: 'Free', votes: '100/day', desc: 'Perfect for testing' },
                    { name: 'Pro', votes: '1,000/day', desc: 'For growing apps' },
                    { name: 'Enterprise', votes: 'Unlimited', desc: 'High-volume use' }
                  ].map((tier, idx) => (
                    <div key={idx} className={`p-4 rounded-xl border ${idx === 2 ? 'bg-purple-500/20 border-purple-500/30' : 'bg-white/5 border-white/10'}`}>
                      <div className="flex justify-between items-center mb-2">
                        <span className="font-bold">{tier.name}</span>
                        <span className="text-purple-300">{tier.votes}</span>
                      </div>
                      <p className="text-sm text-purple-200">{tier.desc}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 border-t border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
                  <span className="text-xl">🎵</span>
                </div>
                <span className="font-bold text-lg">aimusicstore</span>
              </div>
              <p className="text-sm text-purple-300">AI music rankings without the BS</p>
            </div>

            <div>
              <h3 className="font-semibold mb-3">Explore</h3>
              <ul className="space-y-2 text-sm text-purple-300">
                <li><Link to="/trending" className="hover:text-white transition">Trending</Link></li>
                <li><Link to="/top" className="hover:text-white transition">Top 50</Link></li>
                <li><Link to="/waitlist" className="hover:text-white transition">Join Waitlist</Link></li>
              </ul>
            </div>

            <div>
              <h3 className="font-semibold mb-3">Resources</h3>
              <ul className="space-y-2 text-sm text-purple-300">
                <li><a href="https://docs.aimusicstore.com" target="_blank" rel="noopener noreferrer" className="hover:text-white transition">Documentation</a></li>
                <li><a href="https://docs.aimusicstore.com/api" target="_blank" rel="noopener noreferrer" className="hover:text-white transition">API Reference</a></li>
                <li><a href="https://status.aimusicstore.com" target="_blank" rel="noopener noreferrer" className="hover:text-white transition">Status</a></li>
              </ul>
            </div>

            <div>
              <h3 className="font-semibold mb-3">Legal</h3>
              <ul className="space-y-2 text-sm text-purple-300">
                <li><a href="/privacy" className="hover:text-white transition">Privacy</a></li>
                <li><a href="/terms" className="hover:text-white transition">Terms</a></li>
                <li><a href="/affiliate-disclosure" className="hover:text-white transition">Affiliate Disclosure</a></li>
              </ul>
            </div>
          </div>

          <div className="pt-8 border-t border-white/10 text-center text-sm text-purple-300">
            <p>© 2026 aimusicstore.com. Built for AI music creators, by AI music creators.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
