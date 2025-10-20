import React from "react";
import { Stage, Layer, Rect, Text } from "react-konva";

import { useTemplateStore } from "../state/templates";

export const TemplateMapper: React.FC = () => {
  const { templates } = useTemplateStore();
  const template = templates[0];

  return (
    <section className="panel template-panel">
      <header className="panel-header">
        <div>
          <p className="panel-eyebrow">Template DNA</p>
          <h2>Placeholder mapping</h2>
        </div>
        <div className="panel-actions">
          <button type="button" className="ghost-btn small">
            Import template
          </button>
          <button type="button" className="ghost-btn small">
            Auto-detect
          </button>
        </div>
      </header>
      <div className="dropzone">
        <div>
          <strong>Drag & drop</strong> a PDF or PPTX template
          <p>Files stay private. We only keep the design DNA you approve.</p>
        </div>
        <button type="button" className="primary-btn">
          Browse files
        </button>
      </div>
      {template ? (
        <div className="template-preview">
          <div className="template-meta">
            <h3>{template.name}</h3>
            <p>
              {template.slides.length} mapped slide{template.slides.length === 1 ? "" : "s"}
              . Placeholders are colour-coded below.
            </p>
          </div>
          <Stage width={340} height={200} className="preview-stage template-stage">
            <Layer>
              <Rect
                x={0}
                y={0}
                width={340}
                height={200}
                cornerRadius={18}
                fillLinearGradientStartPoint={{ x: 0, y: 0 }}
                fillLinearGradientEndPoint={{ x: 340, y: 200 }}
                fillLinearGradientColorStops={[0, "#111827", 1, "#1f3a8a"]}
                opacity={0.9}
              />
              {template.slides[0]?.placeholders.map((placeholder, index) => (
                <Rect
                  key={placeholder.id}
                  x={placeholder.x * 0.45 + 24}
                  y={placeholder.y * 0.45 + 24}
                  width={placeholder.width * 0.45}
                  height={placeholder.height * 0.45}
                  cornerRadius={10}
                  strokeWidth={2}
                  stroke={index % 2 === 0 ? "#60a5fa" : "#f472b6"}
                  dash={[8, 6]}
                  shadowColor="rgba(14, 116, 144, 0.45)"
                  shadowBlur={10}
                />
              ))}
              <Text text="Template live preview" x={24} y={20} fill="#f8fafc" fontSize={16} />
            </Layer>
          </Stage>
        </div>
      ) : (
        <p className="empty-state">No templates uploaded yet.</p>
      )}
    </section>
  );
};
