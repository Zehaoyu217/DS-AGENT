import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
} from "react";

type Theme = "light" | "dark" | "system";
type ResolvedTheme = "light" | "dark";

interface ThemeContextValue {
  theme: Theme;
  setTheme: (theme: Theme) => void;
  resolvedTheme: ResolvedTheme;
}

const ThemeContext = createContext<ThemeContextValue>({
  theme: "light",
  setTheme: () => {},
  resolvedTheme: "light",
});

const THEME_STORAGE_KEY = "ds:theme";
const LEGACY_STORAGE_KEY = "theme";

function isTheme(value: string | null): value is Theme {
  return value === "light" || value === "dark" || value === "system";
}

// Resolve the initial theme from storage, falling back to a media-query
// hint. We also migrate the legacy `theme` key into the new `ds:theme`
// key so returning users keep their preference across the rename.
function readStoredTheme(): Theme {
  if (typeof window === "undefined") return "light";

  const stored = window.localStorage.getItem(THEME_STORAGE_KEY);
  if (isTheme(stored)) return stored;

  const legacy = window.localStorage.getItem(LEGACY_STORAGE_KEY);
  if (isTheme(legacy)) {
    try {
      window.localStorage.setItem(THEME_STORAGE_KEY, legacy);
      window.localStorage.removeItem(LEGACY_STORAGE_KEY);
    } catch {
      // Storage may be blocked; non-fatal.
    }
    return legacy;
  }

  // No stored preference — honour the OS hint when it's explicit,
  // otherwise prefer the light product default.
  if (typeof window.matchMedia === "function") {
    const prefersDark = window.matchMedia(
      "(prefers-color-scheme: dark)",
    ).matches;
    return prefersDark ? "dark" : "light";
  }
  return "light";
}

function applyTheme(resolved: ResolvedTheme): void {
  if (typeof document === "undefined") return;
  const root = document.documentElement;
  if (resolved === "dark") {
    root.dataset.theme = "dark";
  } else {
    delete root.dataset.theme;
  }
  // Legacy `.light` class is no longer used — strip if present so pages
  // that reload after an upgrade don't end up with stale styling.
  root.classList.remove("light");
}

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setThemeState] = useState<Theme>(readStoredTheme);
  const [resolvedTheme, setResolvedTheme] = useState<ResolvedTheme>(() =>
    readStoredTheme() === "dark" ? "dark" : "light",
  );

  useEffect(() => {
    const mq =
      typeof window.matchMedia === "function"
        ? window.matchMedia("(prefers-color-scheme: dark)")
        : null;

    const apply = () => {
      const resolved: ResolvedTheme =
        theme === "system" ? (mq?.matches ? "dark" : "light") : theme;
      setResolvedTheme(resolved);
      applyTheme(resolved);
    };

    apply();
    mq?.addEventListener("change", apply);
    return () => mq?.removeEventListener("change", apply);
  }, [theme]);

  const setTheme = useCallback((next: Theme) => {
    setThemeState(next);
    try {
      window.localStorage.setItem(THEME_STORAGE_KEY, next);
    } catch {
      // Storage errors (quota, privacy mode, etc.) shouldn't break the UI.
    }
  }, []);

  return (
    <ThemeContext.Provider value={{ theme, setTheme, resolvedTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export const useTheme = () => useContext(ThemeContext);
