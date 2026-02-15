const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const bcrypt = require('bcrypt');
const { v4: uuidv4 } = require('uuid');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(express.static('public'));

// In-memory storage (replace with proper database later)
const waitlist = new Map();
const subscribers = [];

// Validation helpers
const isValidEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
};

// Routes

// Health check
app.get('/health', (req, res) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Get waitlist count
app.get('/api/waitlist/count', (req, res) => {
    const count = subscribers.length + 147; // Base count for social proof
    res.json({ count });
});

// Join waitlist
app.post('/api/waitlist/join', async (req, res) => {
    try {
        const { email } = req.body;
        
        // Validate email
        if (!email || !isValidEmail(email)) {
            return res.status(400).json({ 
                error: 'Invalid email address',
                message: 'Please provide a valid email address'
            });
        }
        
        // Check if already subscribed
        const existing = subscribers.find(s => s.email.toLowerCase() === email.toLowerCase());
        if (existing) {
            return res.status(409).json({ 
                error: 'Already subscribed',
                message: 'You\'re already on the waitlist!'
            });
        }
        
        // Add to waitlist
        const subscriber = {
            id: uuidv4(),
            email: email.toLowerCase(),
            createdAt: new Date().toISOString(),
            ip: req.ip || null,
            userAgent: req.get('user-agent') || null,
            source: req.body.source || 'coming-soon-page'
        };
        
        subscribers.push(subscriber);
        
        // Log (replace with actual database storage)
        console.log('New waitlist signup:', subscriber);
        
        res.json({ 
            success: true,
            message: 'Welcome to the waitlist! We\'ll notify you when we launch.',
            count: subscribers.length + 147
        });
        
    } catch (error) {
        console.error('Waitlist signup error:', error);
        res.status(500).json({ 
            error: 'Internal server error',
            message: 'Something went wrong. Please try again.'
        });
    }
});

// Get all subscribers (admin only - add auth later)
app.get('/api/waitlist/subscribers', (req, res) => {
    res.json({ 
        subscribers: subscribers.map(s => ({
            id: s.id,
            email: s.email,
            createdAt: s.createdAt,
            source: s.source
        })),
        total: subscribers.length
    });
});

// Export waitlist (for backup)
app.get('/api/waitlist/export', (req, res) => {
    const csv = [
        'Email,Joined At,Source',
        ...subscribers.map(s => `${s.email},${s.createdAt},${s.source}`)
    ].join('\n');
    
    res.setHeader('Content-Type', 'text/csv');
    res.setHeader('Content-Disposition', 'attachment; filename=waitlist.csv');
    res.send(csv);
});

// Serve coming soon page
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/public/index.html');
});

// Start server
app.listen(PORT, () => {
    console.log(`🚀 aimusicstore.com server running on port ${PORT}`);
    console.log(`📧 Waitlist ready: ${subscribers.length} subscribers`);
});

module.exports = app;