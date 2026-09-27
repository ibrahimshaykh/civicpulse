import type { Config } from "tailwindcss";

// Plan §8.2: public-works signage, not a SaaS landing page.
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#16324A",
        paper: "#F5F7F8",
        panel: "#FFFFFF",
        rule: "#D5DCE1",
        signal: "#F2B705",
        high: "#B3261E",
        normal: "#2F6DB5",
        low: "#5F6B73",
      },
      fontFamily: {
        sans: ["Public Sans Variable", "system-ui", "sans-serif"],
      },
      fontSize: {
        sm: ["14px", "1.5"],
        base: ["16px", "1.5"],
        lg: ["20px", "1.2"],
        xl: ["28px", "1.2"],
      },
      maxWidth: {
        form: "640px",
        board: "1200px",
      },
    },
  },
  plugins: [],
} satisfies Config;
