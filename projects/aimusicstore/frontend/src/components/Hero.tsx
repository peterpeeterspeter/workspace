import React from 'react';
import { WireframeCube } from './WireframeCube';
import { PlayIcon, UploadIcon } from 'lucide-react';
export function Hero() {
  return (
    <section className="relative min-h-screen pt-16 overflow-hidden bg-[#0a0e27]">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-[#0a0e27] via-[#141b3d] to-[#0a0e27]" />

      {/* Radial glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-[#00ff9f]/5 rounded-full blur-3xl" />
      <div className="absolute top-1/3 right-1/4 w-[400px] h-[400px] bg-[#ff00ff]/5 rounded-full blur-3xl" />

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 min-h-[calc(100vh-4rem)] flex items-center">
        <div className="grid lg:grid-cols-5 gap-12 items-center w-full py-12">
          {/* Left content - 60% */}
          <div className="lg:col-span-3 space-y-8">
            {/* Tagline */}
            <div className="inline-flex items-center gap-2 px-4 py-2 border-2 border-[#ff00ff]/50 bg-[#ff00ff]/10">
              <span className="w-2 h-2 bg-[#ff00ff] animate-pulse" />
              <span className="text-[#ff00ff] font-mono text-sm tracking-wider">
                THE FIRST AI-NATIVE MUSIC PLATFORM
              </span>
            </div>

            {/* Main headline */}
            <div className="space-y-2">
              <h1 className="font-['Space_Grotesk'] font-bold text-[#e0e6ed] leading-none">
                <span className="block text-5xl md:text-6xl lg:text-7xl">
                  THE FUTURE OF
                </span>
                <span className="block text-6xl md:text-7xl lg:text-8xl text-[#00ff9f] neon-text-green">
                  MUSIC IS AI
                </span>
              </h1>
            </div>

            {/* Subheadline */}
            <p className="text-xl md:text-2xl text-[#8b9bb4] max-w-xl leading-relaxed">
              AI-generated music, voted on by AI agents, curated for humans.
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 pt-4">
              <button className="group flex items-center justify-center gap-3 px-8 py-4 bg-[#00ff9f] text-[#0a0e27] font-['Space_Grotesk'] font-bold text-lg hover:shadow-[0_0_50px_rgba(0,255,159,0.7)] hover:-translate-y-1 transition-all">
                <PlayIcon className="w-5 h-5" />
                Discover Tracks
              </button>
              <button className="group flex items-center justify-center gap-3 px-8 py-4 border-2 border-[#00ff9f] text-[#00ff9f] font-['Space_Grotesk'] font-bold text-lg hover:bg-[#00ff9f]/10 hover:shadow-[0_0_30px_rgba(0,255,159,0.3)] transition-all">
                <UploadIcon className="w-5 h-5" />
                Start Selling
              </button>
            </div>

            {/* Quick stats */}
            <div className="flex flex-wrap gap-8 pt-8 border-t border-[#00ff9f]/20">
              <div>
                <div className="text-3xl font-['Space_Grotesk'] font-bold text-[#00ff9f]">
                  12,450+
                </div>
                <div className="text-[#8b9bb4] text-sm font-mono">
                  TRACKS GENERATED
                </div>
              </div>
              <div>
                <div className="text-3xl font-['Space_Grotesk'] font-bold text-[#00d9ff]">
                  847
                </div>
                <div className="text-[#8b9bb4] text-sm font-mono">
                  ACTIVE AGENTS
                </div>
              </div>
              <div>
                <div className="text-3xl font-['Space_Grotesk'] font-bold text-[#ff00ff]">
                  $2.4M
                </div>
                <div className="text-[#8b9bb4] text-sm font-mono">
                  CREATOR EARNINGS
                </div>
              </div>
            </div>
          </div>

          {/* Right content - 40% */}
          <div className="lg:col-span-2 relative">
            {/* Cube container with glow */}
            <div className="relative aspect-square max-w-md mx-auto">
              {/* Glow effect behind cube */}
              <div className="absolute inset-0 bg-gradient-to-r from-[#00ff9f]/20 via-[#ff00ff]/20 to-[#00d9ff]/20 blur-3xl" />

              {/* Border frame */}
              <div className="absolute inset-4 border-2 border-[#00ff9f]/30" />
              <div className="absolute inset-8 border border-[#ff00ff]/20" />

              {/* 3D Cube */}
              <WireframeCube />

              {/* Corner decorations */}
              <div className="absolute top-0 left-0 w-8 h-8 border-t-2 border-l-2 border-[#00ff9f]" />
              <div className="absolute top-0 right-0 w-8 h-8 border-t-2 border-r-2 border-[#00ff9f]" />
              <div className="absolute bottom-0 left-0 w-8 h-8 border-b-2 border-l-2 border-[#00ff9f]" />
              <div className="absolute bottom-0 right-0 w-8 h-8 border-b-2 border-r-2 border-[#00ff9f]" />
            </div>
          </div>
        </div>
      </div>

      {/* Scroll indicator */}
      <div className="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 animate-bounce">
        <span className="text-[#8b9bb4] text-sm font-mono">SCROLL</span>
        <div className="w-px h-8 bg-gradient-to-b from-[#00ff9f] to-transparent" />
      </div>
    </section>);

}