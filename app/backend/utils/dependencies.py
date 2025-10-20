from __future__ import annotations

from fastapi import Depends, FastAPI, Request

from ..context import AppContext
from ..services.ai_client import AIClient
from ..services.clean_service import CleanService
from ..services.deck_service import DeckService
from ..services.pdf_renderer import PdfRenderer
from ..services.preview_renderer import PreviewRenderer
from ..services.template_service import TemplateService
from ..storage.asset_store import AssetStore


def get_app(request: Request) -> FastAPI:
    return request.app


def get_app_context(app: FastAPI = Depends(get_app)) -> AppContext:
    return app.state.ctx


def get_template_service(ctx: AppContext = Depends(get_app_context)) -> TemplateService:
    return ctx.template_service


def get_deck_service(ctx: AppContext = Depends(get_app_context)) -> DeckService:
    return ctx.deck_service


def get_ai_client(ctx: AppContext = Depends(get_app_context)) -> AIClient:
    return ctx.ai_client


def get_preview_renderer(ctx: AppContext = Depends(get_app_context)) -> PreviewRenderer:
    return ctx.preview_renderer


def get_pdf_renderer(ctx: AppContext = Depends(get_app_context)) -> PdfRenderer:
    return ctx.pdf_renderer


def get_asset_store(ctx: AppContext = Depends(get_app_context)) -> AssetStore:
    return ctx.asset_store


def get_clean_service(ctx: AppContext = Depends(get_app_context)) -> CleanService:
    return ctx.clean_service
