from __future__ import annotations

from pathlib import Path
from typing import Dict

from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from ..models.deck import SlideDeck, SlideElementImage, SlideElementText


class PdfRenderer:
    def __init__(self, output_dir: Path | None = None, keep_intermediates: bool = False) -> None:
        self.output_dir = output_dir or Path("var/exports")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self._registered_fonts: Dict[str, str] = {}
        self._keep_intermediates = keep_intermediates

    def _ensure_font(self, name: str, font_path: str | None) -> str:
        if font_path and name not in self._registered_fonts:
            font_file = Path(font_path)
            if font_file.exists():
                pdfmetrics.registerFont(TTFont(name, str(font_file), subsetting=True))
                self._registered_fonts[name] = str(font_file)
        return name

    def render(self, deck: SlideDeck) -> Path:
        output = self.output_dir / f"{deck.id}.pdf"
        c = canvas.Canvas(str(output), pagesize=(1920, 1080))
        c.setTitle(deck.name)

        for slide in deck.slides:
            c.setFillColor(HexColor("#ffffff"))
            c.rect(0, 0, 1920, 1080, fill=True, stroke=False)
            for element in slide.elements:
                if isinstance(element, SlideElementText):
                    font_name = element.style.font_family or "Helvetica"
                    font_name = self._ensure_font(font_name, element.style.font_url)
                    c.setFont(font_name, element.style.font_size)
                    c.setFillColor(HexColor(element.style.color))
                    text_obj = c.beginText(element.box["x"], element.box["y"] + element.box["height"])
                    for line in element.text.split("\n"):
                        text_obj.textLine(line)
                    c.drawText(text_obj)
                elif isinstance(element, SlideElementImage):
                    c.setFillColor(HexColor("#cccccc"))
                    c.rect(
                        element.box["x"],
                        element.box["y"],
                        element.box["width"],
                        element.box["height"],
                        fill=True,
                        stroke=False,
                    )
            c.showPage()

        c.save()
        if not self._keep_intermediates:
            self._prune_old_exports(deck.id)
        return output

    def _prune_old_exports(self, keep_id: str) -> None:
        for pdf in self.output_dir.glob("*.pdf"):
            if pdf.stem == keep_id:
                continue
            try:
                pdf.unlink()
            except FileNotFoundError:
                continue
