import React, { useState } from 'react';
import { MenuIcon, XIcon } from 'lucide-react';
export function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-[#0a0e27]/90 backdrop-blur-sm border-b-2 border-[#00ff9f]/20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <a href="/" className="flex items-center gap-2 group">
            <div className="w-8 h-8 border-2 border-[#00ff9f] flex items-center justify-center group-hover:shadow-[0_0_20px_rgba(0,255,159,0.5)] transition-shadow">
              <span className="text-[#00ff9f] font-bold text-sm font-mono">
                AI
              </span>
            </div>
            <span className="text-[#e0e6ed] font-['Space_Grotesk'] font-bold text-lg tracking-tight">
              AIMusicStore
            </span>
          </a>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-8">
            <a
              href="#discover"
              className="text-[#8b9bb4] hover:text-[#00d9ff] transition-colors font-medium">

              Discover
            </a>
            <a
              href="#agents"
              className="text-[#8b9bb4] hover:text-[#00d9ff] transition-colors font-medium">

              Agents
            </a>
            <a
              href="#sell"
              className="text-[#8b9bb4] hover:text-[#00d9ff] transition-colors font-medium">

              Sell Music
            </a>
            <a
              href="#docs"
              className="text-[#8b9bb4] hover:text-[#00d9ff] transition-colors font-medium">

              Docs
            </a>
          </div>

          {/* CTA Buttons */}
          <div className="hidden md:flex items-center gap-4">
            <button className="px-4 py-2 text-[#00ff9f] border-2 border-[#00ff9f] font-['Space_Grotesk'] font-semibold hover:bg-[#00ff9f]/10 hover:shadow-[0_0_20px_rgba(0,255,159,0.3)] transition-all">
              Connect Wallet
            </button>
            <button className="px-4 py-2 bg-[#00ff9f] text-[#0a0e27] font-['Space_Grotesk'] font-bold hover:shadow-[0_0_30px_rgba(0,255,159,0.5)] hover:-translate-y-0.5 transition-all">
              Launch App
            </button>
          </div>

          {/* Mobile menu button */}
          <button
            className="md:hidden p-2 text-[#00ff9f]"
            onClick={() => setIsOpen(!isOpen)}
            aria-label={isOpen ? 'Close menu' : 'Open menu'}>

            {isOpen ?
            <XIcon className="w-6 h-6" /> :

            <MenuIcon className="w-6 h-6" />
            }
          </button>
        </div>

        {/* Mobile Navigation */}
        {isOpen &&
        <div className="md:hidden border-t-2 border-[#00ff9f]/20 py-4">
            <div className="flex flex-col gap-4">
              <a
              href="#discover"
              className="text-[#8b9bb4] hover:text-[#00d9ff] transition-colors font-medium px-2 py-2">

                Discover
              </a>
              <a
              href="#agents"
              className="text-[#8b9bb4] hover:text-[#00d9ff] transition-colors font-medium px-2 py-2">

                Agents
              </a>
              <a
              href="#sell"
              className="text-[#8b9bb4] hover:text-[#00d9ff] transition-colors font-medium px-2 py-2">

                Sell Music
              </a>
              <a
              href="#docs"
              className="text-[#8b9bb4] hover:text-[#00d9ff] transition-colors font-medium px-2 py-2">

                Docs
              </a>
              <div className="flex flex-col gap-3 pt-4 border-t border-[#00ff9f]/20">
                <button className="w-full px-4 py-3 text-[#00ff9f] border-2 border-[#00ff9f] font-['Space_Grotesk'] font-semibold">
                  Connect Wallet
                </button>
                <button className="w-full px-4 py-3 bg-[#00ff9f] text-[#0a0e27] font-['Space_Grotesk'] font-bold">
                  Launch App
                </button>
              </div>
            </div>
          </div>
        }
      </div>
    </nav>);

}