from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable, Optional

from ..models.deck import PageType, SlideDeck, Template


class SQLiteStoreBase:
    """Utility wrapper around a SQLite database with JSON helpers."""

    def __init__(self, db_path: Path) -> None:
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.execute("PRAGMA journal_mode=WAL;")
        self._conn.execute("PRAGMA synchronous=NORMAL;")


class SQLiteTemplateStore(SQLiteStoreBase):
    def __init__(self, db_path: Path) -> None:
        super().__init__(db_path)
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS templates (
                id TEXT PRIMARY KEY,
                payload TEXT NOT NULL
            )
            """
        )
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS template_page_types (
                template_id TEXT NOT NULL,
                page_type_id TEXT NOT NULL,
                payload TEXT NOT NULL,
                PRIMARY KEY (template_id, page_type_id)
            )
            """
        )

    def list(self) -> Iterable[Template]:
        cursor = self._conn.execute("SELECT payload FROM templates ORDER BY rowid DESC")
        for (payload,) in cursor.fetchall():
            yield Template.parse_raw(payload)

    def get(self, template_id: str) -> Optional[Template]:
        cursor = self._conn.execute(
            "SELECT payload FROM templates WHERE id = ?", (template_id,)
        )
        row = cursor.fetchone()
        if not row:
            return None
        return Template.parse_raw(row[0])

    def save(self, template: Template) -> Template:
        payload = template.json()
        self._conn.execute(
            "REPLACE INTO templates(id, payload) VALUES (?, ?)",
            (template.id, payload),
        )
        self._conn.commit()
        return template

    def save_page_type(self, template_id: str, page_type: PageType) -> PageType:
        self._conn.execute(
            "REPLACE INTO template_page_types(template_id, page_type_id, payload) VALUES (?, ?, ?)",
            (template_id, page_type.id, page_type.json()),
        )
        self._conn.commit()
        template = self.get(template_id)
        if template is None:
            raise KeyError(template_id)
        remaining = [pt for pt in template.page_types if pt.id != page_type.id]
        template.page_types = remaining + [page_type]
        self.save(template)
        return page_type

    def list_page_types(self, template_id: str) -> Iterable[PageType]:
        cursor = self._conn.execute(
            "SELECT payload FROM template_page_types WHERE template_id = ?",
            (template_id,),
        )
        for (payload,) in cursor.fetchall():
            yield PageType.parse_raw(payload)


class SQLiteDeckStore(SQLiteStoreBase):
    def __init__(self, db_path: Path) -> None:
        super().__init__(db_path)
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS decks (
                id TEXT PRIMARY KEY,
                payload TEXT NOT NULL
            )
            """
        )

    def list(self) -> Iterable[SlideDeck]:
        cursor = self._conn.execute("SELECT payload FROM decks ORDER BY rowid DESC")
        for (payload,) in cursor.fetchall():
            yield SlideDeck.parse_raw(payload)

    def get(self, deck_id: str) -> Optional[SlideDeck]:
        cursor = self._conn.execute("SELECT payload FROM decks WHERE id = ?", (deck_id,))
        row = cursor.fetchone()
        if not row:
            return None
        return SlideDeck.parse_raw(row[0])

    def save(self, deck: SlideDeck) -> SlideDeck:
        payload = deck.json()
        self._conn.execute(
            "REPLACE INTO decks(id, payload) VALUES (?, ?)",
            (deck.id, payload),
        )
        self._conn.commit()
        return deck

    def delete(self, deck_id: str) -> None:
        self._conn.execute("DELETE FROM decks WHERE id = ?", (deck_id,))
        self._conn.commit()
