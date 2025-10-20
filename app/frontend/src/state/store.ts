import { configureStore, createSlice, PayloadAction } from "@reduxjs/toolkit";

import { Deck } from "../types";

interface DeckState {
  decks: Deck[];
  selectedDeckId?: string;
}

const initialState: DeckState = {
  decks: [],
};

const deckSlice = createSlice({
  name: "decks",
  initialState,
  reducers: {
    setDecks(state, action: PayloadAction<Deck[]>) {
      state.decks = action.payload;
      state.selectedDeckId = action.payload[0]?.id;
    },
    selectDeck(state, action: PayloadAction<string>) {
      state.selectedDeckId = action.payload;
    },
    upsertDeck(state, action: PayloadAction<Deck>) {
      const index = state.decks.findIndex((deck) => deck.id === action.payload.id);
      if (index >= 0) {
        state.decks[index] = action.payload;
      } else {
        state.decks.push(action.payload);
      }
    },
  },
});

export const { setDecks, selectDeck, upsertDeck } = deckSlice.actions;

export const store = configureStore({
  reducer: {
    decks: deckSlice.reducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
