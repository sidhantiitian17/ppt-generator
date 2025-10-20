import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";

import { DeckEditor } from "./components/DeckEditor";
import { InspectorPanel } from "./components/InspectorPanel";
import { TemplateMapper } from "./components/TemplateMapper";
import { setDecks, type AppDispatch, type RootState } from "./state/store";
import { useTemplateStore } from "./state/templates";
import { Deck, Template } from "./types";

import "./styles.css";

const demoTemplate: Template = {
  id: "template-aurora",
  name: "Aurora Gradient",
  slides: [
    {
      id: "template-slide-1",
      title: "Title Slide",
      layout: "hero",
      placeholders: [
        {
          id: "title",
          type: "text",
          x: 48,
          y: 48,
          width: 520,
          height: 120,
          rotation: 0,
          content: "Welcome to LuminaDeck",
        },
        {
          id: "subtitle",
          type: "text",
          x: 48,
          y: 188,
          width: 420,
          height: 72,
          rotation: 0,
          content: "Design-first AI presentations",
        },
        {
          id: "hero-image",
          type: "image",
          x: 520,
          y: 36,
          width: 320,
          height: 240,
          rotation: 0,
        },
      ],
    },
  ],
};

const demoDeck: Deck = {
  id: "deck-aurora",
  name: "Investor Pitch",
  slides: [
    {
      id: "slide-1",
      title: "Vision & Momentum",
      layout: "hero",
      notes:
        "Highlight market traction and outline the product differentiators that matter most to the audience.",
      placeholders: [
        {
          id: "title",
          type: "text",
          x: 64,
          y: 64,
          width: 520,
          height: 110,
          rotation: 0,
          content: "Reimagining smart teams with AI copilots",
        },
        {
          id: "subtitle",
          type: "text",
          x: 64,
          y: 190,
          width: 420,
          height: 90,
          rotation: 0,
          content:
            "AI-crafted storytelling, beautiful templates, and instant refinements keep your message focused.",
        },
        {
          id: "bullets",
          type: "bullet_list",
          x: 64,
          y: 300,
          width: 360,
          height: 140,
          rotation: 0,
          content:
            "• 42 enterprise pilots completed\n• 3x faster deck revisions\n• Brand-safe exports every time",
        },
        {
          id: "hero",
          type: "image",
          x: 480,
          y: 120,
          width: 360,
          height: 220,
          rotation: 0,
        },
      ],
    },
    {
      id: "slide-2",
      title: "Product Pillars",
      layout: "three-column",
      notes: "Summarise three pillars with supporting detail and CTA.",
      placeholders: [
        {
          id: "pillar-1",
          type: "text",
          x: 60,
          y: 80,
          width: 220,
          height: 200,
          rotation: 0,
          content:
            "Discovery\n • Upload custom templates\n • Extract brand DNA\n • Smart placeholder mapping",
        },
        {
          id: "pillar-2",
          type: "text",
          x: 320,
          y: 80,
          width: 220,
          height: 200,
          rotation: 0,
          content:
            "Compose\n • Guided outline co-pilot\n • Tone & length controls\n • Diagram and chart blocks",
        },
        {
          id: "pillar-3",
          type: "text",
          x: 580,
          y: 80,
          width: 220,
          height: 200,
          rotation: 0,
          content:
            "Deliver\n • Contrast-aware layouts\n • Vector PDF export\n • Shareable preview links",
        },
      ],
    },
  ],
};

const App: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const addTemplate = useTemplateStore((state) => state.addTemplate);
  const templateCount = useTemplateStore((state) => state.templates.length);
  const deckCount = useSelector((state: RootState) => state.decks.decks.length);

  useEffect(() => {
    if (templateCount === 0) {
      addTemplate(demoTemplate);
    }
  }, [addTemplate, templateCount]);

  useEffect(() => {
    if (deckCount === 0) {
      dispatch(setDecks([demoDeck]));
    }
  }, [deckCount, dispatch]);

  return (
    <div className="app-shell">
      <aside className="app-sidebar">
        <div className="brand-mark">
          <span className="brand-glow" />
          <h1>LuminaDeck</h1>
          <p>AI-first presentation studio</p>
        </div>
        <nav className="workflow-nav">
          <p className="nav-label">Workflow</p>
          <ol>
            <li className="active">Upload & map placeholders</li>
            <li>Clean slide backgrounds</li>
            <li>Generate AI outline</li>
            <li>Design & refine</li>
            <li>Export vector-perfect PDF</li>
          </ol>
        </nav>
        <div className="sidebar-card">
          <h3>Brand pulse</h3>
          <p>
            Palette, typography, and spacing from your template are carried into each
            AI suggestion.
          </p>
          <div className="progress-track">
            <span style={{ width: "68%" }} />
          </div>
          <small>68% of slides refined</small>
        </div>
      </aside>
      <div className="app-content">
        <header className="app-topbar">
          <div>
            <h2>Pitch deck workspace</h2>
            <p>Upload, map, and compose in a single flow with instant AI assistance.</p>
          </div>
          <div className="topbar-actions">
            <button type="button" className="ghost-btn">
              View docs
            </button>
            <button type="button" className="primary-btn">
              Export deck
            </button>
          </div>
        </header>
        <main className="app-main">
          <TemplateMapper />
          <DeckEditor />
          <InspectorPanel />
        </main>
      </div>
    </div>
  );
};

export default App;
