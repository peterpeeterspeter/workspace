import React from 'react';
import { RocketIcon, ArrowRightIcon } from 'lucide-react';
export function CTASection() {
  return (
    <section className="relative py-32 bg-[#0a0e27] overflow-hidden">
      {/* Background effects */}
      <div className="absolute inset-0">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-[#00ff9f]/10 rounded-full blur-3xl" />
        <div className="absolute top-1/3 left-1/3 w-[400px] h-[400px] bg-[#ff00ff]/10 rounded-full blur-3xl" />
        <div className="absolute bottom-1/3 right-1/3 w-[400px] h-[400px] bg-[#00d9ff]/10 rounded-full blur-3xl" />
      </div>

      {/* Grid lines */}
      <div className="absolute inset-0 opacity-20">
        <div className="absolute top-0 left-1/4 w-px h-full bg-gradient-to-b from-transparent via-[#00ff9f] to-transparent" />
        <div className="absolute top-0 right-1/4 w-px h-full bg-gradient-to-b from-transparent via-[#00ff9f] to-transparent" />
        <div className="absolute top-1/4 left-0 w-full h-px bg-gradient-to-r from-transparent via-[#ff00ff] to-transparent" />
        <div className="absolute bottom-1/4 left-0 w-full h-px bg-gradient-to-r from-transparent via-[#ff00ff] to-transparent" />
      </div>

      <div className="relative z-10 max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        {/* Icon */}
        <div className="inline-flex items-center justify-center w-20 h-20 border-2 border-[#00ff9f] mb-8 pulse-glow">
          <RocketIcon className="w-10 h-10 text-[#00ff9f]" />
        </div>

        {/* Headline */}
        <h2 className="font-['Space_Grotesk'] font-bold text-4xl md:text-6xl text-[#e0e6ed] mb-6">
          Ready to Join the
          <span className="block text-[#00ff9f] neon-text-green">
            AI Music Revolution?
          </span>
        </h2>

        {/* Subheadline */}
        <p className="text-xl md:text-2xl text-[#8b9bb4] mb-12 max-w-2xl mx-auto">
          Start creating, curating, and earning from AI-generated music today.
          No experience required.
        </p>

        {/* CTA Button */}
        <button className="group relative inline-flex items-center gap-4 px-12 py-6 bg-[#00ff9f] text-[#0a0e27] font-['Space_Grotesk'] font-bold text-xl hover:shadow-[0_0_60px_rgba(0,255,159,0.7)] hover:-translate-y-1 transition-all">
          <span>Launch App</span>
          <ArrowRightIcon className="w-6 h-6 group-hover:translate-x-1 transition-transform" />

          {/* Corner accents */}
          <div className="absolute -top-1 -left-1 w-4 h-4 border-t-2 border-l-2 border-[#0a0e27]" />
          <div className="absolute -top-1 -right-1 w-4 h-4 border-t-2 border-r-2 border-[#0a0e27]" />
          <div className="absolute -bottom-1 -left-1 w-4 h-4 border-b-2 border-l-2 border-[#0a0e27]" />
          <div className="absolute -bottom-1 -right-1 w-4 h-4 border-b-2 border-r-2 border-[#0a0e27]" />
        </button>

        {/* Trust badges */}
        <div className="flex flex-wrap justify-center gap-8 mt-12 text-[#8b9bb4] text-sm font-mono">
          <span className="flex items-center gap-2">
            <span className="w-2 h-2 bg-[#00ff9f]" />
            No credit card required
          </span>
          <span className="flex items-center gap-2">
            <span className="w-2 h-2 bg-[#ff00ff]" />
            Free tier available
          </span>
          <span className="flex items-center gap-2">
            <span className="w-2 h-2 bg-[#00d9ff]" />
            Instant payouts
          </span>
        </div>
      </div>
    </section>);

}