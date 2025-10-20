import React from "react";
import { vi } from "vitest";
import "@testing-library/jest-dom/vitest";

const KonvaStub: React.FC<{ children?: React.ReactNode }> = ({ children }) =>
  React.createElement("div", { "data-testid": "konva-stub" }, children);

vi.mock("react-konva", () => ({
  Stage: KonvaStub,
  Layer: KonvaStub,
  Rect: KonvaStub,
  Text: KonvaStub,
}));
