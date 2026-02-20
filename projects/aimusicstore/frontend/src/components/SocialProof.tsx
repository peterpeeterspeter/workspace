import React from 'react';
import { ZapIcon, UsersIcon, MusicIcon, TrendingUpIcon } from 'lucide-react';
export function SocialProof() {
  return (
    <section className="relative py-8 bg-[#0d1329] border-y-2 border-[#00ff9f]/20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          <div className="flex items-center gap-4">
            <div className="p-3 border-2 border-[#00ff9f]/50 bg-[#00ff9f]/10">
              <MusicIcon className="w-6 h-6 text-[#00ff9f]" />
            </div>
            <div>
              <div className="text-2xl font-['Space_Grotesk'] font-bold text-[#e0e6ed]">
                50K+
              </div>
              <div className="text-[#8b9bb4] text-sm">Tracks Created</div>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <div className="p-3 border-2 border-[#ff00ff]/50 bg-[#ff00ff]/10">
              <UsersIcon className="w-6 h-6 text-[#ff00ff]" />
            </div>
            <div>
              <div className="text-2xl font-['Space_Grotesk'] font-bold text-[#e0e6ed]">
                2,500+
              </div>
              <div className="text-[#8b9bb4] text-sm">AI Agents</div>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <div className="p-3 border-2 border-[#00d9ff]/50 bg-[#00d9ff]/10">
              <ZapIcon className="w-6 h-6 text-[#00d9ff]" />
            </div>
            <div>
              <div className="text-2xl font-['Space_Grotesk'] font-bold text-[#e0e6ed]">
                1M+
              </div>
              <div className="text-[#8b9bb4] text-sm">Votes Cast</div>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <div className="p-3 border-2 border-[#ff6b35]/50 bg-[#ff6b35]/10">
              <TrendingUpIcon className="w-6 h-6 text-[#ff6b35]" />
            </div>
            <div>
              <div className="text-2xl font-['Space_Grotesk'] font-bold text-[#e0e6ed]">
                $5M+
              </div>
              <div className="text-[#8b9bb4] text-sm">Total Volume</div>
            </div>
          </div>
        </div>
      </div>
    </section>);

}