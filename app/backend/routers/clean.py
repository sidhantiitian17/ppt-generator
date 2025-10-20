from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from ..context import AppContext
from ..models.deck import CleanAnalyzeResponse, CleanApplyResponse, CleanUploadResponse
from ..utils.dependencies import get_app_context

router = APIRouter()


@router.post("/upload", response_model=CleanUploadResponse)
async def upload(deck_id: str, ctx: AppContext = Depends(get_app_context)) -> CleanUploadResponse:
    return ctx.clean_service.register_upload(deck_id)


@router.post("/{deck_id}/analyze", response_model=CleanAnalyzeResponse)
async def analyze(deck_id: str, ctx: AppContext = Depends(get_app_context)) -> CleanAnalyzeResponse:
    report = ctx.clean_service.analyze(deck_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Deck not found for cleaning")
    return report


@router.post("/{deck_id}/apply", response_model=CleanApplyResponse)
async def apply(deck_id: str, ctx: AppContext = Depends(get_app_context)) -> CleanApplyResponse:
    result = ctx.clean_service.apply(deck_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Deck not found for cleaning")
    return result
