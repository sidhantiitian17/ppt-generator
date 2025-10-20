from __future__ import annotations

from datetime import datetime
from typing import Dict, Iterable, Optional
from uuid import uuid4

from ..models.deck import DeckCreateRequest, DeckUpdateRequest, SlideDeck
from ..storage.sqlite_store import SQLiteDeckStore, SQLiteTemplateStore


class DeckService:
    def __init__(self, deck_store: SQLiteDeckStore, template_store: SQLiteTemplateStore) -> None:
        self._deck_store = deck_store
        self._template_store = template_store

    def list(self) -> Iterable[SlideDeck]:
        return self._deck_store.list()

    def get(self, deck_id: str) -> SlideDeck | None:
        return self._deck_store.get(deck_id)

    def create(self, payload: DeckCreateRequest) -> SlideDeck:
        template = self._template_store.get(payload.template_id)
        if template is None:
            raise KeyError(f"template {payload.template_id} not found")
        now = datetime.utcnow()
        hints: Dict[str, Optional[int]] = {
            "keepIntermediates": 0,
            "previewTTL": 3600,
        }
        if payload.storage_hints:
            hints.update({k: v for k, v in payload.storage_hints.items() if v is not None})

        deck = SlideDeck(
            id=uuid4().hex,
            template_id=payload.template_id,
            name=payload.name,
            created_at=now,
            updated_at=now,
            slides=payload.slides,
            storage_hints=hints,
        )
        self._deck_store.save(deck)
        return deck

    def update(self, deck_id: str, payload: DeckUpdateRequest) -> SlideDeck:
        deck = self._deck_store.get(deck_id)
        if deck is None:
            raise KeyError(f"deck {deck_id} not found")
        if payload.name:
            deck.name = payload.name
        if payload.slides:
            deck.slides = payload.slides
        if payload.assets:
            deck.assets = payload.assets
        if payload.storage_hints:
            deck.storage_hints.update({k: v for k, v in payload.storage_hints.items() if v is not None})
        deck.touch()
        self._deck_store.save(deck)
        return deck
