/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        slate: {
          50: 'var(--c-slate-50)',
          100: 'var(--c-slate-100)',
          200: 'var(--c-slate-200)',
          300: 'var(--c-slate-300)',
          400: 'var(--c-slate-400)',
          500: 'var(--c-slate-500)',
          600: 'var(--c-slate-600)',
          700: 'var(--c-slate-700)',
          800: 'var(--c-slate-800)',
          900: 'var(--c-slate-900)',
          950: 'var(--c-slate-950)',
        },
        emerald: {
          300: 'var(--c-emerald-300)',
          400: 'var(--c-emerald-400)',
          500: 'var(--c-emerald-500)',
        },
        teal: {
          300: 'var(--c-teal-300)',
          400: 'var(--c-teal-400)',
          500: 'var(--c-teal-500)',
        },
        ide: {
          bg: 'var(--bg-app)',
          panel: 'var(--bg-panel)',
          sidebar: 'var(--bg-surface)',
          terminal: 'var(--bg-terminal)',
          navbar: 'var(--bg-panel)',
          border: 'var(--c-slate-800)',
          text: 'var(--c-slate-100)',
          muted: 'var(--c-slate-400)',
        },
        accent: {
          blue: {
            DEFAULT: '#0078d4',
            hover: '#1084e3',
            light: 'rgba(0, 120, 212, 0.15)',
          },
          green: {
            DEFAULT: '#4ec9b0',
            light: 'rgba(78, 201, 176, 0.15)',
          },
          red: {
            DEFAULT: '#f44747',
            light: 'rgba(244, 71, 71, 0.15)',
          },
          yellow: {
            DEFAULT: '#dcdcaa',
            light: 'rgba(220, 220, 170, 0.15)',
          },
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial', 'sans-serif'],
        mono: ['Fira Code', 'JetBrains Mono', 'Menlo', 'Monaco', 'Consolas', 'Liberation Mono', 'Courier New', 'monospace'],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      }
    },
  },
  plugins: [],
}
