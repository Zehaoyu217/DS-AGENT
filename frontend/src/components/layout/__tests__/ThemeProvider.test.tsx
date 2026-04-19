import { act, fireEvent, render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it } from "vitest";
import { ThemeProvider, useTheme } from "../ThemeProvider";

function Probe() {
  const { theme, setTheme, resolvedTheme } = useTheme();
  return (
    <div>
      <span data-testid="theme">{theme}</span>
      <span data-testid="resolved">{resolvedTheme}</span>
      <button onClick={() => setTheme("dark")}>Go Dark</button>
      <button onClick={() => setTheme("light")}>Go Light</button>
    </div>
  );
}

function resetEnv(): void {
  window.localStorage.clear();
  delete document.documentElement.dataset.theme;
  document.documentElement.classList.remove("light");
}

beforeEach(() => {
  resetEnv();
});

describe("ThemeProvider", () => {
  it("defaults to light when no storage + no OS preference", () => {
    render(
      <ThemeProvider>
        <Probe />
      </ThemeProvider>,
    );
    expect(screen.getByTestId("theme").textContent).toBe("light");
    expect(document.documentElement.dataset.theme).toBeUndefined();
  });

  it("honours ds:theme=dark on mount and sets the data-theme attr", () => {
    window.localStorage.setItem("ds:theme", "dark");
    render(
      <ThemeProvider>
        <Probe />
      </ThemeProvider>,
    );
    expect(screen.getByTestId("theme").textContent).toBe("dark");
    expect(document.documentElement.dataset.theme).toBe("dark");
  });

  it("migrates legacy `theme` key into `ds:theme`", () => {
    window.localStorage.setItem("theme", "dark");
    render(
      <ThemeProvider>
        <Probe />
      </ThemeProvider>,
    );
    expect(window.localStorage.getItem("ds:theme")).toBe("dark");
    expect(window.localStorage.getItem("theme")).toBeNull();
    expect(screen.getByTestId("theme").textContent).toBe("dark");
  });

  it("setTheme(dark) applies the data-theme attr and writes ds:theme", () => {
    render(
      <ThemeProvider>
        <Probe />
      </ThemeProvider>,
    );
    expect(document.documentElement.dataset.theme).toBeUndefined();
    act(() => {
      fireEvent.click(screen.getByText("Go Dark"));
    });
    expect(document.documentElement.dataset.theme).toBe("dark");
    expect(window.localStorage.getItem("ds:theme")).toBe("dark");
  });

  it("setTheme(light) strips the data-theme attr and any legacy .light class", () => {
    document.documentElement.classList.add("light");
    window.localStorage.setItem("ds:theme", "dark");
    render(
      <ThemeProvider>
        <Probe />
      </ThemeProvider>,
    );
    expect(document.documentElement.dataset.theme).toBe("dark");
    act(() => {
      fireEvent.click(screen.getByText("Go Light"));
    });
    expect(document.documentElement.dataset.theme).toBeUndefined();
    expect(document.documentElement.classList.contains("light")).toBe(false);
  });
});
