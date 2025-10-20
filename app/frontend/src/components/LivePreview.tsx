import React from "react";
import { Stage, Layer, Rect, Text } from "react-konva";

import { Deck } from "../types";

interface LivePreviewProps {
  deck: Deck;
}

export const LivePreview: React.FC<LivePreviewProps> = ({ deck }) => {
  const slide = deck.slides[0];

  if (!slide) {
    return <p className="empty-state">No slides available.</p>;
  }

  const scale = 0.7;
  const offsetX = 42;
  const offsetY = 36;

  return (
    <div className="live-preview">
      <div className="preview-header">
        <div>
          <h3>{slide.title}</h3>
          <p>{slide.layout} layout · synced with AI copywriter</p>
        </div>
        <button type="button" className="ghost-btn small">
          Before / After
        </button>
      </div>
      <Stage width={680} height={380} className="preview-stage live-stage">
        <Layer>
          <Rect
            x={0}
            y={0}
            width={680}
            height={380}
            cornerRadius={22}
            fillLinearGradientStartPoint={{ x: 80, y: 20 }}
            fillLinearGradientEndPoint={{ x: 640, y: 360 }}
            fillLinearGradientColorStops={[0, "#0f172a", 1, "#1d4ed8"]}
            shadowColor="rgba(15, 23, 42, 0.4)"
            shadowBlur={25}
            opacity={0.95}
          />
          {slide.placeholders.map((placeholder, index) => {
            const width = placeholder.width * scale;
            const height = placeholder.height * scale;
            const x = placeholder.x * scale + offsetX;
            const y = placeholder.y * scale + offsetY;

            return (
              <React.Fragment key={placeholder.id}>
                <Rect
                  x={x}
                  y={y}
                  width={width}
                  height={height}
                  cornerRadius={14}
                  strokeWidth={2}
                  stroke={index % 2 === 0 ? "#38bdf8" : "#c084fc"}
                  fill="rgba(15, 118, 110, 0.08)"
                  dash={[12, 6]}
                />
                <Text
                  text={placeholder.content ?? placeholder.type}
                  x={x + 14}
                  y={y + 18}
                  width={width - 28}
                  height={height - 28}
                  fill="#e0f2fe"
                  fontStyle="bold"
                  fontSize={16}
                />
              </React.Fragment>
            );
          })}
        </Layer>
      </Stage>
    </div>
  );
};
