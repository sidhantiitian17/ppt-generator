from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from ..models.deck import PdfRenderResponse, PreviewResponse
from ..utils.dependencies import get_deck_service, get_pdf_renderer, get_preview_renderer

router = APIRouter()


@router.post("/preview/{deck_id}", response_model=PreviewResponse)
async def render_preview(deck_id: str, preview_renderer=Depends(get_preview_renderer), deck_service=Depends(get_deck_service)) -> PreviewResponse:
    deck = deck_service.get(deck_id)
    if deck is None:
        raise HTTPException(status_code=404, detail="Deck not found")
    previews = preview_renderer.synthetic_previews(deck_id, len(deck.slides))
    return PreviewResponse(deck_id=deck_id, previews=previews)


@router.post("/pdf/{deck_id}", response_model=PdfRenderResponse)
async def render_pdf(deck_id: str, pdf_renderer=Depends(get_pdf_renderer), deck_service=Depends(get_deck_service)) -> PdfRenderResponse:
    deck = deck_service.get(deck_id)
    if deck is None:
        raise HTTPException(status_code=404, detail="Deck not found")
    path = pdf_renderer.render(deck)
    return PdfRenderResponse(deck_id=deck_id, path=str(path))
