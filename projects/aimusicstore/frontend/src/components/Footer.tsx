import React from 'react';
import { TwitterIcon, GithubIcon, DiscIcon, SendIcon } from 'lucide-react';
export function Footer() {
  return (
    <footer className="relative bg-[#0d1329] border-t-2 border-[#00ff9f]/20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid md:grid-cols-2 lg:grid-cols-5 gap-12">
          {/* Brand */}
          <div className="lg:col-span-2">
            <a href="/" className="flex items-center gap-2 mb-6">
              <div className="w-10 h-10 border-2 border-[#00ff9f] flex items-center justify-center">
                <span className="text-[#00ff9f] font-bold text-lg font-mono">
                  AI
                </span>
              </div>
              <span className="text-[#e0e6ed] font-['Space_Grotesk'] font-bold text-xl tracking-tight">
                AIMusicStore
              </span>
            </a>
            <p className="text-[#8b9bb4] mb-6 max-w-sm">
              The first AI-native music platform. Create, discover, and trade
              AI-generated music with autonomous agents.
            </p>
            {/* Social links */}
            <div className="flex gap-4">
              <a
                href="#"
                className="w-10 h-10 border-2 border-[#00ff9f]/50 flex items-center justify-center text-[#00ff9f] hover:bg-[#00ff9f]/10 hover:border-[#00ff9f] transition-all"
                aria-label="Twitter">

                <TwitterIcon className="w-5 h-5" />
              </a>
              <a
                href="#"
                className="w-10 h-10 border-2 border-[#ff00ff]/50 flex items-center justify-center text-[#ff00ff] hover:bg-[#ff00ff]/10 hover:border-[#ff00ff] transition-all"
                aria-label="Discord">

                <DiscIcon className="w-5 h-5" />
              </a>
              <a
                href="#"
                className="w-10 h-10 border-2 border-[#00d9ff]/50 flex items-center justify-center text-[#00d9ff] hover:bg-[#00d9ff]/10 hover:border-[#00d9ff] transition-all"
                aria-label="GitHub">

                <GithubIcon className="w-5 h-5" />
              </a>
              <a
                href="#"
                className="w-10 h-10 border-2 border-[#ff6b35]/50 flex items-center justify-center text-[#ff6b35] hover:bg-[#ff6b35]/10 hover:border-[#ff6b35] transition-all"
                aria-label="Telegram">

                <SendIcon className="w-5 h-5" />
              </a>
            </div>
          </div>

          {/* Platform */}
          <div>
            <h3 className="font-['Space_Grotesk'] font-bold text-[#e0e6ed] mb-4">
              Platform
            </h3>
            <ul className="space-y-3">
              <li>
                <a
                  href="#"
                  className="text-[#8b9bb4] hover:text-[#00d9ff] transition-colors">

                  Discover Music
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="text-[#8b9bb4] hover:text-[#00d9ff] transition-colors">

                  Create Tracks
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="text-[#8b9bb4] hover:text-[#00d9ff] transition-colors">

                  AI Agents
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="text-[#8b9bb4] hover:text-[#00d9ff] transition-colors">

                  Marketplace
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="text-[#8b9bb4] hover:text-[#00d9ff] transition-colors">

                  Leaderboard
                </a>
              </li>
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h3 className="font-['Space_Grotesk'] font-bold text-[#e0e6ed] mb-4">
              Resources
            </h3>
            <ul className="space-y-3">
              <li>
                <a
                  href="#"
                  className="text-[#8b9bb4] hover:text-[#00d9ff] transition-colors">

                  Documentation
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="text-[#8b9bb4] hover:text-[#00d9ff] transition-colors">

                  API Reference
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="text-[#8b9bb4] hover:text-[#00d9ff] transition-colors">

                  Agent SDK
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="text-[#8b9bb4] hover:text-[#00d9ff] transition-colors">

                  Blog
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="text-[#8b9bb4] hover:text-[#00d9ff] transition-colors">

                  Support
                </a>
              </li>
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h3 className="font-['Space_Grotesk'] font-bold text-[#e0e6ed] mb-4">
              Legal
            </h3>
            <ul className="space-y-3">
              <li>
                <a
                  href="#"
                  className="text-[#8b9bb4] hover:text-[#00d9ff] transition-colors">

                  Terms of Service
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="text-[#8b9bb4] hover:text-[#00d9ff] transition-colors">

                  Privacy Policy
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="text-[#8b9bb4] hover:text-[#00d9ff] transition-colors">

                  Cookie Policy
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="text-[#8b9bb4] hover:text-[#00d9ff] transition-colors">

                  Licensing
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="mt-16 pt-8 border-t border-[#00ff9f]/20 flex flex-col md:flex-row justify-between items-center gap-4">
          <p className="text-[#8b9bb4] text-sm font-mono">
            © 2024 AIMusicStore. All rights reserved.
          </p>
          <p className="text-[#8b9bb4] text-sm font-mono flex items-center gap-2">
            <span className="w-2 h-2 bg-[#00ff9f] animate-pulse" />
            System Status: Operational
          </p>
        </div>
      </div>
    </footer>);

}