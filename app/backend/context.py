from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path

from .services.ai_client import AIClient
from .services.cache import DiskLRUCache
from .services.clean_service import CleanService
from .services.deck_service import DeckService
from .services.pdf_renderer import PdfRenderer
from .services.preview_renderer import PreviewRenderer
from .services.template_service import TemplateService
from .storage.asset_store import AssetStore
from .storage.sqlite_store import SQLiteDeckStore, SQLiteTemplateStore


@dataclass
class AppContext:
    template_service: TemplateService
    deck_service: DeckService
    preview_renderer: PreviewRenderer
    pdf_renderer: PdfRenderer
    ai_client: AIClient
    asset_store: AssetStore
    clean_service: CleanService


@dataclass
class AppSettings:
    enable_ocr: bool
    preview_cache_bytes: int
    preview_ttl_seconds: int
    keep_intermediates: bool
    max_upload_bytes: int

    @classmethod
    def load(cls) -> "AppSettings":
        return cls(
            enable_ocr=os.getenv("ENABLE_OCR", "0") == "1",
            preview_cache_bytes=int(os.getenv("PREVIEW_CACHE_MB", "200")) * 1024 * 1024,
            preview_ttl_seconds=int(os.getenv("PREVIEW_TTL_SEC", "3600")),
            keep_intermediates=os.getenv("KEEP_INTERMEDIATES", "0") == "1",
            max_upload_bytes=int(os.getenv("MAX_UPLOAD_MB", "30")) * 1024 * 1024,
        )


def build_context(base_path: Path) -> AppContext:
    settings = AppSettings.load()
    storage_dir = base_path / "var"
    storage_dir.mkdir(exist_ok=True)
    previews_dir = storage_dir / "previews"
    previews_dir.mkdir(exist_ok=True)
    pdf_dir = storage_dir / "pdf"
    pdf_dir.mkdir(exist_ok=True)
    assets_dir = storage_dir / "assets"
    assets_dir.mkdir(exist_ok=True)
    db_path = storage_dir / "app.db"

    template_store = SQLiteTemplateStore(db_path)
    deck_store = SQLiteDeckStore(db_path)
    asset_store = AssetStore(assets_dir, max_bytes=settings.max_upload_bytes)

    cache = DiskLRUCache(previews_dir, settings.preview_cache_bytes, settings.preview_ttl_seconds)
    preview_renderer = PreviewRenderer(previews_dir, cache=cache)
    pdf_renderer = PdfRenderer(pdf_dir, keep_intermediates=settings.keep_intermediates)
    template_service = TemplateService(template_store, preview_renderer)
    deck_service = DeckService(deck_store, template_store)
    clean_service = CleanService(template_service, preview_renderer, enable_ocr=settings.enable_ocr)
    ai_client = AIClient()

    return AppContext(
        template_service=template_service,
        deck_service=deck_service,
        preview_renderer=preview_renderer,
        pdf_renderer=pdf_renderer,
        ai_client=ai_client,
        asset_store=asset_store,
        clean_service=clean_service,
    )
