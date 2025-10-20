from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from ..models.deck import DeckUpdateRequest, OutlineRequest, OutlineResponse, SlideDeck
from ..services.ai_client import AIClient
from ..services.deck_service import DeckService
from ..utils.dependencies import get_ai_client, get_deck_service

router = APIRouter()


@router.post("/outline", response_model=OutlineResponse)
async def outline(payload: OutlineRequest, client: AIClient = Depends(get_ai_client)) -> OutlineResponse:
    return client.generate_outline(payload)


@router.post("/{deck_id}/refill", response_model=SlideDeck)
async def refill(
    deck_id: str,
    outline: OutlineResponse,
    client: AIClient = Depends(get_ai_client),
    deck_service: DeckService = Depends(get_deck_service),
) -> SlideDeck:
    deck = deck_service.get(deck_id)
    if deck is None:
        raise HTTPException(status_code=404, detail="Deck not found")
    updated = client.refill_deck(deck, outline)
    return deck_service.update(deck_id, DeckUpdateRequest(slides=updated.slides))


@router.post("/{deck_id}/refill/stream")
async def refill_stream(
    deck_id: str,
    outline: OutlineResponse,
    client: AIClient = Depends(get_ai_client),
    deck_service: DeckService = Depends(get_deck_service),
) -> StreamingResponse:
    deck = deck_service.get(deck_id)
    if deck is None:
        raise HTTPException(status_code=404, detail="Deck not found")

    def task() -> SlideDeck:
        updated = client.refill_deck(deck, outline)
        return deck_service.update(deck_id, DeckUpdateRequest(slides=updated.slides))

    def iterator():
        yield "queued\n"
        task()
        yield "completed\n"

    return StreamingResponse(iterator(), media_type="text/plain")
