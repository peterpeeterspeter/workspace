// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
/**
 * Fetch system health status
 */
export async function getHealth() {
    const response = await fetch(`${API_BASE_URL}/health`);
    if (!response.ok) {
        throw new Error(`Health check failed: ${response.statusText}`);
    }
    return response.json();
}
/**
 * Fetch trending songs and tools (Top 10 each)
 */
export async function getTrending() {
    const response = await fetch(`${API_BASE_URL}/api/v1/trending`);
    if (!response.ok) {
        throw new Error(`Failed to fetch trending: ${response.statusText}`);
    }
    return response.json();
}
/**
 * Fetch top 50 rankings by period
 * @param period - 'daily' | 'weekly' | 'monthly' | 'alltime'
 */
export async function getTop(period = 'alltime') {
    const response = await fetch(`${API_BASE_URL}/api/v1/top/${period}`);
    if (!response.ok) {
        throw new Error(`Failed to fetch top 50: ${response.statusText}`);
    }
    return response.json();
}
/**
 * Fetch song details by ID
 * @param songId - Song unique identifier
 */
export async function getSong(songId) {
    const response = await fetch(`${API_BASE_URL}/api/v1/songs/${songId}`);
    if (!response.ok) {
        throw new Error(`Failed to fetch song: ${response.statusText}`);
    }
    return response.json();
}
/**
 * Fetch tool details by ID
 * @param toolId - Tool unique identifier
 */
export async function getTool(toolId) {
    const response = await fetch(`${API_BASE_URL}/api/v1/tools/${toolId}`);
    if (!response.ok) {
        throw new Error(`Failed to fetch tool: ${response.statusText}`);
    }
    return response.json();
}
/**
 * Submit a vote (requires API key in production)
 */
export async function submitVote(item_type, item_id, vote, apiKey) {
    const headers = {
        'Content-Type': 'application/json',
    };
    if (apiKey) {
        headers['Authorization'] = `Bearer ${apiKey}`;
    }
    return fetch(`${API_BASE_URL}/api/v1/vote`, {
        method: 'POST',
        headers,
        body: JSON.stringify({
            item_type,
            item_id,
            vote,
        }),
    });
}
/**
 * Get API key info (requires authentication)
 */
export async function getApiKeys(apiKey) {
    return fetch(`${API_BASE_URL}/api/v1/keys`, {
        headers: {
            'Authorization': `Bearer ${apiKey}`,
        },
    });
}
/**
 * Create new API key (requires authentication)
 */
export async function createApiKey(apiKey, name) {
    return fetch(`${API_BASE_URL}/api/v1/keys`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name }),
    });
}
/**
 * Get waitlist count
 */
export async function getWaitlistCount() {
    const response = await fetch(`${API_BASE_URL}/api/v1/waitlist/count`);
    if (!response.ok) {
        throw new Error(`Failed to fetch waitlist count: ${response.statusText}`);
    }
    return response.json();
}
/**
 * Join waitlist
 */
export async function joinWaitlist(email) {
    const response = await fetch(`${API_BASE_URL}/api/v1/waitlist`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
    });
    if (!response.ok) {
        throw new Error(`Failed to join waitlist: ${response.statusText}`);
    }
    return response.json();
}
// Export a simpler API client for components
const apiClient = {
    get: async (endpoint) => {
        const response = await fetch(`${API_BASE_URL}${endpoint}`);
        if (!response.ok) {
            throw new Error(`API request failed: ${response.statusText}`);
        }
        return response.json();
    },
    post: async (endpoint, data) => {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });
        if (!response.ok) {
            throw new Error(`API request failed: ${response.statusText}`);
        }
        return response.json();
    },
};
export default apiClient;
