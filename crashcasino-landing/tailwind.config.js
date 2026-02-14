/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'primary': '#0a0a0a',
        'secondary': '#141414',
        'accent': '#00ff88',
        'accent-hover': '#00cc6a',
        'text-primary': '#fafafa',
        'text-secondary': '#a1a1a1',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'delay-1000': 'delay 1000ms',
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}
