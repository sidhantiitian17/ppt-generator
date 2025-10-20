from __future__ import annotations

from pathlib import Path
from typing import Iterable, List
from uuid import uuid4

from fastapi import UploadFile

from ..models.deck import (
    DesignDNA,
    PageType,
    Template,
    TemplateBlueprint,
    TemplatePage,
    ColorSwatch,
)
from ..storage.sqlite_store import SQLiteTemplateStore
from .preview_renderer import PreviewRenderer


class TemplateService:
    """Handle ingestion of PDF/PPTX templates and derived metadata."""

    def __init__(
        self,
        template_store: SQLiteTemplateStore,
        preview_renderer: PreviewRenderer,
        template_dir: Path | None = None,
        blueprint_library: List[TemplateBlueprint] | None = None,
    ) -> None:
        self._template_store = template_store
        self._preview_renderer = preview_renderer
        self._template_dir = template_dir or Path("var/templates")
        self._template_dir.mkdir(parents=True, exist_ok=True)
        self._blueprints = blueprint_library or self._build_default_blueprints()

    def list_templates(self) -> Iterable[Template]:
        return self._template_store.list()

    def get_template(self, template_id: str) -> Template | None:
        return self._template_store.get(template_id)

    async def ingest_upload(self, upload: UploadFile, name: str | None = None) -> Template:
        suffix = Path(upload.filename or "template.pdf").suffix or ".pdf"
        template_id = uuid4().hex
        destination = self._template_dir / f"{template_id}{suffix}"
        destination.write_bytes(await upload.read())

        # Generate stub previews (real implementation would render each page).
        preview_urls = self._preview_renderer.generate_template_previews(template_id, page_count=1)
        pages = [
            TemplatePage(page_index=index, preview_url=url, width=1920, height=1080)
            for index, url in enumerate(preview_urls)
        ]
        dna = self._extract_design_dna(destination)
        template = Template(
            id=template_id,
            name=name or upload.filename or "Template",
            source_path=str(destination),
            pages=pages,
            design_dna=dna,
            blueprint_ids=[bp.id for bp in self._blueprints],
        )
        self._template_store.save(template)
        return template

    def register_page_types(self, template_id: str, page_types: List[PageType]) -> List[PageType]:
        stored = self._template_store.get(template_id)
        if stored is None:
            raise KeyError(f"template {template_id} not found")
        for page_type in page_types:
            self._template_store.save_page_type(template_id, page_type)
        return list(self._template_store.list_page_types(template_id))

    def list_page_types(self, template_id: str) -> Iterable[PageType]:
        return self._template_store.list_page_types(template_id)

    def list_blueprints(self) -> List[TemplateBlueprint]:
        return list(self._blueprints)

    def _extract_design_dna(self, source_path: Path) -> DesignDNA:
        """Generate a compact "design DNA" summary for the uploaded template."""

        palette = [
            ColorSwatch(hex="#0F172A", usage="text"),
            ColorSwatch(hex="#2563EB", usage="accent"),
            ColorSwatch(hex="#F8FAFC", usage="background"),
        ]
        fonts = ["Helvetica", "Helvetica-Bold"]
        guides = ["margin:40", "grid:12"]
        return DesignDNA(palette=palette, fonts=fonts, guides=guides)

    def _build_default_blueprints(self) -> List[TemplateBlueprint]:
        return [
            TemplateBlueprint(
                id="executive-summary",
                name="Executive Summary",
                description="High-level overview highlighting objectives and key takeaways.",
            ),
            TemplateBlueprint(
                id="pain-points",
                name="Pain Points",
                description="Showcase current challenges before introducing solutions.",
            ),
            TemplateBlueprint(
                id="architecture",
                name="Architecture",
                description="Layered architecture blocks for systems and integrations.",
            ),
            TemplateBlueprint(
                id="comparison",
                name="Comparison",
                description="Side-by-side comparison grid for features or competitors.",
            ),
            TemplateBlueprint(
                id="metrics",
                name="Metrics",
                description="Data card layout suitable for KPIs and quick stats.",
            ),
            TemplateBlueprint(
                id="roadmap",
                name="Roadmap",
                description="Timeline blocks for quarterly or monthly milestones.",
            ),
        ]
