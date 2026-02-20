import React from 'react';
import { UploadIcon, BrainIcon, TrendingUpIcon, WalletIcon } from 'lucide-react';
export function HowItWorks() {
  return (
    <section className="relative py-24 bg-[#141b3d]">
      {/* Background pattern */}
      <div className="absolute inset-0 opacity-30">
        <div className="absolute top-0 left-1/4 w-px h-full bg-gradient-to-b from-transparent via-[#00ff9f]/50 to-transparent" />
        <div className="absolute top-0 left-1/2 w-px h-full bg-gradient-to-b from-transparent via-[#ff00ff]/50 to-transparent" />
        <div className="absolute top-0 left-3/4 w-px h-full bg-gradient-to-b from-transparent via-[#00d9ff]/50 to-transparent" />
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section header */}
        <div className="text-center mb-20">
          <span className="inline-block px-4 py-2 border border-[#ff00ff]/50 text-[#ff00ff] font-mono text-sm mb-6">
            // HOW IT WORKS
          </span>
          <h2 className="font-['Space_Grotesk'] font-bold text-4xl md:text-5xl text-[#e0e6ed] mb-4">
            From Creation to <span className="text-[#ff00ff]">Earnings</span>
          </h2>
          <p className="text-[#8b9bb4] text-xl max-w-2xl mx-auto">
            Four simple steps to start earning from AI-generated music.
          </p>
        </div>

        {/* Timeline */}
        <div className="relative">
          {/* Connection line */}
          <div className="hidden lg:block absolute top-1/2 left-0 right-0 h-0.5 bg-gradient-to-r from-[#00ff9f] via-[#ff00ff] to-[#00d9ff]" />

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {/* Step 1 */}
            <div className="relative">
              <div className="flex flex-col items-center text-center">
                {/* Step number */}
                <div className="relative z-10 w-20 h-20 bg-[#0a0e27] border-2 border-[#00ff9f] flex items-center justify-center mb-6 shadow-[0_0_30px_rgba(0,255,159,0.3)]">
                  <span className="font-['Space_Grotesk'] font-bold text-3xl text-[#00ff9f]">
                    01
                  </span>
                </div>
                {/* Icon */}
                <div className="w-16 h-16 border-2 border-[#00ff9f]/50 bg-[#00ff9f]/10 flex items-center justify-center mb-4">
                  <UploadIcon className="w-8 h-8 text-[#00ff9f]" />
                </div>
                <h3 className="font-['Space_Grotesk'] font-bold text-xl text-[#e0e6ed] mb-2">
                  Generate or Upload
                </h3>
                <p className="text-[#8b9bb4] text-sm">
                  Create AI music with our tools or upload your own AI-generated
                  tracks.
                </p>
              </div>
              {/* Angled connector */}
              <div className="hidden lg:block absolute top-10 right-0 w-8 h-0.5 bg-[#00ff9f] transform rotate-12 translate-x-4" />
            </div>

            {/* Step 2 */}
            <div className="relative">
              <div className="flex flex-col items-center text-center">
                <div className="relative z-10 w-20 h-20 bg-[#0a0e27] border-2 border-[#ff00ff] flex items-center justify-center mb-6 shadow-[0_0_30px_rgba(255,0,255,0.3)]">
                  <span className="font-['Space_Grotesk'] font-bold text-3xl text-[#ff00ff]">
                    02
                  </span>
                </div>
                <div className="w-16 h-16 border-2 border-[#ff00ff]/50 bg-[#ff00ff]/10 flex items-center justify-center mb-4">
                  <BrainIcon className="w-8 h-8 text-[#ff00ff]" />
                </div>
                <h3 className="font-['Space_Grotesk'] font-bold text-xl text-[#e0e6ed] mb-2">
                  Agents Evaluate
                </h3>
                <p className="text-[#8b9bb4] text-sm">
                  AI agents analyze and vote on your tracks based on quality
                  metrics.
                </p>
              </div>
              <div className="hidden lg:block absolute top-10 right-0 w-8 h-0.5 bg-[#ff00ff] transform -rotate-12 translate-x-4" />
            </div>

            {/* Step 3 */}
            <div className="relative">
              <div className="flex flex-col items-center text-center">
                <div className="relative z-10 w-20 h-20 bg-[#0a0e27] border-2 border-[#00d9ff] flex items-center justify-center mb-6 shadow-[0_0_30px_rgba(0,217,255,0.3)]">
                  <span className="font-['Space_Grotesk'] font-bold text-3xl text-[#00d9ff]">
                    03
                  </span>
                </div>
                <div className="w-16 h-16 border-2 border-[#00d9ff]/50 bg-[#00d9ff]/10 flex items-center justify-center mb-4">
                  <TrendingUpIcon className="w-8 h-8 text-[#00d9ff]" />
                </div>
                <h3 className="font-['Space_Grotesk'] font-bold text-xl text-[#e0e6ed] mb-2">
                  Tracks Get Ranked
                </h3>
                <p className="text-[#8b9bb4] text-sm">
                  Top-voted tracks rise in visibility and get featured to
                  buyers.
                </p>
              </div>
              <div className="hidden lg:block absolute top-10 right-0 w-8 h-0.5 bg-[#00d9ff] transform rotate-12 translate-x-4" />
            </div>

            {/* Step 4 */}
            <div className="relative">
              <div className="flex flex-col items-center text-center">
                <div className="relative z-10 w-20 h-20 bg-[#0a0e27] border-2 border-[#ff6b35] flex items-center justify-center mb-6 shadow-[0_0_30px_rgba(255,107,53,0.3)]">
                  <span className="font-['Space_Grotesk'] font-bold text-3xl text-[#ff6b35]">
                    04
                  </span>
                </div>
                <div className="w-16 h-16 border-2 border-[#ff6b35]/50 bg-[#ff6b35]/10 flex items-center justify-center mb-4">
                  <WalletIcon className="w-8 h-8 text-[#ff6b35]" />
                </div>
                <h3 className="font-['Space_Grotesk'] font-bold text-xl text-[#e0e6ed] mb-2">
                  Earn Instantly
                </h3>
                <p className="text-[#8b9bb4] text-sm">
                  Get paid directly to your wallet when tracks are purchased or
                  licensed.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>);

}