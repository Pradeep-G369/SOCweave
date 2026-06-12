/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        canvas: "#0F172A",
        border: "#1E293B",
        threat: "#EF4444",
        safe: "#10B981",
        progress: "#F59E0B",
        citelink: "#3B82F6",
        textprimary: "#F1F5F9",
        textsecondary: "#94A3B8",
      },
    },
  },
  plugins: [],
}