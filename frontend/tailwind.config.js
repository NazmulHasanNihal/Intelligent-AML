/** @type {import('tailwindcss').Config} */
const token = (name) => `rgb(var(--${name}) / <alpha-value>)`;

export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: ['class', '[data-theme="dark"]'],
  theme: {
    extend: {
      colors: {
        background: token('background'),
        bg: token('background'),
        surface: token('surface'),
        surfaceRaised: token('surface-raised'),
        surfaceHover: token('surface-hover'),
        popover: token('popover'),
        border: token('border'),
        borderSubtle: token('border-subtle'),
        borderStrong: token('border-strong'),
        foreground: token('foreground'),
        
        text: {
          DEFAULT: token('foreground'),
          2: token('muted-foreground'),
          muted: token('muted-foreground'),
        },

        muted: {
          DEFAULT: token('muted-foreground'),
          foreground: token('muted-foreground'),
        },
        
        accent: {
          DEFAULT: token('accent'),
          hover: "var(--accent-hover)",
          subtle: "var(--accent-subtle)",
          text: token('accent'),
        },
        
        critical: {
          DEFAULT: token('critical'),
          bg: "var(--critical-bg)",
          border: "var(--critical-border)",
          text: token('critical'),
        },
        
        review: {
          DEFAULT: token('review'),
          bg: "var(--review-bg)",
          border: "var(--review-border)",
          text: token('review'),
        },
        
        cleared: {
          DEFAULT: token('cleared'),
          bg: "var(--cleared-bg)",
          border: "var(--cleared-border)",
          text: token('cleared'),
        },
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', '"Segoe UI"', 'Roboto', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'SFMono-Regular', 'Menlo', 'Monaco', 'Consolas', 'monospace'],
      },
      borderRadius: {
        DEFAULT: "var(--radius)",
        sm: "var(--radius-sm)",
        md: "var(--radius-md)",
        lg: "var(--radius-lg)",
        full: "var(--radius-full)",
      },
      boxShadow: {
        sm: "var(--shadow-sm)",
        DEFAULT: "var(--shadow)",
        md: "var(--shadow-md)",
        lg: "var(--shadow-lg)",
        drawer: "var(--shadow-drawer)",
      },
      transitionDuration: {
        DEFAULT: "150ms",
      },
    },
  },
  plugins: [],
}
