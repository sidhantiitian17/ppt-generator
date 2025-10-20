from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ..models.deck import (
    CleanAnalyzeResponse,
    CleanApplyResponse,
    CleanRegion,
    CleanUploadResponse,
    SlideCleanReport,
)
from ..services.preview_renderer import PreviewRenderer
from ..services.template_service import TemplateService


@dataclass
class CleanRecord:
    deck_id: str
    page_count: int


class CleanService:
    """Coordinates cleaning flows for uploaded decks.

    The production system would run OCR and inpainting.  For the scaffold we
    simulate the pipeline so the API remains integration-ready while tests stay
    lightweight.
    """

    def __init__(
        self,
        template_service: TemplateService,
        preview_renderer: PreviewRenderer,
        *,
        enable_ocr: bool = False,
    ) -> None:
        self._template_service = template_service
        self._preview_renderer = preview_renderer
        self._registry: dict[str, CleanRecord] = {}
        self._enable_ocr = enable_ocr

    def register_upload(self, deck_id: str) -> CleanUploadResponse:
        # Pretend that we extracted previews for every page of the uploaded deck.
        previews = self._preview_renderer.synthetic_previews(deck_id, page_count=1)
        record = CleanRecord(deck_id=deck_id, page_count=len(previews))
        self._registry[deck_id] = record
        return CleanUploadResponse(deck_id=deck_id, page_count=record.page_count, preview_urls=previews)

    def analyze(self, deck_id: str) -> Optional[CleanAnalyzeResponse]:
        record = self._registry.get(deck_id)
        if not record:
            return None
        regions = [CleanRegion(x=0, y=0, w=100, h=50, method="shape-clear", confidence=0.9)]
        if self._enable_ocr:
            regions.append(
                CleanRegion(
                    x=120,
                    y=80,
                    w=180,
                    h=48,
                    method="inpaint",
                    confidence=0.6,
                )
            )
        report = SlideCleanReport(
            slide_index=0,
            regions=regions,
            had_vector_text=True,
            had_raster_text=self._enable_ocr,
        )
        return CleanAnalyzeResponse(deck_id=deck_id, reports=[report])

    def apply(self, deck_id: str) -> Optional[CleanApplyResponse]:
        record = self._registry.get(deck_id)
        if not record:
            return None
        previews = self._preview_renderer.synthetic_previews(deck_id, page_count=record.page_count)
        return CleanApplyResponse(deck_id=deck_id, cleaned_background_urls=previews)
