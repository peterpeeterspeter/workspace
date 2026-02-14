/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#0a0a0a',
        secondary: '#7c3aed',
        surface: '#1a1a2e',
        surfaceAlt: '#241432',
        border: '#37224a',
        accent: '#a855f7',
        accentHover: '#c975fb',
        success: '#10b981',
        warning: '#f59e0b',
        error: '#ef4444',
      },
      fontFamily: {
        display: ['Space Grotesk', 'sans-serif'],
        body: ['Instrument Sans', 'sans-serif'],
      },
    },
  },
  plugins: [],
}

