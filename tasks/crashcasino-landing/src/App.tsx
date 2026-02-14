import { siteConfig } from './config/site'
import './App.css'

function App() {
  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white">
      {/* Hero Section */}
      <section className="relative px-6 py-20 lg:py-32 overflow-hidden">
        {/* Background gradient */}
        <div className="absolute inset-0 bg-gradient-to-br from-[#0a0a0a] via-[#0f1f0f] to-[#0a0a0a] opacity-50" />

        {/* Animated grid pattern */}
        <div className="absolute inset-0 bg-[linear-gradient(rgba(0,255,136,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(0,255,136,0.03)_1px,transparent_1px)] bg-[size:60px_60px] [mask-image:radial-gradient(ellipse_60%_60%_at_50%_50%,black,transparent)]" />

        <div className="relative max-w-7xl mx-auto">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-[#00ff88]/10 border border-[#00ff88]/20 mb-8">
            <span className="w-2 h-2 rounded-full bg-[#00ff88] animate-pulse" />
            <span className="text-sm font-medium text-[#00ff88]">{siteConfig.hero.badge}</span>
          </div>

          {/* Title */}
          <h1 className="text-5xl md:text-7xl lg:text-8xl font-bold leading-tight mb-6">
            {siteConfig.hero.title.split('\n').map((line, i) => (
              <span key={i} className="block">
                {line}
                {i === 1 && <span className="text-[#00ff88]">.</span>}
              </span>
            ))}
          </h1>

          {/* Subtitle */}
          <p className="text-xl md:text-2xl text-gray-400 max-w-3xl mb-12 leading-relaxed">
            {siteConfig.hero.subtitle}
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4">
            <a
              href={siteConfig.hero.cta.href}
              className="px-8 py-4 bg-[#00ff88] text-black font-semibold rounded-lg hover:bg-[#00ff88]/90 transition-all duration-300 text-center"
            >
              {siteConfig.hero.cta.text}
            </a>
            <a
              href={siteConfig.hero.secondaryCta.href}
              className="px-8 py-4 border border-gray-700 text-white font-semibold rounded-lg hover:border-[#00ff88] hover:text-[#00ff88] transition-all duration-300 text-center"
            >
              {siteConfig.hero.secondaryCta.text}
            </a>
          </div>
        </div>
      </section>

      {/* Methodology Section */}
      <section id="methodology" className="py-20 px-6 bg-[#0f0f0f]">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl md:text-5xl font-bold mb-4">{siteConfig.methodology.title}</h2>
          <p className="text-xl text-gray-400 mb-12">{siteConfig.methodology.subtitle}</p>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {siteConfig.methodology.steps.map((step, i) => (
              <div key={i} className="p-6 rounded-xl bg-[#1a1a1a] border border-gray-800 hover:border-[#00ff88]/30 transition-all duration-300">
                <div className="text-4xl mb-4">{step.icon}</div>
                <h3 className="text-xl font-semibold mb-2">{step.title}</h3>
                <p className="text-gray-400">{step.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Verified Casinos Section */}
      <section id="verified" className="py-20 px-6">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl md:text-5xl font-bold mb-4">Verified Safe Casinos</h2>
          <p className="text-xl text-gray-400 mb-12">12 casinos passed all our verification checks</p>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {siteConfig.verifiedCasinos.map((casino, i) => (
              <div key={i} className="p-6 rounded-xl bg-[#1a1a1a] border border-gray-800 hover:border-[#00ff88] transition-all duration-300">
                <div className="flex items-start justify-between mb-4">
                  <h3 className="text-2xl font-bold">{casino.name}</h3>
                  <div className="flex items-center gap-2">
                    <span className="text-2xl font-bold text-[#00ff88]">{casino.rating}</span>
                    {casino.verified && <span className="text-[#00ff88]">✓</span>}
                  </div>
                </div>

                {casino.badge && (
                  <div className="inline-block px-3 py-1 bg-[#00ff88]/10 border border-[#00ff88]/20 rounded-full text-sm text-[#00ff88] mb-4">
                    {casino.badge}
                  </div>
                )}

                <ul className="space-y-2 mb-6">
                  {casino.features.map((feature, j) => (
                    <li key={j} className="flex items-center gap-2 text-gray-300">
                      <span className="text-[#00ff88]">✓</span>
                      {feature}
                    </li>
                  ))}
                </ul>

                <a
                  href={casino.link}
                  target="_blank"
                  rel="nofollow noopener"
                  className="block w-full px-6 py-3 bg-[#00ff88] text-black font-semibold rounded-lg hover:bg-[#00ff88]/90 transition-all duration-300 text-center"
                >
                  Play Now
                </a>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Red Flags Section */}
      <section id="flags" className="py-20 px-6 bg-[#0f0f0f]">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl md:text-5xl font-bold mb-4">{siteConfig.redFlags.title}</h2>
          <p className="text-xl text-gray-400 mb-12">{siteConfig.redFlags.subtitle}</p>

          <div className="grid md:grid-cols-2 gap-6">
            {siteConfig.redFlags.flags.map((flag, i) => (
              <div key={i} className="p-6 rounded-xl bg-[#1a1a1a] border border-red-900/30 hover:border-red-500/50 transition-all duration-300">
                <div className="flex items-start gap-4">
                  <div className="text-3xl">{flag.icon}</div>
                  <div>
                    <h3 className="text-xl font-semibold mb-2">{flag.title}</h3>
                    <p className="text-gray-400">{flag.description}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section id="faq" className="py-20 px-6">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl md:text-5xl font-bold mb-12 text-center">Frequently Asked Questions</h2>

          <div className="space-y-4">
            {siteConfig.faq.map((item, i) => (
              <details key={i} className="group">
                <summary className="flex items-center justify-between p-6 rounded-xl bg-[#1a1a1a] border border-gray-800 hover:border-[#00ff88]/30 cursor-pointer transition-all duration-300">
                  <span className="text-lg font-semibold">{item.q}</span>
                  <span className="text-2xl text-gray-500 group-open:text-[#00ff88] transition-colors">+</span>
                </summary>
                <div className="p-6 pt-0 text-gray-400">
                  {item.a}
                </div>
              </details>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-6 bg-[#050505] border-t border-gray-900">
        <div className="max-w-7xl mx-auto">
          <p className="text-2xl font-bold text-[#00ff88] mb-8">{siteConfig.footer.tagline}</p>

          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-8">
            <div className="flex flex-wrap gap-6">
              {siteConfig.footer.links.map((link, i) => (
                <a key={i} href={link.href} className="text-gray-400 hover:text-white transition-colors">
                  {link.label}
                </a>
              ))}
            </div>

            <div className="flex flex-wrap gap-6">
              {siteConfig.footer.legal.map((link, i) => (
                <a key={i} href={link.href} className="text-sm text-gray-500 hover:text-gray-300 transition-colors">
                  {link.label}
                </a>
              ))}
            </div>
          </div>

          <p className="mt-8 text-sm text-gray-600">
            © 2026 {siteConfig.name}. All rights reserved. Gamble responsibly.
          </p>
        </div>
      </footer>
    </div>
  )
}

export default App
