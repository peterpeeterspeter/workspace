import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
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
    return (_jsxs("div", { className: "relative min-h-screen bg-[#0a0e27]", children: [_jsx("div", { className: "scanlines" }), _jsx("div", { className: "grid-overlay" }), _jsx("div", { className: "noise" }), _jsx(Navbar, {}), _jsxs("main", { children: [_jsx(Hero, {}), _jsx(SocialProof, {}), _jsx(Features, {}), _jsx(HowItWorks, {}), _jsx(TrackPreview, {}), _jsx(AgentShowcase, {}), _jsx(CTASection, {})] }), _jsx(Footer, {})] }));
}
