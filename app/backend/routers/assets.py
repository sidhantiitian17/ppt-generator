from __future__ import annotations

from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pathlib import Path

from ..models.deck import AssetUploadResponse
from ..utils.dependencies import get_asset_store

router = APIRouter()


async def _save_asset(kind: str, upload: UploadFile, store) -> AssetUploadResponse:
    asset_id = uuid4().hex
    extension = Path(upload.filename or "asset.bin").suffix
    filename = f"{asset_id}{extension}"
    data = await upload.read()
    try:
        path = store.save(filename, data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return AssetUploadResponse(asset_id=asset_id, url=path.as_uri(), kind=kind)  # type: ignore[arg-type]


@router.post("/images", response_model=AssetUploadResponse)
async def upload_image(file: UploadFile = File(...), store=Depends(get_asset_store)) -> AssetUploadResponse:
    return await _save_asset("image", file, store)


@router.post("/fonts", response_model=AssetUploadResponse)
async def upload_font(file: UploadFile = File(...), store=Depends(get_asset_store)) -> AssetUploadResponse:
    return await _save_asset("font", file, store)
