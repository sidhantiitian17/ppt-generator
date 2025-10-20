import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import React from "react";
import { Provider } from "react-redux";

import { selectDeck, store, upsertDeck } from "../state/store";
import { DeckEditor } from "./DeckEditor";

store.dispatch(
  upsertDeck({
    id: "deck-1",
    name: "Demo Deck",
    slides: [],
  })
);

store.dispatch(selectDeck("deck-1"));

const renderWithProviders = (ui: React.ReactElement): void => {
  render(<Provider store={store}>{ui}</Provider>);
};

describe("DeckEditor", () => {
  it("renders deck buttons", () => {
    // The helper wraps React Testing Library's render with providers; the return
    // type is not consumed in this smoke test, so we suppress the strict call
    // check for this invocation.
    // eslint-disable-next-line @typescript-eslint/no-unsafe-call
    renderWithProviders(<DeckEditor />);
    expect(screen.getByText("Demo Deck")).toBeInTheDocument();
  });
});
