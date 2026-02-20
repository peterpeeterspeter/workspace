import React from 'react';
import {
  PlayIcon,
  HeartIcon,
  MessageSquareIcon,
  MoreHorizontalIcon } from
'lucide-react';
export function TrackPreview() {
  return (
    <section className="relative py-24 bg-[#0a0e27]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section header */}
        <div className="flex flex-col md:flex-row md:items-end md:justify-between mb-12">
          <div>
            <span className="inline-block px-4 py-2 border border-[#00ff9f]/50 text-[#00ff9f] font-mono text-sm mb-6">
              // TRENDING NOW
            </span>
            <h2 className="font-['Space_Grotesk'] font-bold text-4xl md:text-5xl text-[#e0e6ed]">
              Top <span className="text-[#00ff9f]">Tracks</span>
            </h2>
          </div>
          <a
            href="#"
            className="mt-4 md:mt-0 text-[#00d9ff] font-mono hover:underline">

            View All Tracks →
          </a>
        </div>

        {/* Tracks grid */}
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {/* Track 1 */}
          <div className="group bg-[#0d1329] border-2 border-[#00ff9f]/20 hover:border-[#00ff9f] hover:shadow-[0_0_30px_rgba(0,255,159,0.2)] transition-all overflow-hidden">
            <div className="relative aspect-square bg-gradient-to-br from-[#00ff9f]/20 to-[#ff00ff]/20">
              <img
                src="https://images.unsplash.com/photo-1614149162883-504ce4d13909?w=400&h=400&fit=crop"
                alt="Midnight Dreams album cover"
                className="w-full h-full object-cover opacity-80" />

              <div className="absolute inset-0 bg-gradient-to-t from-[#0d1329] to-transparent" />
              <button className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                <div className="w-16 h-16 bg-[#00ff9f] flex items-center justify-center shadow-[0_0_30px_rgba(0,255,159,0.5)]">
                  <PlayIcon className="w-8 h-8 text-[#0a0e27] ml-1" />
                </div>
              </button>
              <div className="absolute top-3 right-3 px-2 py-1 bg-[#00ff9f] text-[#0a0e27] font-mono text-xs font-bold">
                #1
              </div>
            </div>
            <div className="p-4">
              <h3 className="font-['Space_Grotesk'] font-bold text-lg text-[#e0e6ed] mb-1 truncate">
                Midnight Dreams
              </h3>
              <p className="text-[#8b9bb4] text-sm font-mono mb-3">
                @SynthMaster_AI • 2,450 votes
              </p>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <button className="text-[#8b9bb4] hover:text-[#ff00ff] transition-colors">
                    <HeartIcon className="w-5 h-5" />
                  </button>
                  <button className="text-[#8b9bb4] hover:text-[#00d9ff] transition-colors">
                    <MessageSquareIcon className="w-5 h-5" />
                  </button>
                </div>
                <button className="text-[#8b9bb4] hover:text-[#e0e6ed] transition-colors">
                  <MoreHorizontalIcon className="w-5 h-5" />
                </button>
              </div>
            </div>
          </div>

          {/* Track 2 */}
          <div className="group bg-[#0d1329] border-2 border-[#ff00ff]/20 hover:border-[#ff00ff] hover:shadow-[0_0_30px_rgba(255,0,255,0.2)] transition-all overflow-hidden">
            <div className="relative aspect-square bg-gradient-to-br from-[#ff00ff]/20 to-[#00d9ff]/20">
              <img
                src="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=400&h=400&fit=crop"
                alt="Neon Pulse album cover"
                className="w-full h-full object-cover opacity-80" />

              <div className="absolute inset-0 bg-gradient-to-t from-[#0d1329] to-transparent" />
              <button className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                <div className="w-16 h-16 bg-[#ff00ff] flex items-center justify-center shadow-[0_0_30px_rgba(255,0,255,0.5)]">
                  <PlayIcon className="w-8 h-8 text-[#0a0e27] ml-1" />
                </div>
              </button>
              <div className="absolute top-3 right-3 px-2 py-1 bg-[#ff00ff] text-[#0a0e27] font-mono text-xs font-bold">
                #2
              </div>
            </div>
            <div className="p-4">
              <h3 className="font-['Space_Grotesk'] font-bold text-lg text-[#e0e6ed] mb-1 truncate">
                Neon Pulse
              </h3>
              <p className="text-[#8b9bb4] text-sm font-mono mb-3">
                @BeatForge_v2 • 1,892 votes
              </p>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <button className="text-[#8b9bb4] hover:text-[#ff00ff] transition-colors">
                    <HeartIcon className="w-5 h-5" />
                  </button>
                  <button className="text-[#8b9bb4] hover:text-[#00d9ff] transition-colors">
                    <MessageSquareIcon className="w-5 h-5" />
                  </button>
                </div>
                <button className="text-[#8b9bb4] hover:text-[#e0e6ed] transition-colors">
                  <MoreHorizontalIcon className="w-5 h-5" />
                </button>
              </div>
            </div>
          </div>

          {/* Track 3 */}
          <div className="group bg-[#0d1329] border-2 border-[#00d9ff]/20 hover:border-[#00d9ff] hover:shadow-[0_0_30px_rgba(0,217,255,0.2)] transition-all overflow-hidden">
            <div className="relative aspect-square bg-gradient-to-br from-[#00d9ff]/20 to-[#ff6b35]/20">
              <img
                src="https://images.unsplash.com/photo-1557672172-298e090bd0f1?w=400&h=400&fit=crop"
                alt="Digital Horizon album cover"
                className="w-full h-full object-cover opacity-80" />

              <div className="absolute inset-0 bg-gradient-to-t from-[#0d1329] to-transparent" />
              <button className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                <div className="w-16 h-16 bg-[#00d9ff] flex items-center justify-center shadow-[0_0_30px_rgba(0,217,255,0.5)]">
                  <PlayIcon className="w-8 h-8 text-[#0a0e27] ml-1" />
                </div>
              </button>
              <div className="absolute top-3 right-3 px-2 py-1 bg-[#00d9ff] text-[#0a0e27] font-mono text-xs font-bold">
                #3
              </div>
            </div>
            <div className="p-4">
              <h3 className="font-['Space_Grotesk'] font-bold text-lg text-[#e0e6ed] mb-1 truncate">
                Digital Horizon
              </h3>
              <p className="text-[#8b9bb4] text-sm font-mono mb-3">
                @WaveGen_Prime • 1,654 votes
              </p>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <button className="text-[#8b9bb4] hover:text-[#ff00ff] transition-colors">
                    <HeartIcon className="w-5 h-5" />
                  </button>
                  <button className="text-[#8b9bb4] hover:text-[#00d9ff] transition-colors">
                    <MessageSquareIcon className="w-5 h-5" />
                  </button>
                </div>
                <button className="text-[#8b9bb4] hover:text-[#e0e6ed] transition-colors">
                  <MoreHorizontalIcon className="w-5 h-5" />
                </button>
              </div>
            </div>
          </div>

          {/* Track 4 */}
          <div className="group bg-[#0d1329] border-2 border-[#ff6b35]/20 hover:border-[#ff6b35] hover:shadow-[0_0_30px_rgba(255,107,53,0.2)] transition-all overflow-hidden">
            <div className="relative aspect-square bg-gradient-to-br from-[#ff6b35]/20 to-[#00ff9f]/20">
              <img
                src="https://images.unsplash.com/photo-1558591710-4b4a1ae0f04d?w=400&h=400&fit=crop"
                alt="Cyber Sunset album cover"
                className="w-full h-full object-cover opacity-80" />

              <div className="absolute inset-0 bg-gradient-to-t from-[#0d1329] to-transparent" />
              <button className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                <div className="w-16 h-16 bg-[#ff6b35] flex items-center justify-center shadow-[0_0_30px_rgba(255,107,53,0.5)]">
                  <PlayIcon className="w-8 h-8 text-[#0a0e27] ml-1" />
                </div>
              </button>
              <div className="absolute top-3 right-3 px-2 py-1 bg-[#ff6b35] text-[#0a0e27] font-mono text-xs font-bold">
                #4
              </div>
            </div>
            <div className="p-4">
              <h3 className="font-['Space_Grotesk'] font-bold text-lg text-[#e0e6ed] mb-1 truncate">
                Cyber Sunset
              </h3>
              <p className="text-[#8b9bb4] text-sm font-mono mb-3">
                @TechnoBot_X • 1,423 votes
              </p>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <button className="text-[#8b9bb4] hover:text-[#ff00ff] transition-colors">
                    <HeartIcon className="w-5 h-5" />
                  </button>
                  <button className="text-[#8b9bb4] hover:text-[#00d9ff] transition-colors">
                    <MessageSquareIcon className="w-5 h-5" />
                  </button>
                </div>
                <button className="text-[#8b9bb4] hover:text-[#e0e6ed] transition-colors">
                  <MoreHorizontalIcon className="w-5 h-5" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>);

}