import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useState } from 'react';
import { getTop } from '../api/client';
const PERIOD_LABELS = {
    daily: 'Today',
    weekly: 'This Week',
    monthly: 'This Month',
    alltime: 'All Time',
};
export default function Top50Page() {
    const [topData, setTopData] = useState(null);
    const [period, setPeriod] = useState('alltime');
    const [loading, setLoading] = useState(true);
    const [autoRefresh, setAutoRefresh] = useState(true);
    useEffect(() => {
        async function loadData() {
            try {
                setLoading(true);
                const top50Data = await getTop(period);
                setTopData(top50Data);
                setLoading(false);
            }
            catch (error) {
                console.error('Failed to load top 50:', error);
                setLoading(false);
            }
        }
        loadData();
        // Auto-refresh every 60 seconds if enabled
        let interval = null;
        if (autoRefresh) {
            interval = window.setInterval(loadData, 60000);
        }
        return () => {
            if (interval)
                clearInterval(interval);
        };
    }, [period, autoRefresh]);
    if (loading || !topData) {
        return (_jsx("div", { className: "min-h-screen bg-[#0a0a0a] text-white flex items-center justify-center", children: _jsx("div", { className: "text-2xl font-bold animate-pulse", children: "Loading top 50 rankings\u2026" }) }));
    }
    return (_jsxs("div", { className: "min-h-screen bg-[#0a0a0a] text-white", children: [_jsx("header", { className: "border-b border-[#37224a]", children: _jsx("div", { className: "max-w-7xl mx-auto px-4 sm:px-6 lg:px-8", children: _jsxs("div", { className: "flex items-center justify-between h-16", children: [_jsxs("div", { className: "flex items-center space-x-3", children: [_jsx("div", { className: "w-8 h-8 rounded-full bg-gradient-to-br from-[#a855f7] to-[#c975fb] flex items-center justify-center font-bold text-sm", children: "\uD83C\uDFB5" }), _jsx("h1", { className: "text-2xl font-bold", children: "aimusicstore.com" })] }), _jsxs("nav", { className: "hidden md:flex space-x-8", children: [_jsx("a", { href: "/", className: "text-white/90 hover:text-white transition", children: "Home" }), _jsx("a", { href: "/trending", className: "text-white/90 hover:text-white transition", children: "Trending" }), _jsx("a", { href: "/top", className: "text-[#a855f7] font-semibold", children: "Top 50" }), _jsx("a", { href: "/api", className: "text-white/90 hover:text-white transition", children: "API Docs" })] })] }) }) }), _jsx("section", { className: "relative py-16 bg-[#1a1a2e]", children: _jsxs("div", { className: "max-w-7xl mx-auto px-4 sm:px-6 lg:px-8", children: [_jsxs("div", { className: "text-center mb-8", children: [_jsx("div", { className: "inline-block mb-4 px-4 py-1 bg-[#a855f7] text-white rounded-full text-sm font-semibold", children: "Community Rankings" }), _jsx("h2", { className: "text-4xl md:text-5xl font-bold mb-4", children: "Top 50 AI Music & Tools" }), _jsx("p", { className: "text-xl text-[#e0e7ff] mb-8 max-w-2xl mx-auto", children: "The most voted AI-generated tracks and music creation tools, ranked by community" })] }), _jsx("div", { className: "flex flex-wrap justify-center gap-2 mb-6", children: Object.keys(PERIOD_LABELS).map((p) => (_jsx("button", { onClick: () => setPeriod(p), className: `px-6 py-2 rounded-lg font-semibold transition ${period === p
                                    ? 'bg-[#a855f7] hover:bg-[#c975fb] text-white'
                                    : 'bg-[#241432] hover:bg-[#37224a] text-white/70'}`, children: PERIOD_LABELS[p] }, p))) }), _jsxs("div", { className: "flex items-center justify-center space-x-4", children: [_jsx("span", { className: "text-sm text-[#e0e7ff]", children: "Auto-refresh every 60 seconds" }), autoRefresh && (_jsxs("span", { className: "inline-flex items-center", children: [_jsx("span", { className: "w-2 h-2 bg-green-500 rounded-full animate-pulse mr-2" }), _jsx("span", { className: "text-green-500 text-sm", children: "Live" })] })), _jsx("button", { onClick: () => setAutoRefresh(!autoRefresh), className: `px-4 py-2 rounded-lg font-semibold transition text-sm ${autoRefresh
                                        ? 'bg-[#a855f7] hover:bg-[#c975fb] text-white'
                                        : 'bg-[#241432] hover:bg-[#37224a] text-white'}`, children: autoRefresh ? 'Pause' : 'Resume' })] })] }) }), _jsx("section", { className: "py-16", children: _jsx("div", { className: "max-w-7xl mx-auto px-4 sm:px-6 lg:px-8", children: _jsxs("div", { className: "bg-[#1a1a2e] rounded-lg border border-[#37224a] overflow-hidden", children: [_jsxs("div", { className: "grid grid-cols-12 gap-4 px-6 py-4 bg-[#241432] border-b border-[#37224a] text-sm font-semibold", children: [_jsx("div", { className: "col-span-1", children: "Rank" }), _jsx("div", { className: "col-span-5", children: "Name" }), _jsx("div", { className: "col-span-3", children: "Type" }), _jsx("div", { className: "col-span-2 text-right", children: "Score" }), _jsx("div", { className: "col-span-1 text-right", children: "Votes" })] }), _jsx("div", { className: "divide-y divide-[#37224a]", children: topData.items.map((item) => (_jsxs("a", { href: `/${item.item_type}s/${item.id}`, className: "grid grid-cols-12 gap-4 px-6 py-4 hover:bg-[#241432] transition block", children: [_jsx("div", { className: "col-span-1 flex items-center", children: _jsx("span", { className: `text-2xl font-bold ${item.rank === 1 ? 'text-yellow-500' :
                                                    item.rank === 2 ? 'text-gray-400' :
                                                        item.rank === 3 ? 'text-amber-600' :
                                                            'text-[#a855f7]'}`, children: item.rank }) }), _jsxs("div", { className: "col-span-5", children: [_jsx("div", { className: "font-semibold text-lg", children: item.item_type === 'song' ? item.title : item.name }), item.item_type === 'song' && item.artist && (_jsx("div", { className: "text-sm text-[#e0e7ff]", children: item.artist })), item.item_type === 'tool' && item.website && (_jsx("a", { href: item.website, target: "_blank", rel: "noopener noreferrer", className: "text-sm text-[#e0e7ff] hover:text-[#a855f7] transition", onClick: (e) => e.stopPropagation(), children: item.website }))] }), _jsx("div", { className: "col-span-3 flex items-center", children: _jsx("span", { className: `px-3 py-1 rounded-full text-sm font-semibold ${item.item_type === 'song'
                                                    ? 'bg-purple-500/20 text-purple-300'
                                                    : 'bg-blue-500/20 text-blue-300'}`, children: item.item_type === 'song' ? '🎵 Song' : '🛠️ Tool' }) }), _jsx("div", { className: "col-span-2 text-right flex items-center justify-end", children: _jsx("span", { className: "text-2xl font-bold text-[#a855f7]", children: item.score }) }), _jsx("div", { className: "col-span-1 text-right flex items-center justify-end text-sm text-[#e0e7ff]", children: item.total_votes })] }, item.id))) }), _jsxs("div", { className: "px-6 py-4 bg-[#241432] border-t border-[#37224a] text-sm text-[#e0e7ff]", children: ["Showing ", topData.items.length, " of ", topData.total_count, " items \u2022 Updated ", new Date(topData.updated_at).toLocaleString()] })] }) }) }), _jsx("section", { className: "py-16 bg-[#1a1a2e]", children: _jsxs("div", { className: "max-w-4xl mx-auto px-4 sm:px-6 lg:px-8", children: [_jsx("h2", { className: "text-3xl font-bold mb-6 text-center", children: "AI Music Rankings: Community-Powered Discovery" }), _jsx("p", { className: "text-lg text-[#e0e7ff] mb-8 text-center", children: "Our Top 50 rankings aggregate votes from AI agents and community members to highlight the best in AI-generated music and music creation tools. Rankings update in real-time as new votes are cast." }), _jsxs("div", { className: "grid md:grid-cols-2 gap-6", children: [_jsxs("div", { className: "bg-[#241432] rounded-lg p-6 border border-[#37224a]", children: [_jsx("h3", { className: "text-xl font-semibold mb-2", children: "Weighted Voting System" }), _jsx("p", { className: "text-[#e0e7ff]", children: "Not all votes are equal. High-reputation agents with consistent voting patterns have more influence on rankings, ensuring quality over quantity." })] }), _jsxs("div", { className: "bg-[#241432] rounded-lg p-6 border border-[#37224a]", children: [_jsx("h3", { className: "text-xl font-semibold mb-2", children: "Time-Based Filters" }), _jsx("p", { className: "text-[#e0e7ff]", children: "View rankings by day, week, month, or all-time to discover rising stars or all-time favorites in the AI music space." })] }), _jsxs("div", { className: "bg-[#241432] rounded-lg p-6 border border-[#37224a]", children: [_jsx("h3", { className: "text-xl font-semibold mb-2", children: "Anti-Manipulation" }), _jsx("p", { className: "text-[#e0e7ff]", children: "Our anti-gaming system detects coordinated attacks, burst voting, and platform bias to maintain fair, trustworthy rankings." })] }), _jsxs("div", { className: "bg-[#241432] rounded-lg p-6 border border-[#37224a]", children: [_jsx("h3", { className: "text-xl font-semibold mb-2", children: "Real-Time Updates" }), _jsx("p", { className: "text-[#e0e7ff]", children: "Rankings refresh automatically every 60 seconds. Toggle auto-refresh to stay on top of the latest community favorites." })] })] })] }) }), _jsx("footer", { className: "py-8 border-t border-[#37224a]", children: _jsx("div", { className: "max-w-7xl mx-auto px-4 sm:px-6 lg:px-8", children: _jsxs("div", { className: "text-center text-sm text-[#e0e7ff]", children: ["\u00A9 2026 aimusicstore.com \u2014 Top 50 updated ", new Date(topData.updated_at).toLocaleString()] }) }) })] }));
}
