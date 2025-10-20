import React, { useMemo } from "react";
import { useDispatch, useSelector } from "react-redux";

import { LivePreview } from "./LivePreview";
import { selectDeck } from "../state/store";
import { selectDeckState } from "../state/selectors";

const quickActions = [
  { label: "Regenerate", description: "Ask AI for a fresh take" },
  { label: "Shorter", description: "Trim bullets to essentials" },
  { label: "Longer", description: "Add supporting detail" },
  { label: "Change tone", description: "Switch voice instantly" },
  { label: "Create diagram", description: "Build a flow or architecture" },
];

export const DeckEditor: React.FC = () => {
  const dispatch = useDispatch();
  const { decks, selectedDeckId } = useSelector(selectDeckState);
  const selectedDeck = decks.find((deck) => deck.id === selectedDeckId);
  const activeSlide = useMemo(() => selectedDeck?.slides[0], [selectedDeck]);

  return (
    <section className="panel deck-panel">
      <header className="panel-header">
        <div>
          <p className="panel-eyebrow">Deck crafting</p>
          <h2>AI-powered editor</h2>
        </div>
        <div className="panel-actions">
          <button type="button" className="ghost-btn small">
            Undo
          </button>
          <button type="button" className="ghost-btn small">
            Redo
          </button>
        </div>
      </header>

      <div className="deck-selector">
        {decks.map((deck) => (
          <button
            key={deck.id}
            className={`deck-chip ${deck.id === selectedDeckId ? "active" : ""}`}
            onClick={() => dispatch(selectDeck(deck.id))}
            type="button"
          >
            <span className="deck-name">{deck.name}</span>
            <span className="deck-meta">{deck.slides.length} slides</span>
          </button>
        ))}
        <button type="button" className="ghost-btn small add-deck">
          + New deck
        </button>
      </div>

      {selectedDeck ? (
        <>
          <div className="deck-workspace">
            <div className="thumbnail-rail">
              <h3>Slides</h3>
              <ul>
                {selectedDeck.slides.map((slide, index) => (
                  <li key={slide.id} className={index === 0 ? "active" : ""}>
                    <span className="thumb-index">{index + 1}</span>
                    <div className="thumb-meta">
                      <p>{slide.title}</p>
                      <small>{slide.layout}</small>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
            <div className="canvas-shell">
              {activeSlide ? (
                <LivePreview deck={selectedDeck} />
              ) : (
                <div className="empty-state">Select a slide to start editing.</div>
              )}
            </div>
          </div>

          <div className="quick-actions">
            {quickActions.map((action) => (
              <button type="button" key={action.label} className="quick-action">
                <span className="action-label">{action.label}</span>
                <span className="action-description">{action.description}</span>
              </button>
            ))}
          </div>
        </>
      ) : (
        <p className="empty-state">Select or create a deck to begin.</p>
      )}
    </section>
  );
};
