import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { PipelineAction } from "../PipelineAction";
import type { PhaseState } from "@/lib/pipeline-store";

const idle: PhaseState = {
  status: "idle",
  lastRunAt: null,
  lastResult: null,
  errorMessage: null,
};

describe("PipelineAction", () => {
  it("renders label and fires onClick when idle", () => {
    const onClick = vi.fn();
    render(
      <PipelineAction
        phase="digest"
        label="Digest"
        icon={<span data-testid="icon">D</span>}
        state={idle}
        onClick={onClick}
      />,
    );
    fireEvent.click(screen.getByRole("button"));
    expect(onClick).toHaveBeenCalledTimes(1);
  });

  it("disables button and shows RUNNING… while running", () => {
    const onClick = vi.fn();
    render(
      <PipelineAction
        phase="digest"
        label="Digest"
        icon={<span>D</span>}
        state={{ ...idle, status: "running" }}
        onClick={onClick}
      />,
    );
    const btn = screen.getByRole("button");
    expect(btn).toBeDisabled();
    expect(btn).toHaveAttribute("aria-busy", "true");
    expect(btn.textContent).toContain("RUNNING");
    fireEvent.click(btn);
    expect(onClick).not.toHaveBeenCalled();
  });

  it("summarizes ingest result", () => {
    render(
      <PipelineAction
        phase="ingest"
        label="Ingest"
        icon={<span>I</span>}
        state={{
          status: "done",
          lastRunAt: new Date().toISOString(),
          lastResult: { sources_added: 3 },
          errorMessage: null,
        }}
        onClick={vi.fn()}
      />,
    );
    expect(screen.getByRole("button").textContent).toContain("+3 sources");
  });

  it("summarizes maintain clean vs errors", () => {
    const { rerender } = render(
      <PipelineAction
        phase="maintain"
        label="Maintain"
        icon={<span>M</span>}
        state={{
          status: "done",
          lastRunAt: new Date().toISOString(),
          lastResult: {
            lint_errors: 0,
            lint_warnings: 0,
            lint_info: 0,
            open_contradictions: 0,
            stale_count: 0,
            stale_abstracts: [],
            analytics_rebuilt: true,
            habit_proposals: 0,
            fts_bytes_before: 0,
            fts_bytes_after: 0,
            duck_bytes_before: 0,
            duck_bytes_after: 0,
          },
          errorMessage: null,
        }}
        onClick={vi.fn()}
      />,
    );
    expect(screen.getByRole("button").textContent).toContain("clean");

    rerender(
      <PipelineAction
        phase="maintain"
        label="Maintain"
        icon={<span>M</span>}
        state={{
          status: "done",
          lastRunAt: new Date().toISOString(),
          lastResult: {
            lint_errors: 2,
            lint_warnings: 5,
            lint_info: 0,
            open_contradictions: 0,
            stale_count: 0,
            stale_abstracts: [],
            analytics_rebuilt: true,
            habit_proposals: 0,
            fts_bytes_before: 0,
            fts_bytes_after: 0,
            duck_bytes_before: 0,
            duck_bytes_after: 0,
          },
          errorMessage: null,
        }}
        onClick={vi.fn()}
      />,
    );
    expect(screen.getByRole("button").textContent).toContain("2 err");
  });

  it("shows error message when errored", () => {
    render(
      <PipelineAction
        phase="digest"
        label="Digest"
        icon={<span>D</span>}
        state={{
          status: "error",
          lastRunAt: null,
          lastResult: null,
          errorMessage: "boom",
        }}
        onClick={vi.fn()}
      />,
    );
    expect(screen.getByRole("button").textContent).toContain("boom");
  });
});
