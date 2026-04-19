import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { Resizer } from "../Resizer";

describe("Resizer", () => {
  it("exposes ARIA attributes for a horizontal separator", () => {
    render(
      <Resizer
        axis="x"
        min={100}
        max={400}
        value={200}
        onChange={vi.fn()}
        ariaLabel="Resize list"
      />,
    );
    const sep = screen.getByRole("separator", { name: "Resize list" });
    expect(sep).toHaveAttribute("aria-orientation", "vertical");
    expect(sep).toHaveAttribute("aria-valuenow", "200");
    expect(sep).toHaveAttribute("aria-valuemin", "100");
    expect(sep).toHaveAttribute("aria-valuemax", "400");
  });

  it("ArrowRight on x-axis fires onChange with value + 10", () => {
    const onChange = vi.fn();
    render(
      <Resizer
        axis="x"
        min={100}
        max={400}
        value={200}
        onChange={onChange}
        ariaLabel="Resize list"
      />,
    );
    const sep = screen.getByRole("separator");
    fireEvent.keyDown(sep, { key: "ArrowRight" });
    expect(onChange).toHaveBeenCalledWith(210);
  });

  it("ArrowLeft on x-axis fires onChange with value - 10", () => {
    const onChange = vi.fn();
    render(
      <Resizer
        axis="x"
        min={100}
        max={400}
        value={200}
        onChange={onChange}
        ariaLabel="Resize"
      />,
    );
    fireEvent.keyDown(screen.getByRole("separator"), { key: "ArrowLeft" });
    expect(onChange).toHaveBeenCalledWith(190);
  });

  it("Shift+ArrowRight uses a step of 50", () => {
    const onChange = vi.fn();
    render(
      <Resizer
        axis="x"
        min={100}
        max={400}
        value={200}
        onChange={onChange}
        ariaLabel="Resize"
      />,
    );
    fireEvent.keyDown(screen.getByRole("separator"), {
      key: "ArrowRight",
      shiftKey: true,
    });
    expect(onChange).toHaveBeenCalledWith(250);
  });

  it("clamps keyboard moves to min/max", () => {
    const onChange = vi.fn();
    render(
      <Resizer
        axis="x"
        min={100}
        max={400}
        value={395}
        onChange={onChange}
        ariaLabel="Resize"
      />,
    );
    fireEvent.keyDown(screen.getByRole("separator"), {
      key: "ArrowRight",
      shiftKey: true,
    });
    expect(onChange).toHaveBeenCalledWith(400);
  });

  it("Home and End snap to bounds", () => {
    const onChange = vi.fn();
    render(
      <Resizer
        axis="x"
        min={100}
        max={400}
        value={240}
        onChange={onChange}
        ariaLabel="Resize"
      />,
    );
    const sep = screen.getByRole("separator");
    fireEvent.keyDown(sep, { key: "Home" });
    expect(onChange).toHaveBeenLastCalledWith(100);
    fireEvent.keyDown(sep, { key: "End" });
    expect(onChange).toHaveBeenLastCalledWith(400);
  });

  it("invert=true reverses the keyboard direction", () => {
    const onChange = vi.fn();
    render(
      <Resizer
        axis="x"
        min={100}
        max={400}
        value={200}
        onChange={onChange}
        invert
        ariaLabel="Resize"
      />,
    );
    // With invert, ArrowRight should *decrease* — left-edge handle semantics.
    fireEvent.keyDown(screen.getByRole("separator"), { key: "ArrowRight" });
    expect(onChange).toHaveBeenCalledWith(190);
  });

  it("y-axis uses ArrowUp/ArrowDown instead of ArrowLeft/ArrowRight", () => {
    const onChange = vi.fn();
    render(
      <Resizer
        axis="y"
        min={100}
        max={400}
        value={200}
        onChange={onChange}
        ariaLabel="Resize"
      />,
    );
    const sep = screen.getByRole("separator");
    expect(sep).toHaveAttribute("aria-orientation", "horizontal");
    fireEvent.keyDown(sep, { key: "ArrowDown" });
    expect(onChange).toHaveBeenCalledWith(210);
    fireEvent.keyDown(sep, { key: "ArrowRight" });
    // ArrowRight should be ignored on y-axis.
    expect(onChange).toHaveBeenCalledTimes(1);
  });
});
