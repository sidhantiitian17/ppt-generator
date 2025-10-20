from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from ..models.deck import PageType, Template, TemplateBlueprint
from ..utils.dependencies import get_template_service

router = APIRouter()


@router.get("/", response_model=List[Template])
async def list_templates(service=Depends(get_template_service)) -> List[Template]:
    return list(service.list_templates())


@router.post("/", response_model=Template)
async def create_template(
    file: UploadFile = File(...),
    name: str | None = Form(None),
    service=Depends(get_template_service),
) -> Template:
    return await service.ingest_upload(file, name)


@router.get("/blueprints", response_model=List[TemplateBlueprint])
async def list_blueprints(service=Depends(get_template_service)) -> List[TemplateBlueprint]:
    return service.list_blueprints()


@router.get("/{template_id}", response_model=Template)
async def get_template(template_id: str, service=Depends(get_template_service)) -> Template:
    template = service.get_template(template_id)
    if template is None:
        raise HTTPException(status_code=404, detail="Template not found")
    return template


@router.post("/{template_id}/page-types", response_model=List[PageType])
async def save_page_types(template_id: str, page_types: List[PageType], service=Depends(get_template_service)) -> List[PageType]:
    try:
        return service.register_page_types(template_id, page_types)
    except KeyError:
        raise HTTPException(status_code=404, detail="Template not found") from None


@router.get("/{template_id}/page-types", response_model=List[PageType])
async def list_page_types(template_id: str, service=Depends(get_template_service)) -> List[PageType]:
    return list(service.list_page_types(template_id))
