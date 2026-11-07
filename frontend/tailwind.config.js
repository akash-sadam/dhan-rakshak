/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        guard: {
          900: '#06090e',
          850: '#0b1118',
          800: '#0f172a',
          accent: '#38bdf8',
          crimson: '#ef4444',
          amber: '#f59e0b',
          emerald: '#10b981',
        }
      }
    },
  },
  plugins: [],
}
