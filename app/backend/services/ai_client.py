from __future__ import annotations

from dataclasses import dataclass
from typing import List

from ..models.deck import (
    OutlineRequest,
    OutlineResponse,
    OutlineSlide,
    SlideDeck,
    SlideElementText,
)


@dataclass
class AIConfig:
    outline_prompt: str = "You are a presentation copywriter."
    rewrite_prompt: str = "Rewrite the slide content."


class AIClient:
    def __init__(self, config: AIConfig | None = None) -> None:
        self.config = config or AIConfig()

    def generate_outline(self, payload: OutlineRequest) -> OutlineResponse:
        slides: List[OutlineSlide] = []
        target_bullets = {"short": 3, "medium": 4, "long": 6}[payload.length]
        for item in payload.slides:
            title_hint = item.title_hint or f"{payload.topic} {item.page_type_id}"
            title = title_hint.title()
            if payload.topic.lower() not in title.lower():
                title = f"{payload.topic}: {title}".title()
            title = " ".join(title.split()[:8])
            bullets = [
                self._format_bullet(payload.topic, idx, payload.tone)
                for idx in range(target_bullets)
            ]
            notes = self._format_notes(payload.topic, item.page_type_id, payload.length)
            image_prompt = item.image_prompt or self._image_prompt(payload.topic, payload.tone)
            icons = ["feather-trending-up", "feather-target"] if payload.tone == "investor" else []
            slides.append(
                OutlineSlide(
                    page_type_id=item.page_type_id,
                    title=title.title(),
                    bullets=bullets,
                    notes=notes,
                    image_prompt=image_prompt,
                    icons=icons,
                )
            )
        return OutlineResponse(slides=slides)

    def refill_deck(self, deck: SlideDeck, outline: OutlineResponse) -> SlideDeck:
        slide_lookup = {slide.page_type_id: slide for slide in outline.slides}
        for slide in deck.slides:
            outline_slide = slide_lookup.get(slide.page_type_id)
            if not outline_slide:
                continue
            for element in slide.elements:
                if isinstance(element, SlideElementText):
                    if element.placeholder_id and element.placeholder_id.lower().startswith("title"):
                        element.text = outline_slide.title
                    else:
                        element.text = "\n".join(outline_slide.bullets)
        return deck

    def _format_bullet(self, topic: str, index: int, tone: str) -> str:
        verbs = {
            "professional": ["Align", "Quantify", "Outline", "Mitigate", "Deliver", "Elevate"],
            "academic": ["Investigate", "Analyze", "Synthesize", "Validate", "Evaluate", "Document"],
            "marketing": ["Showcase", "Highlight", "Engage", "Convert", "Delight", "Amplify"],
            "investor": ["Scale", "Monetize", "Differentiate", "Optimize", "Forecast", "De-risk"],
        }
        verb = verbs.get(tone, verbs["professional"])[index % 6]
        return f"{verb} {topic} point {index + 1}"

    def _format_notes(self, topic: str, page_type_id: str, length: str) -> str:
        target_words = {"short": 40, "medium": 60, "long": 80}[length]
        base = f"Emphasize how {topic} relates to {page_type_id} outcomes."
        words = base.split()
        if len(words) > target_words:
            words = words[:target_words]
        else:
            words.extend(["Provide", "concise", "context"])
        return " ".join(words[:target_words])

    def _image_prompt(self, topic: str, tone: str) -> str:
        palette = {
            "professional": "sleek corporate illustration",
            "academic": "minimal research diagram",
            "marketing": "vibrant campaign visual",
            "investor": "elegant financial dashboard",
        }
        return f"{palette.get(tone, 'sleek corporate illustration')} for {topic}"
