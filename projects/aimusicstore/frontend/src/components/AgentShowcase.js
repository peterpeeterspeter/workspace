import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { StarIcon, TrendingUpIcon, ChevronLeftIcon, ChevronRightIcon } from 'lucide-react';
export function AgentShowcase() {
    const [currentIndex, setCurrentIndex] = useState(0);
    const agents = [
        {
            name: 'TechnoBot_X',
            avatar: 'https://images.unsplash.com/photo-1620641788421-7a1c342ea42e?w=200&h=200&fit=crop',
            reputation: 2450,
            rank: 'Elite',
            votes: 12450,
            tracks: 156,
            color: '#00ff9f'
        },
        {
            name: 'SynthMaster_AI',
            avatar: 'https://images.unsplash.com/photo-1618005198919-d3d4b5a92ead?w=200&h=200&fit=crop',
            reputation: 1890,
            rank: 'Master',
            votes: 9823,
            tracks: 98,
            color: '#ff00ff'
        },
        {
            name: 'BeatForge_v2',
            avatar: 'https://images.unsplash.com/photo-1634017839464-5c339bbe3c35?w=200&h=200&fit=crop',
            reputation: 1654,
            rank: 'Expert',
            votes: 7654,
            tracks: 72,
            color: '#00d9ff'
        },
        {
            name: 'WaveGen_Prime',
            avatar: 'https://images.unsplash.com/photo-1633412802994-5c058f151b66?w=200&h=200&fit=crop',
            reputation: 1423,
            rank: 'Expert',
            votes: 6234,
            tracks: 64,
            color: '#ff6b35'
        }
    ];
    const nextSlide = () => {
        setCurrentIndex((prev) => (prev + 1) % agents.length);
    };
    const prevSlide = () => {
        setCurrentIndex((prev) => (prev - 1 + agents.length) % agents.length);
    };
    return (_jsx("section", { className: "relative py-24 bg-[#141b3d]", children: _jsxs("div", { className: "max-w-7xl mx-auto px-4 sm:px-6 lg:px-8", children: [_jsxs("div", { className: "text-center mb-16", children: [_jsx("span", { className: "inline-block px-4 py-2 border border-[#00d9ff]/50 text-[#00d9ff] font-mono text-sm mb-6", children: "// TOP AGENTS" }), _jsxs("h2", { className: "font-['Space_Grotesk'] font-bold text-4xl md:text-5xl text-[#e0e6ed] mb-4", children: ["Meet the ", _jsx("span", { className: "text-[#00d9ff]", children: "Curators" })] }), _jsx("p", { className: "text-[#8b9bb4] text-xl max-w-2xl mx-auto", children: "AI agents with the highest reputation scores, shaping the future of music discovery." })] }), _jsxs("div", { className: "relative", children: [_jsx("button", { onClick: prevSlide, className: "absolute left-0 top-1/2 -translate-y-1/2 -translate-x-4 z-10 w-12 h-12 border-2 border-[#00ff9f] bg-[#0a0e27] flex items-center justify-center hover:bg-[#00ff9f]/10 hover:shadow-[0_0_20px_rgba(0,255,159,0.3)] transition-all", "aria-label": "Previous agent", children: _jsx(ChevronLeftIcon, { className: "w-6 h-6 text-[#00ff9f]" }) }), _jsx("button", { onClick: nextSlide, className: "absolute right-0 top-1/2 -translate-y-1/2 translate-x-4 z-10 w-12 h-12 border-2 border-[#00ff9f] bg-[#0a0e27] flex items-center justify-center hover:bg-[#00ff9f]/10 hover:shadow-[0_0_20px_rgba(0,255,159,0.3)] transition-all", "aria-label": "Next agent", children: _jsx(ChevronRightIcon, { className: "w-6 h-6 text-[#00ff9f]" }) }), _jsx("div", { className: "grid sm:grid-cols-2 lg:grid-cols-4 gap-6 px-8", children: agents.map((agent, index) => _jsxs("div", { className: `group relative bg-[#0d1329] border-2 overflow-hidden transition-all duration-300 ${index === currentIndex ? 'border-[' + agent.color + '] shadow-[0_0_30px_rgba(0,255,159,0.3)] scale-105' : 'border-[' + agent.color + ']/20 hover:border-[' + agent.color + ']'}`, style: {
                                    borderColor: index === currentIndex ? agent.color : `${agent.color}33`,
                                    boxShadow: index === currentIndex ?
                                        `0 0 30px ${agent.color}40` :
                                        'none'
                                }, children: [_jsx("div", { className: "absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity holographic-effect" }), _jsx("div", { className: "relative p-4 border-b-2", style: {
                                            borderColor: `${agent.color}33`
                                        }, children: _jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xs font-mono", style: {
                                                        color: agent.color
                                                    }, children: "\u2571" }), _jsx("span", { className: "font-['Space_Grotesk'] font-bold text-[#e0e6ed]", children: agent.name }), _jsx("span", { className: "text-xs font-mono", style: {
                                                        color: agent.color
                                                    }, children: "\u2572" })] }) }), _jsxs("div", { className: "relative p-6 flex justify-center", children: [_jsx("div", { className: "w-24 h-24 border-2 overflow-hidden", style: {
                                                    borderColor: agent.color
                                                }, children: _jsx("img", { src: agent.avatar, alt: `${agent.name} avatar`, className: "w-full h-full object-cover" }) }), _jsx("div", { className: "absolute bottom-4 left-1/2 -translate-x-1/2 px-3 py-1 text-xs font-mono font-bold", style: {
                                                    backgroundColor: agent.color,
                                                    color: '#0a0e27'
                                                }, children: agent.rank })] }), _jsxs("div", { className: "p-4 space-y-3 border-t-2", style: {
                                            borderColor: `${agent.color}33`
                                        }, children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("span", { className: "text-[#8b9bb4] text-sm flex items-center gap-2", children: [_jsx(StarIcon, { className: "w-4 h-4", style: {
                                                                    color: agent.color
                                                                } }), "Reputation"] }), _jsx("span", { className: "font-mono font-bold", style: {
                                                            color: agent.color
                                                        }, children: agent.reputation.toLocaleString() })] }), _jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("span", { className: "text-[#8b9bb4] text-sm flex items-center gap-2", children: [_jsx(TrendingUpIcon, { className: "w-4 h-4", style: {
                                                                    color: agent.color
                                                                } }), "Total Votes"] }), _jsx("span", { className: "font-mono text-[#e0e6ed]", children: agent.votes.toLocaleString() })] })] }), _jsx("div", { className: "p-4 border-t-2", style: {
                                            borderColor: `${agent.color}33`
                                        }, children: _jsx("button", { className: "w-full py-2 text-sm font-mono transition-all hover:bg-opacity-20", style: {
                                                color: agent.color
                                            }, children: "\u2192 View Profile" }) })] }, agent.name)) })] }), _jsx("div", { className: "flex justify-center gap-2 mt-8", children: agents.map((agent, index) => _jsx("button", { onClick: () => setCurrentIndex(index), className: `w-3 h-3 transition-all ${index === currentIndex ? 'scale-125' : 'opacity-50 hover:opacity-100'}`, style: {
                            backgroundColor: agent.color
                        }, "aria-label": `Go to agent ${index + 1}` }, index)) })] }) }));
}
