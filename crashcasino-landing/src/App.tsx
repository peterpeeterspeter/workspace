import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'

function App() {
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 50)
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  return (
    <div className="min-h-screen bg-black text-white overflow-x-hidden">
      {/* Animated Header */}
      <motion.header 
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 ${scrolled ? 'bg-black/90 backdrop-blur-xl border-b border-white/10' : ''}`}
      >
        <div className="max-w-7xl mx-auto px-6 py-6 flex items-center justify-between">
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="text-3xl font-black tracking-tighter"
          >
            <span className="text-lime-400">CRASH</span>CASINO
          </motion.div>
          <motion.nav 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
            className="hidden md:flex items-center gap-8 text-sm font-medium"
          >
            <a href="#methodology" className="hover:text-lime-400 transition-colors">METHOD</a>
            <a href="#verified" className="hover:text-lime-400 transition-colors">VERIFIED</a>
            <a href="#compare" className="hover:text-lime-400 transition-colors">COMPARE</a>
          </motion.nav>
        </div>
      </motion.header>

      {/* Hero Section - Bold & Dramatic */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
        {/* Dramatic Background */}
        <div className="absolute inset-0">
          <div className="absolute inset-0 bg-gradient-to-br from-black via-gray-900 to-black"></div>
          <div className="absolute top-1/4 left-1/4 w-[600px] h-[600px] bg-lime-500/20 rounded-full blur-[150px] animate-pulse"></div>
          <div className="absolute bottom-1/4 right-1/4 w-[400px] h-[400px] bg-emerald-500/20 rounded-full blur-[120px] animate-pulse delay-1000"></div>
          
          {/* Grid Pattern */}
          <div className="absolute inset-0 opacity-10" style={{
            backgroundImage: 'linear-gradient(to right, #333 1px, transparent 1px), linear-gradient(to bottom, #333 1px, transparent 1px)',
            backgroundSize: '60px 60px'
          }}></div>
        </div>

        <div className="relative z-10 max-w-6xl mx-auto px-6 text-center">
          {/* Animated Badge */}
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2, duration: 0.5 }}
            className="inline-flex items-center gap-3 px-6 py-3 rounded-full border-2 border-lime-500/50 bg-lime-500/10 mb-8"
          >
            <span className="relative flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-lime-500 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-lime-500"></span>
            </span>
            <span className="text-sm font-bold text-lime-400 tracking-wider">INVESTIGATION COMPLETE</span>
          </motion.div>

          {/* Dramatic Title */}
          <motion.h1
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3, duration: 0.6 }}
            className="text-7xl md:text-8xl lg:text-9xl font-black leading-[0.9] tracking-tight mb-6"
          >
            <div className="block">
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-white to-gray-400">CRASH</span>
              <span className="text-lime-400">.</span>
            </div>
            <div className="block text-5xl md:text-6xl lg:text-7xl">
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-lime-400 to-emerald-400">GAMBLING</span>
            </div>
            <div className="block mt-4 text-4xl md:text-5xl text-white/90">
              IS IT <span className="relative inline-block">
                RIGGED
                <svg className="absolute -bottom-2 left-0 w-full h-3 text-red-500" viewBox="0 0 200 9" fill="none">
                  <path d="M2 6.5C50 3.5 150 3.5 198 6.5" stroke="currentColor" strokeWidth="3" strokeLinecap="round"/>
                </svg>
              </span>?
            </div>
          </motion.h1>

          {/* Subtitle */}
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
            className="text-xl md:text-2xl text-gray-400 max-w-3xl mx-auto mb-12 leading-relaxed"
          >
            We tested <span className="text-white font-semibold">50 crash casinos</span>. 
            Only <span className="text-lime-400 font-bold">12 passed</span> every test.
            <span className="block mt-3 text-white/80">Here's what we found.</span>
          </motion.p>

          {/* CTA Buttons */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
            className="flex flex-col sm:flex-row items-center justify-center gap-4"
          >
            <a 
              href="#verified" 
              className="group relative px-10 py-5 bg-lime-500 text-black font-black text-lg rounded-lg hover:bg-lime-400 transition-all duration-300 shadow-[0_0_40px_rgba(132,204,22,0.3)] hover:shadow-[0_0_60px_rgba(132,204,22,0.5)] hover:-translate-y-1"
            >
              <span className="relative z-10">SEE VERIFIED SITES</span>
              <div className="absolute inset-0 rounded-lg bg-gradient-to-r from-lime-400 to-emerald-400 opacity-0 group-hover:opacity-100 transition-opacity"></div>
            </a>
            <a 
              href="#methodology" 
              className="px-10 py-5 border-2 border-white/20 text-white font-semibold text-lg rounded-lg hover:bg-white/10 hover:border-white/40 transition-all duration-300"
            >
              OUR METHODOLOGY
            </a>
          </motion.div>

          {/* Stats Bar */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.7 }}
            className="mt-16 grid grid-cols-3 gap-8 max-w-2xl mx-auto"
          >
            <div className="text-center">
              <div className="text-4xl font-black text-lime-400">50</div>
              <div className="text-xs text-gray-500 tracking-wider">SITES TESTED</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-black text-red-500">76%</div>
              <div className="text-xs text-gray-500 tracking-wider">FAILED</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-black text-emerald-400">12</div>
              <div className="text-xs text-gray-500 tracking-wider">VERIFIED</div>
            </div>
          </motion.div>
        </div>

        {/* Scroll Indicator */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1, duration: 1 }}
          className="absolute bottom-10 left-1/2 -translate-x-1/2"
        >
          <div className="flex flex-col items-center gap-2 text-gray-500">
            <span className="text-xs tracking-widest">SCROLL TO DISCOVER</span>
            <motion.div
              animate={{ y: [0, 10, 0] }}
              transition={{ duration: 1.5, repeat: Infinity }}
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
              </svg>
            </motion.div>
          </div>
        </motion.div>
      </section>

      {/* Methodology Section */}
      <section id="methodology" className="py-32 bg-gradient-to-b from-black to-gray-900">
        <div className="max-w-7xl mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-20"
          >
            <h2 className="text-5xl md:text-6xl font-black mb-6 tracking-tight">
              HOW WE <span className="text-lime-400">TEST</span>
            </h2>
            <p className="text-xl text-gray-400">5-step rigorous testing process. Every site audited.</p>
          </motion.div>

          <div className="grid md:grid-cols-2 gap-16 items-center">
            <div>
              {[
                { step: '01', title: 'Provably Fair Check', desc: 'SHA-256 hash verification, server & client seed analysis' },
                { step: '02', title: 'RTP Audit', desc: 'House edge calculation, payout percentage verification' },
                { step: '03', title: 'Real Withdrawals', desc: 'We deposit & withdraw. Speed & reliability tested.' },
                { step: '04', title: 'License Verify', desc: 'Jurisdiction check, authenticity confirmation' },
                { step: '05', title: 'Security Test', desc: 'SSL, data privacy, 2FA, account protection' }
              ].map((item, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, x: -20 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.1 }}
                  className="flex gap-6 py-6 border-b border-white/5 last:border-0"
                >
                  <span className="text-5xl font-black text-lime-400/50">{item.step}</span>
                  <div>
                    <h3 className="text-xl font-bold mb-1">{item.title}</h3>
                    <p className="text-gray-500 text-sm">{item.desc}</p>
                  </div>
                </motion.div>
              ))}
            </div>

            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              className="bg-gradient-to-br from-gray-900 to-black rounded-3xl p-12 border border-lime-500/20 text-center"
            >
              <div className="text-8xl font-black text-red-500 mb-2">76%</div>
              <div className="text-2xl font-bold mb-3">FAILED RATE</div>
              <p className="text-gray-400">Most crash casinos fail at least one critical test.<br/>We only recommend sites that pass all five.</p>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Verified Sites - Card Grid */}
      <section id="verified" className="py-32 bg-black">
        <div className="max-w-7xl mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <div className="inline-block px-4 py-2 bg-lime-500/10 border border-lime-500/30 rounded-full text-lime-400 text-sm font-bold mb-4">
              VERIFIED & APPROVED
            </div>
            <h2 className="text-5xl md:text-6xl font-black mb-4 tracking-tight">
              THE <span className="text-lime-400">12</span> THAT PASSED
            </h2>
            <p className="text-xl text-gray-400">Licensed, provably fair, fast payouts. Tested by us.</p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              { name: 'Cybet', tag: 'BEGINNER FRIENDLY', bonus: '$10,000', highlight: '$0.10 min bets' },
              { name: 'Betzrd', tag: 'NO DEPOSIT', bonus: 'FREE BONUS', highlight: 'Risk-free trial' },
              { name: '7Bit', tag: 'ESTABLISHED', bonus: '325% BONUS', highlight: 'Since 2014' },
              { name: 'Mirax', tag: 'HUGE VARIETY', bonus: '12 BTC', highlight: '15+ crash games' }
            ].map((casino, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                whileHover={{ y: -5 }}
                className="group bg-gradient-to-br from-gray-900 to-black rounded-2xl p-6 border border-white/10 hover:border-lime-500/30 transition-all duration-300"
              >
                <div className="text-xs font-bold text-lime-400 mb-3">{casino.tag}</div>
                <h3 className="text-2xl font-black mb-2">{casino.name}</h3>
                <p className="text-3xl font-bold text-white mb-2">{casino.bonus}</p>
                <p className="text-sm text-gray-500 mb-4">{casino.highlight}</p>
                <div className="flex items-center gap-2 text-sm text-gray-400">
                  <svg className="w-4 h-4 text-lime-500" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <span>Passed All Tests</span>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Red Flags - Warning Section */}
      <section id="red-flags" className="py-32 bg-gradient-to-b from-gray-900 to-black">
        <div className="max-w-7xl mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16 max-w-3xl mx-auto"
          >
            <div className="inline-block px-4 py-2 bg-red-500/10 border border-red-500/30 rounded-full text-red-500 text-sm font-bold mb-4">
              WARNING SIGNS
            </div>
            <h2 className="text-5xl md:text-6xl font-black mb-4 tracking-tight">
              RED FLAGS <span className="text-red-500">WE FOUND</span>
            </h2>
            <p className="text-xl text-gray-400">These appeared in 76% of sites tested. Avoid crash casinos showing these patterns.</p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-6 max-w-5xl mx-auto">
            {[
              'No provably fair verification',
              'Slow or blocked withdrawals',
              'Fake/expired gambling licenses',
              '"Guaranteed win" claims',
              'Poor or no customer support',
              'Hidden terms & unfair conditions'
            ].map((flag, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, scale: 0.9 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.05 }}
                className="bg-red-950/30 border-l-4 border-red-500 rounded-lg p-5"
              >
                <p className="text-gray-300 font-medium">{flag}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ - Accordion */}
      <section id="faq" className="py-32 bg-black">
        <div className="max-w-3xl mx-auto px-6">
          <motion.h2
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-5xl md:text-6xl font-black text-center mb-16 tracking-tight"
          >
            COMMON <span className="text-lime-400">QUESTIONS</span>
          </motion.h2>

          <div className="space-y-4">
            {[
              {
                q: 'How long does testing take?',
                a: 'Each site undergoes 7-14 days of continuous testing. Real deposits, 100+ rounds, withdrawal tests, provably fair verification.'
              },
              {
                q: 'Do casinos pay for reviews?',
                a: 'No. We accept affiliate commissions from verified sites, but never let this affect our recommendations. 76% of sites are rejected.'
              },
              {
                q: 'What is provably fair?',
                a: 'A cryptographic system verifying every game round was fair. We check SHA-256 hashes, server seeds, client seeds to ensure games aren\'t rigged.'
              },
              {
                q: 'How often do you re-test?',
                a: 'Every 3 months. Casinos can change policies overnight. We continuously monitor verified sites and re-audit quarterly.'
              }
            ].map((item, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 10 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.05 }}
                className="bg-gray-900 rounded-xl overflow-hidden"
              >
                <h3 className="px-8 py-5 font-bold text-lg border-b border-white/5">{item.q}</h3>
                <p className="px-8 pb-5 text-gray-400 leading-relaxed">{item.a}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-16 bg-black border-t border-white/10">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center">
            <div className="text-4xl font-black mb-4">
              <span className="text-lime-400">CRASH</span>CASINO
            </div>
            <p className="text-gray-500 mb-6">Testing crash casinos for fairness, safety, and transparency.</p>
            <div className="flex items-center justify-center gap-6 text-sm text-gray-500">
              <a href="#" className="hover:text-lime-400 transition-colors">Privacy</a>
              <span>·</span>
              <a href="#" className="hover:text-lime-400 transition-colors">Terms</a>
              <span>·</span>
              <a href="#" className="hover:text-lime-400 transition-colors">Contact</a>
            </div>
            <div className="mt-8 text-sm text-gray-600">
              © 2026 CrashCasino.io. Play responsibly. 18+ only.
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App
