from __future__ import annotations

from pathlib import Path
from typing import List

from PIL import Image, ImageDraw, ImageFont

from .cache import DiskLRUCache


class PreviewRenderer:
    def __init__(
        self,
        preview_dir: Path | None = None,
        cache: DiskLRUCache | None = None,
    ) -> None:
        self.preview_dir = preview_dir or Path("var/previews")
        self.preview_dir.mkdir(parents=True, exist_ok=True)
        self._cache = cache

    def _render_placeholder(self, identifier: str, label: str, page_count: int) -> List[str]:
        urls: List[str] = []
        for index in range(page_count):
            key = f"{identifier}-{index}.png"
            cached = self._cache.get(key) if self._cache else None
            if cached:
                urls.append(cached.as_uri())
                continue

            image = Image.new("RGB", (960, 540), color=(255, 255, 255))
            draw = ImageDraw.Draw(image)
            text = f"{label} {identifier}\nPage {index + 1}"
            try:
                font_obj: ImageFont.ImageFont = ImageFont.truetype("DejaVuSans.ttf", 28)
            except OSError:
                font_obj = ImageFont.load_default()
            font: ImageFont.ImageFont = font_obj
            text_bbox = draw.multiline_textbbox((0, 0), text, font=font, align="center")
            x = (image.width - (text_bbox[2] - text_bbox[0])) // 2
            y = (image.height - (text_bbox[3] - text_bbox[1])) // 2
            draw.multiline_text((x, y), text, fill=(40, 40, 40), font=font, align="center")

            def _writer(path: Path) -> None:
                path.parent.mkdir(parents=True, exist_ok=True)
                image.save(path, format="PNG", optimize=True)

            if self._cache:
                stored = self._cache.store(key, _writer)
            else:
                output = self.preview_dir / key
                _writer(output)
                stored = output
            urls.append(stored.as_uri())
        return urls

    def generate_template_previews(self, template_id: str, page_count: int) -> List[str]:
        return self._render_placeholder(template_id, "Template Preview", page_count)

    def synthetic_previews(self, deck_id: str, page_count: int) -> List[str]:
        return self._render_placeholder(deck_id, "Deck Preview", page_count)
