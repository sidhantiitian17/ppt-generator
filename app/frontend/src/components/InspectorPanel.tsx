import React from "react";
import { useSelector } from "react-redux";

import { selectDeckState } from "../state/selectors";

export const InspectorPanel: React.FC = () => {
  const { decks, selectedDeckId } = useSelector(selectDeckState);
  const deck = decks.find((item) => item.id === selectedDeckId);
  const slide = deck?.slides[0];

  if (!deck || !slide) {
    return (
      <section className="panel inspector-panel empty">
        <h2>Inspector</h2>
        <p>Select a slide to review its layout, placeholders, and notes.</p>
      </section>
    );
  }

  return (
    <section className="panel inspector-panel">
      <header className="panel-header">
        <div>
          <p className="panel-eyebrow">Slide overview</p>
          <h2>{slide.title ?? "Untitled slide"}</h2>
        </div>
        <button type="button" className="ghost-btn small">
          Compare versions
        </button>
      </header>
      <div className="inspector-summary">
        <div>
          <span className="summary-label">Layout</span>
          <span className="summary-value">{slide.layout}</span>
        </div>
        <div>
          <span className="summary-label">Placeholders</span>
          <span className="summary-value">{slide.placeholders.length}</span>
        </div>
        <div>
          <span className="summary-label">Notes length</span>
          <span className="summary-value">{slide.notes?.length ?? 0} chars</span>
        </div>
      </div>
      <div className="inspector-notes">
        <h3>Speaker notes</h3>
        <p>{slide.notes}</p>
        <div className="note-actions">
          <button type="button" className="ghost-btn small">
            Shorten
          </button>
          <button type="button" className="ghost-btn small">
            Elaborate
          </button>
          <button type="button" className="ghost-btn small">
            Change tone
          </button>
        </div>
      </div>
      <div className="placeholder-list">
        <h3>Mapped placeholders</h3>
        <ul>
          {slide.placeholders.map((placeholder) => (
            <li key={placeholder.id}>
              <div className="placeholder-chip">
                <span className={`badge badge-${placeholder.type}`}>
                  {placeholder.type.replace("_", " ")}
                </span>
                <div>
                  <p className="placeholder-title">{placeholder.id}</p>
                  <p className="placeholder-meta">
                    {Math.round(placeholder.width)} × {Math.round(placeholder.height)} px
                  </p>
                </div>
              </div>
              {placeholder.content ? (
                <p className="placeholder-preview">{placeholder.content}</p>
              ) : (
                <p className="placeholder-empty">Awaiting AI content</p>
              )}
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
};
