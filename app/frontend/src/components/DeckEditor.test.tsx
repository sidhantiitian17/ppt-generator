import { describe, expect, it } from "vitest";
import { render } from "@testing-library/react";
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

const renderWithProviders = (ui: React.ReactElement) =>
  render(<Provider store={store}>{ui}</Provider>);

describe("DeckEditor", () => {
  it("renders deck buttons", () => {
    const { getByText } = renderWithProviders(<DeckEditor />);
    expect(getByText("Demo Deck")).toBeInTheDocument();
  });
});
