import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import apiClient from '../api/client';
function ComingSoonPage() {
    const [email, setEmail] = useState('');
    const [waitlistCount, setWaitlistCount] = useState(0);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [submitStatus, setSubmitStatus] = useState('idle');
    const [statusMessage, setStatusMessage] = useState('');
    // Fetch current waitlist count on mount
    useEffect(() => {
        fetchWaitlistCount();
    }, []);
    const fetchWaitlistCount = async () => {
        try {
            const response = await apiClient.get('/waitlist/count');
            if (response.success) {
                setWaitlistCount(response.count);
            }
        }
        catch (error) {
            console.error('Failed to fetch waitlist count:', error);
            // Start at 0 if endpoint doesn't exist yet
            setWaitlistCount(0);
        }
    };
    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!email || !email.includes('@')) {
            setStatusMessage('Please enter a valid email address');
            setSubmitStatus('error');
            return;
        }
        setIsSubmitting(true);
        setSubmitStatus('idle');
        try {
            const response = await apiClient.post('/waitlist', { email });
            if (response.success) {
                setSubmitStatus('success');
                setStatusMessage(`Welcome to the waitlist! You're #${response.count} in line.`);
                setWaitlistCount(response.count);
                setEmail('');
            }
            else {
                setSubmitStatus('error');
                setStatusMessage(response.message || 'Something went wrong. Please try again.');
            }
        }
        catch (error) {
            setSubmitStatus('error');
            setStatusMessage(error.message || 'Failed to join waitlist. Please try again.');
        }
        finally {
            setIsSubmitting(false);
        }
    };
    return (_jsxs("div", { className: "min-h-screen bg-gradient-to-br from-purple-900 via-indigo-900 to-blue-900", children: [_jsx("div", { className: "container mx-auto px-4 py-16 md:py-24", children: _jsxs("div", { className: "max-w-4xl mx-auto text-center", children: [_jsx("div", { className: "inline-block mb-6 px-4 py-2 bg-purple-500/20 border border-purple-400/30 rounded-full", children: _jsx("span", { className: "text-purple-300 text-sm font-medium", children: "\uD83D\uDE80 Coming Soon" }) }), _jsx("h1", { className: "text-4xl md:text-6xl font-bold text-white mb-6 leading-tight", children: "Discover the Best AI Music & Tools" }), _jsx("p", { className: "text-lg md:text-xl text-purple-200 mb-8 max-w-2xl mx-auto", children: "Community-powered voting. Weighted by reputation. Protected from gaming." }), _jsx("div", { className: "mb-8", children: _jsxs("div", { className: "inline-flex items-center gap-2 px-4 py-2 bg-blue-500/20 border border-blue-400/30 rounded-lg", children: [_jsx("span", { className: "text-blue-300 text-sm", children: "Current waitlist:" }), _jsx("span", { className: "text-2xl font-bold text-white", children: waitlistCount }), _jsx("span", { className: "text-blue-300 text-sm", children: "people" })] }) }), _jsxs("form", { onSubmit: handleSubmit, className: "max-w-md mx-auto mb-8", children: [_jsxs("div", { className: "flex flex-col sm:flex-row gap-3", children: [_jsx("label", { htmlFor: "waitlist-email", className: "sr-only", children: "Email address" }), _jsx("input", { id: "waitlist-email", type: "email", inputMode: "email", autoComplete: "email", spellCheck: false, value: email, onChange: (e) => setEmail(e.target.value), placeholder: "Enter your email\u2026", "aria-describedby": "waitlist-status", className: "flex-1 px-4 py-3 bg-white/10 border border-purple-400/30 rounded-lg text-white placeholder-purple-300/50 focus:outline-none focus:ring-2 focus:ring-purple-400 focus-visible:ring-2 focus-visible:ring-purple-400", disabled: isSubmitting }), _jsx("button", { type: "submit", disabled: isSubmitting, className: "px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white font-semibold rounded-lg hover:from-purple-600 hover:to-pink-600 transition-all disabled:opacity-50 disabled:cursor-not-allowed focus-visible:ring-2 focus-visible:ring-purple-400", children: isSubmitting ? 'Joining…' : 'Join Waitlist' })] }), statusMessage && (_jsx("div", { id: "waitlist-status", role: "status", "aria-live": "polite", className: `mt-4 text-center ${submitStatus === 'success' ? 'text-green-400' : 'text-red-400'}`, children: statusMessage }))] }), _jsx("div", { className: "max-w-2xl mx-auto mb-12", children: _jsxs("div", { className: "grid md:grid-cols-3 gap-6", children: [_jsxs("div", { className: "text-left p-4 bg-white/5 rounded-lg border border-purple-400/20", children: [_jsx("div", { className: "text-2xl mb-2", children: "\u2713" }), _jsx("h3", { className: "text-white font-semibold mb-2", children: "Weighted Voting" }), _jsx("p", { className: "text-purple-200 text-sm", children: "Reputation matters, not 1 person = 1 vote" })] }), _jsxs("div", { className: "text-left p-4 bg-white/5 rounded-lg border border-purple-400/20", children: [_jsx("div", { className: "text-2xl mb-2", children: "\u2713" }), _jsx("h3", { className: "text-white font-semibold mb-2", children: "Anti-Gaming Protection" }), _jsx("p", { className: "text-purple-200 text-sm", children: "Manipulation attempts are blocked" })] }), _jsxs("div", { className: "text-left p-4 bg-white/5 rounded-lg border border-purple-400/20", children: [_jsx("div", { className: "text-2xl mb-2", children: "\u2713" }), _jsx("h3", { className: "text-white font-semibold mb-2", children: "Real-Time Rankings" }), _jsx("p", { className: "text-purple-200 text-sm", children: "Scores update live as votes come in" })] })] }) }), waitlistCount > 10 && (_jsxs("div", { className: "text-center text-purple-300 text-sm", children: ["Join ", waitlistCount, " early adopters building the most trusted AI music rankings"] }))] }) }), _jsx("div", { className: "container mx-auto px-4 py-8 border-t border-purple-800", children: _jsx("div", { className: "text-center text-purple-400 text-sm", children: "\u00A9 2026 aimusicstore.com - Community-Powered AI Music Rankings" }) })] }));
}
export default ComingSoonPage;
