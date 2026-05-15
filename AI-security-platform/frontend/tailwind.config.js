/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        dark: {
          50: "#f8fafc",
          100: "#f1f5f9",
          700: "#1e293b",
          800: "#0f172a",
          900: "#020617",
        },
      },
    },
  },
  plugins: [],
};
