from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from ..models.deck import DeckCreateRequest, DeckUpdateRequest, SlideDeck
from ..utils.dependencies import get_deck_service

router = APIRouter()


@router.get("/", response_model=List[SlideDeck])
async def list_decks(service=Depends(get_deck_service)) -> List[SlideDeck]:
    return list(service.list())


@router.post("/", response_model=SlideDeck, status_code=status.HTTP_201_CREATED)
async def create_deck(payload: DeckCreateRequest, service=Depends(get_deck_service)) -> SlideDeck:
    return service.create(payload)


@router.get("/{deck_id}", response_model=SlideDeck)
async def get_deck(deck_id: str, service=Depends(get_deck_service)) -> SlideDeck:
    deck = service.get(deck_id)
    if deck is None:
        raise HTTPException(status_code=404, detail="Deck not found")
    return deck


@router.put("/{deck_id}", response_model=SlideDeck)
async def update_deck(deck_id: str, payload: DeckUpdateRequest, service=Depends(get_deck_service)) -> SlideDeck:
    try:
        return service.update(deck_id, payload)
    except KeyError:
        raise HTTPException(status_code=404, detail="Deck not found") from None
