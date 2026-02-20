import React from 'react';
import { Navbar } from '../components/Navbar';
import { Hero } from '../components/Hero';
import { SocialProof } from '../components/SocialProof';
import { Features } from '../components/Features';
import { HowItWorks } from '../components/HowItWorks';
import { TrackPreview } from '../components/TrackPreview';
import { AgentShowcase } from '../components/AgentShowcase';
import { CTASection } from '../components/CTASection';
import { Footer } from '../components/Footer';
export function HomePage() {
  return (
    <div className="relative min-h-screen bg-[#0a0e27]">
      {/* Global effects */}
      <div className="scanlines" />
      <div className="grid-overlay" />
      <div className="noise" />

      {/* Navigation */}
      <Navbar />

      {/* Main content */}
      <main>
        <Hero />
        <SocialProof />
        <Features />
        <HowItWorks />
        <TrackPreview />
        <AgentShowcase />
        <CTASection />
      </main>

      {/* Footer */}
      <Footer />
    </div>);

}