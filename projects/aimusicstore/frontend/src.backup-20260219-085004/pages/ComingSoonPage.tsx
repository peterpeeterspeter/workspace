import React, { useState, useEffect } from 'react'
import apiClient from '../api/client'

interface WaitlistResponse {
  success: boolean
  count: number
  message?: string
}

function ComingSoonPage() {
  const [email, setEmail] = useState('')
  const [waitlistCount, setWaitlistCount] = useState(0)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitStatus, setSubmitStatus] = useState<'idle' | 'success' | 'error'>('idle')
  const [statusMessage, setStatusMessage] = useState('')

  // Fetch current waitlist count on mount
  useEffect(() => {
    fetchWaitlistCount()
  }, [])

  const fetchWaitlistCount = async () => {
    try {
      const response = await apiClient.get('/waitlist/count') as WaitlistResponse
      if (response.success) {
        setWaitlistCount(response.count)
      }
    } catch (error) {
      console.error('Failed to fetch waitlist count:', error)
      // Start at 0 if endpoint doesn't exist yet
      setWaitlistCount(0)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!email || !email.includes('@')) {
      setStatusMessage('Please enter a valid email address')
      setSubmitStatus('error')
      return
    }

    setIsSubmitting(true)
    setSubmitStatus('idle')

    try {
      const response = await apiClient.post('/waitlist', { email }) as WaitlistResponse
      
      if (response.success) {
        setSubmitStatus('success')
        setStatusMessage(`Welcome to the waitlist! You're #${response.count} in line.`)
        setWaitlistCount(response.count)
        setEmail('')
      } else {
        setSubmitStatus('error')
        setStatusMessage(response.message || 'Something went wrong. Please try again.')
      }
    } catch (error: any) {
      setSubmitStatus('error')
      setStatusMessage(error.message || 'Failed to join waitlist. Please try again.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-indigo-900 to-blue-900">
      {/* Hero Section */}
      <div className="container mx-auto px-4 py-16 md:py-24">
        <div className="max-w-4xl mx-auto text-center">
          {/* Main Badge */}
          <div className="inline-block mb-6 px-4 py-2 bg-purple-500/20 border border-purple-400/30 rounded-full">
            <span className="text-purple-300 text-sm font-medium">🚀 Coming Soon</span>
          </div>

          {/* Headline */}
          <h1 className="text-4xl md:text-6xl font-bold text-white mb-6 leading-tight">
            Discover the Best AI Music & Tools
          </h1>

          {/* Subhead */}
          <p className="text-lg md:text-xl text-purple-200 mb-8 max-w-2xl mx-auto">
            Community-powered voting. Weighted by reputation. Protected from gaming.
          </p>

          {/* Waitlist Counter */}
          <div className="mb-8">
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-blue-500/20 border border-blue-400/30 rounded-lg">
              <span className="text-blue-300 text-sm">Current waitlist:</span>
              <span className="text-2xl font-bold text-white">{waitlistCount}</span>
              <span className="text-blue-300 text-sm">people</span>
            </div>
          </div>

          {/* Email Form */}
          <form onSubmit={handleSubmit} className="max-w-md mx-auto mb-8">
            <div className="flex flex-col sm:flex-row gap-3">
              <label htmlFor="waitlist-email" className="sr-only">Email address</label>
              <input
                id="waitlist-email"
                type="email"
                inputMode="email"
                autoComplete="email"
                spellCheck={false}
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter your email…"
                aria-describedby="waitlist-status"
                className="flex-1 px-4 py-3 bg-white/10 border border-purple-400/30 rounded-lg text-white placeholder-purple-300/50 focus:outline-none focus:ring-2 focus:ring-purple-400 focus-visible:ring-2 focus-visible:ring-purple-400"
                disabled={isSubmitting}
              />
              <button
                type="submit"
                disabled={isSubmitting}
                className="px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white font-semibold rounded-lg hover:from-purple-600 hover:to-pink-600 transition-all disabled:opacity-50 disabled:cursor-not-allowed focus-visible:ring-2 focus-visible:ring-purple-400"
              >
                {isSubmitting ? 'Joining…' : 'Join Waitlist'}
              </button>
            </div>

            {/* Status Message */}
            {statusMessage && (
              <div
                id="waitlist-status"
                role="status"
                aria-live="polite"
                className={`mt-4 text-center ${
                  submitStatus === 'success' ? 'text-green-400' : 'text-red-400'
                }`}
              >
                {statusMessage}
              </div>
            )}
          </form>

          {/* Value Proposition */}
          <div className="max-w-2xl mx-auto mb-12">
            <div className="grid md:grid-cols-3 gap-6">
              <div className="text-left p-4 bg-white/5 rounded-lg border border-purple-400/20">
                <div className="text-2xl mb-2">✓</div>
                <h3 className="text-white font-semibold mb-2">Weighted Voting</h3>
                <p className="text-purple-200 text-sm">Reputation matters, not 1 person = 1 vote</p>
              </div>

              <div className="text-left p-4 bg-white/5 rounded-lg border border-purple-400/20">
                <div className="text-2xl mb-2">✓</div>
                <h3 className="text-white font-semibold mb-2">Anti-Gaming Protection</h3>
                <p className="text-purple-200 text-sm">Manipulation attempts are blocked</p>
              </div>

              <div className="text-left p-4 bg-white/5 rounded-lg border border-purple-400/20">
                <div className="text-2xl mb-2">✓</div>
                <h3 className="text-white font-semibold mb-2">Real-Time Rankings</h3>
                <p className="text-purple-200 text-sm">Scores update live as votes come in</p>
              </div>
            </div>
          </div>

          {/* Social Proof (Placeholder - will be updated once we have signups) */}
          {waitlistCount > 10 && (
            <div className="text-center text-purple-300 text-sm">
              Join {waitlistCount} early adopters building the most trusted AI music rankings
            </div>
          )}
        </div>
      </div>

      {/* Footer */}
      <div className="container mx-auto px-4 py-8 border-t border-purple-800">
        <div className="text-center text-purple-400 text-sm">
          © 2026 aimusicstore.com - Community-Powered AI Music Rankings
        </div>
      </div>
    </div>
  )
}

export default ComingSoonPage
