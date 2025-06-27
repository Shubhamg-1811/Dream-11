// tailwind.config.js

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html",
  ],
  theme: {
    extend: {
      boxShadow: {
        'custom-glow': '0 0 10px rgba(0, 0, 0, 0.7)', // Red glow
        'custom-glow-blue': '0 0 10px rgba(59, 130, 246, 0.7)', // Blue glow for Captain
        'custom-glow-green': '0 0 10px rgba(34, 197, 94, 0.7)', // Green glow for Vice-Captain
      },
    },
  },
  plugins: [],
}
