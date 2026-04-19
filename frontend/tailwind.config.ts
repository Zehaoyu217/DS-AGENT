import type { Config } from "tailwindcss";

const config: Config = {
  /**
   * Dark theme activates when <html data-theme="dark"> is set.
   * Light is the default.
   */
  darkMode: ["selector", '[data-theme="dark"]'],
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx,mdx}"],
  safelist: [
    "animate-march",
    "animate-pulse-ring",
    "animate-pulse-ds",
    "animate-draw-check",
    "animate-scale-in-ds",
    "animate-fade-in-ds",
    "animate-slide-in-r",
    "animate-sheen",
  ],
  theme: {
    extend: {
      colors: {
        // ── Shadcn semantic tokens (HSL via CSS vars) ─────────────────────
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",

        // ── DS-Agent handoff tokens ───────────────────────────────────────
        "bg-0": "var(--bg-0)",
        "bg-1": "var(--bg-1)",
        "bg-2": "var(--bg-2)",
        "bg-3": "var(--bg-3)",
        "fg-0": "var(--fg-0)",
        "fg-1": "var(--fg-1)",
        "fg-2": "var(--fg-2)",
        "fg-3": "var(--fg-3)",
        line: "var(--line)",
        "line-2": "var(--line-2)",
        acc: {
          DEFAULT: "var(--acc)",
          fg: "var(--acc-fg)",
          dim: "var(--acc-dim)",
          line: "var(--acc-line)",
        },
        ok: "var(--ok)",
        warn: "var(--warn)",
        err: "var(--err)",

        // ── Legacy-compat direct var tokens (kept for untouched code) ─────
        canvas: {
          DEFAULT: "var(--color-bg-primary)",
          secondary: "var(--color-bg-secondary)",
          elevated: "var(--color-bg-elevated)",
        },
        ink: {
          DEFAULT: "var(--color-text-primary)",
          secondary: "var(--color-text-secondary)",
          muted: "var(--color-text-muted)",
        },
        "brand-accent": {
          DEFAULT: "var(--color-accent)",
          hover: "var(--color-accent-hover)",
          active: "var(--color-accent-active)",
          fg: "var(--color-accent-foreground)",
        },
        edge: {
          DEFAULT: "var(--color-border)",
          hover: "var(--color-border-hover)",
        },
        success: {
          DEFAULT: "var(--color-success)",
          bg: "var(--color-success-bg)",
        },
        warning: {
          DEFAULT: "var(--color-warning)",
          bg: "var(--color-warning-bg)",
        },
        error: {
          DEFAULT: "var(--color-error)",
          bg: "var(--color-error-bg)",
        },
        info: {
          DEFAULT: "var(--color-info)",
          bg: "var(--color-info-bg)",
        },
        "code-surface": {
          DEFAULT: "var(--color-code-bg)",
          text: "var(--color-code-text)",
        },

        // ── Brand palette (Claude orange) ─────────────────────────────────
        brand: {
          50: "#fff7ed",
          100: "#ffedd5",
          200: "#fed7aa",
          300: "#fdba74",
          400: "#fb923c",
          500: "#f97316",
          600: "#ea580c",
          700: "#c2410c",
          800: "#9a3412",
          900: "#7c2d12",
          950: "#431407",
        },

        // ── Surface neutral palette ───────────────────────────────────────
        surface: {
          50: "#fafafa",
          100: "#f4f4f5",
          200: "#e4e4e7",
          300: "#d4d4d8",
          400: "#a1a1aa",
          500: "#71717a",
          600: "#52525b",
          700: "#3f3f46",
          800: "#27272a",
          850: "#1f1f23",
          900: "#18181b",
          950: "#09090b",
        },
      },

      fontFamily: {
        sans: [
          "Inter",
          "ui-sans-serif",
          "-apple-system",
          "BlinkMacSystemFont",
          "SF Pro Text",
          "Helvetica Neue",
          "sans-serif",
        ],
        serif: [
          "Charter",
          "Iowan Old Style",
          "Palatino",
          "ui-serif",
          "serif",
        ],
        mono: [
          "JetBrains Mono",
          "ui-monospace",
          "SFMono-Regular",
          "Menlo",
          "Consolas",
          "monospace",
        ],
      },

      borderRadius: {
        xs: "var(--radius-xs)",
        DEFAULT: "var(--radius)",
        sm: "var(--radius-xs)",
        md: "var(--radius)",
        lg: "var(--radius-lg)",
        xl: "var(--radius-xl)",
      },

      transitionDuration: {
        fast: "140ms",
        base: "220ms",
        slow: "360ms",
        // Legacy aliases
        normal: "220ms",
      },

      transitionTimingFunction: {
        "out-expo": "cubic-bezier(0.16, 1, 0.3, 1)",
        "out-2": "cubic-bezier(0.22, 1, 0.36, 1)",
        "in-out": "cubic-bezier(0.65, 0, 0.35, 1)",
        spring: "cubic-bezier(0.34, 1.56, 0.64, 1)",
      },

      boxShadow: {
        "ds-1": "var(--shadow-1)",
        "ds-2": "var(--shadow-2)",
        ds: "var(--shadow)",
      },

      animation: {
        // Legacy
        "fade-in": "fadeIn 200ms ease forwards",
        "fade-out": "fadeOut 200ms ease forwards",
        "slide-up": "slideUp 300ms ease forwards",
        "slide-down": "slideDown 300ms ease forwards",
        "slide-down-out": "slideDownOut 300ms ease forwards",
        "scale-in": "scaleIn 200ms ease forwards",
        "scale-out": "scaleOut 200ms ease forwards",
        shimmer: "shimmerLegacy 2s linear infinite",
        spin: "spin 1s linear infinite",
        "pulse-soft": "pulseSoft 2s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "progress-bar": "progress linear forwards",

        // DS handoff
        march: "march 1s linear infinite",
        "pulse-ds":
          "pulse-ds 1.8s cubic-bezier(0.65, 0, 0.35, 1) infinite",
        "pulse-ring":
          "pulseRing 1.8s cubic-bezier(0.16, 1, 0.3, 1) infinite",
        "draw-check":
          "drawCheck 420ms cubic-bezier(0.16, 1, 0.3, 1) forwards",
        "scale-in-ds":
          "scaleInDs 280ms cubic-bezier(0.34, 1.56, 0.64, 1) both",
        "fade-in-ds": "fadeInDs 280ms cubic-bezier(0.16, 1, 0.3, 1) both",
        "slide-in-r": "slideInR 260ms cubic-bezier(0.16, 1, 0.3, 1) both",
        sheen: "sheen 2.4s cubic-bezier(0.65, 0, 0.35, 1) infinite",
      },

      keyframes: {
        // Legacy (unchanged names preserved where existing components depend on them)
        fadeIn: {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        fadeOut: {
          "0%": { opacity: "1" },
          "100%": { opacity: "0" },
        },
        slideUp: {
          "0%": { transform: "translateY(8px)", opacity: "0" },
          "100%": { transform: "translateY(0)", opacity: "1" },
        },
        slideDown: {
          "0%": { transform: "translateY(-8px)", opacity: "0" },
          "100%": { transform: "translateY(0)", opacity: "1" },
        },
        slideDownOut: {
          "0%": { transform: "translateY(0)", opacity: "1" },
          "100%": { transform: "translateY(8px)", opacity: "0" },
        },
        scaleIn: {
          "0%": { transform: "scale(0.95)", opacity: "0" },
          "100%": { transform: "scale(1)", opacity: "1" },
        },
        scaleOut: {
          "0%": { transform: "scale(1)", opacity: "1" },
          "100%": { transform: "scale(0.95)", opacity: "0" },
        },
        shimmerLegacy: {
          "0%": { backgroundPosition: "-200% 0" },
          "100%": { backgroundPosition: "200% 0" },
        },
        pulseSoft: {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.5" },
        },
        progress: {
          from: { transform: "scaleX(1)" },
          to: { transform: "scaleX(0)" },
        },

        // DS handoff
        march: {
          to: { backgroundPosition: "16px 0" },
        },
        "pulse-ds": {
          "0%, 100%": { opacity: "0.35", transform: "scale(0.9)" },
          "50%": { opacity: "1", transform: "scale(1.15)" },
        },
        pulseRing: {
          "0%": { transform: "scale(1)", opacity: "0.55" },
          "80%": { transform: "scale(2.2)", opacity: "0" },
          "100%": { transform: "scale(2.2)", opacity: "0" },
        },
        drawCheck: {
          from: { strokeDashoffset: "22" },
          to: { strokeDashoffset: "0" },
        },
        scaleInDs: {
          from: { transform: "scale(0.6)", opacity: "0" },
          to: { transform: "scale(1)", opacity: "1" },
        },
        fadeInDs: {
          from: { opacity: "0", transform: "translateY(3px)" },
          to: { opacity: "1", transform: "translateY(0)" },
        },
        slideInR: {
          from: { transform: "translateX(8px)", opacity: "0" },
          to: { transform: "translateX(0)", opacity: "1" },
        },
        sheen: {
          "0%": { backgroundPosition: "-200% 0" },
          "100%": { backgroundPosition: "200% 0" },
        },
      },
    },
  },
  plugins: [],
};

export default config;
