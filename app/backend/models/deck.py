from __future__ import annotations

"""Core Pydantic models shared across the presentation pipeline.

The data layer mirrors the structures described in the product requirements so
routers and services can exchange strongly typed payloads.  The models stay
fairly lightweight – validation and computed helpers live in the service layer.
"""

from datetime import datetime
from typing import Dict, List, Literal, Optional, Sequence, Union

from pydantic import BaseModel, Field, validator

PlaceholderKind = Literal["text", "image"]
TextAlign = Literal["left", "center", "right", "justify"]
Tone = Literal["professional", "academic", "marketing", "investor"]
ImageFit = Literal["contain", "cover"]
BulletStyle = Literal["disc", "dash", "numbered"]
CleanMethod = Literal["shape-clear", "pdf-redact", "inpaint"]
LengthMode = Literal["short", "medium", "long"]


class TextBullet(BaseModel):
    style: BulletStyle = "disc"
    indent_px: int = 24


class TextStyle(BaseModel):
    font_family: str = "Helvetica"
    font_url: Optional[str] = None
    font_size: float = 32
    color: str = "#000000"
    line_height: float = 1.2
    align: TextAlign = "left"
    weight: Literal["regular", "bold"] = "regular"
    italic: bool = False
    bullet: Optional[TextBullet] = None
    letter_spacing: Optional[float] = None
    box_padding: Optional[float] = None
    opacity: Optional[float] = 1.0
    shadow: Optional[str] = None


class Placeholder(BaseModel):
    id: str
    name: str
    kind: PlaceholderKind
    x: float
    y: float
    width: float
    height: float
    z_index: int = 0
    default_style: Optional[TextStyle] = None

    @validator("width", "height")
    def _ensure_positive(cls, value: float) -> float:  # noqa: N805
        if value <= 0:
            raise ValueError("placeholders must have positive dimensions")
        return value


class ColorSwatch(BaseModel):
    hex: str
    usage: Literal["background", "accent", "text", "neutral"] = "accent"


class DesignDNA(BaseModel):
    palette: List[ColorSwatch] = Field(default_factory=list)
    fonts: List[str] = Field(default_factory=list)
    guides: List[str] = Field(default_factory=list)


class TemplateBlueprint(BaseModel):
    id: str
    name: str
    description: str
    recommended_page_type_id: Optional[str] = None


class TemplatePage(BaseModel):
    page_index: int
    preview_url: str
    width: float
    height: float


class PageType(BaseModel):
    id: str
    name: str
    page_index: int
    placeholders: List[Placeholder] = Field(default_factory=list)


class Template(BaseModel):
    id: str
    name: str
    source_path: Optional[str] = None
    pages: List[TemplatePage] = Field(default_factory=list)
    page_types: List[PageType] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    design_dna: Optional[DesignDNA] = None
    blueprint_ids: List[str] = Field(default_factory=list)

    def page_type(self, page_type_id: str) -> PageType:
        for page_type in self.page_types:
            if page_type.id == page_type_id:
                return page_type
        raise KeyError(page_type_id)


class CleanRegion(BaseModel):
    x: float
    y: float
    w: float
    h: float
    method: CleanMethod
    confidence: float


class SlideCleanReport(BaseModel):
    slide_index: int
    regions: List[CleanRegion] = Field(default_factory=list)
    had_vector_text: bool = False
    had_raster_text: bool = False


class SlideElementText(BaseModel):
    id: str
    type: Literal["text"] = "text"
    placeholder_id: Optional[str] = None
    text: str
    style: TextStyle
    box: Dict[str, float]


class SlideElementImage(BaseModel):
    id: str
    type: Literal["image"] = "image"
    placeholder_id: Optional[str] = None
    image_url: str
    box: Dict[str, float]
    object_fit: ImageFit = "contain"


SlideElement = Union[SlideElementText, SlideElementImage]


class Slide(BaseModel):
    id: str
    page_type_id: str
    elements: List[SlideElement] = Field(default_factory=list)
    notes: Optional[str] = None
    clean_report: Optional[SlideCleanReport] = None
    cleaned_background_url: Optional[str] = None
    original_preview_url: Optional[str] = None


class DeckAsset(BaseModel):
    id: str
    kind: Literal["image", "font"]
    url: str
    meta: Dict[str, str] = Field(default_factory=dict)


class SlideDeck(BaseModel):
    id: str
    template_id: str
    name: str
    created_at: datetime
    updated_at: datetime
    slides: List[Slide] = Field(default_factory=list)
    assets: List[DeckAsset] = Field(default_factory=list)
    storage_hints: Dict[str, Optional[int]] = Field(
        default_factory=lambda: {"keepIntermediates": 0, "previewTTL": 3600}
    )

    def touch(self) -> None:
        self.updated_at = datetime.utcnow()


class SlidePlanItem(BaseModel):
    page_type_id: str
    title_hint: Optional[str] = None
    bullet_hints: Optional[List[str]] = None
    image_prompt: Optional[str] = None
    notes_hint: Optional[str] = None


class SlidePlan(BaseModel):
    topic: str
    tone: Optional[Tone] = "professional"
    length: LengthMode = "medium"
    global_style: Optional[TextStyle] = None
    slides: Sequence[SlidePlanItem]


class OutlineRequest(BaseModel):
    topic: str
    tone: Tone = "professional"
    length: LengthMode = "medium"
    slides: Sequence[SlidePlanItem]


class OutlineSlide(BaseModel):
    page_type_id: str
    title: str
    bullets: List[str]
    notes: str
    image_prompt: str
    icons: List[str] = Field(default_factory=list)


class OutlineResponse(BaseModel):
    slides: List[OutlineSlide]


class DeckCreateRequest(BaseModel):
    template_id: str
    name: str
    slides: List[Slide]
    storage_hints: Optional[Dict[str, Optional[int]]] = None


class DeckUpdateRequest(BaseModel):
    name: Optional[str] = None
    slides: Optional[List[Slide]] = None
    assets: Optional[List[DeckAsset]] = None
    storage_hints: Optional[Dict[str, Optional[int]]] = None


class CleanUploadResponse(BaseModel):
    deck_id: str
    page_count: int
    preview_urls: List[str]


class CleanAnalyzeResponse(BaseModel):
    deck_id: str
    reports: List[SlideCleanReport]


class CleanApplyResponse(BaseModel):
    deck_id: str
    cleaned_background_urls: List[str]


class PreviewRequest(BaseModel):
    deck_id: str
    dpi: int = 220


class PreviewResponse(BaseModel):
    deck_id: str
    previews: List[str]


class PdfRenderRequest(BaseModel):
    deck_id: str


class PdfRenderResponse(BaseModel):
    deck_id: str
    path: str


class AssetUploadResponse(BaseModel):
    asset_id: str
    url: str
    kind: Literal["image", "font"]


class AuthRequest(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
