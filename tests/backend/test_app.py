from __future__ import annotations

from datetime import datetime
from io import BytesIO
from pathlib import Path

from fastapi.testclient import TestClient
from reportlab.pdfgen import canvas

from app.backend.main import app
from app.backend.models.deck import (
    OutlineRequest,
    PageType,
    Placeholder,
    Slide,
    SlideElementText,
    SlidePlanItem,
    TextStyle,
)

client = TestClient(app)


def _make_pdf() -> bytes:
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    c.drawString(100, 750, "Demo Template")
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.read()


def _create_template() -> str:
    response = client.post(
        "/templates/",
        files={"file": ("template.pdf", _make_pdf(), "application/pdf")},
        data={"name": "Demo Template"},
    )
    assert response.status_code == 200
    template_id = response.json()["id"]

    page_type = PageType(
        id="title-slide",
        name="Title Slide",
        page_index=0,
        placeholders=[
            Placeholder(
                id="title",
                name="Title",
                kind="text",
                x=100,
                y=100,
                width=600,
                height=120,
                default_style=TextStyle(font_family="Helvetica", font_size=36, color="#222222"),
            )
        ],
    )
    resp = client.post(
        f"/templates/{template_id}/page-types",
        json=[page_type.dict()],
    )
    assert resp.status_code == 200
    return template_id


def test_outline_endpoint() -> None:
    payload = OutlineRequest(
        topic="AI Productivity",
        length="long",
        slides=[SlidePlanItem(page_type_id="title-slide", title_hint="Overview")],
    )
    response = client.post("/ai/outline", json=payload.dict())
    assert response.status_code == 200
    data = response.json()
    assert "ai productivity" in data["slides"][0]["title"].lower()
    assert len(data["slides"][0]["bullets"]) >= 5


def test_template_upload_and_page_types() -> None:
    template_id = _create_template()
    response = client.get(f"/templates/{template_id}")
    assert response.status_code == 200
    template = response.json()
    assert template["name"] == "Demo Template"
    assert template["design_dna"]["palette"]
    assert "executive-summary" in template["blueprint_ids"]
    page_types = client.get(f"/templates/{template_id}/page-types").json()
    assert len(page_types) == 1


def test_template_blueprints_endpoint() -> None:
    template_id = _create_template()
    response = client.get("/templates/blueprints")
    assert response.status_code == 200
    data = response.json()
    assert any(bp["id"] == "roadmap" for bp in data)


def test_pdf_render(tmp_path: Path) -> None:
    template_id = _create_template()
    slide = Slide(
        id="slide-1",
        page_type_id="title-slide",
        elements=[
            SlideElementText(
                id="text-1",
                placeholder_id="title",
                text="Welcome",
                style=TextStyle(font_family="Helvetica", font_size=32, color="#000000"),
                box={"x": 100, "y": 400, "width": 600, "height": 120},
            )
        ],
    )
    create_response = client.post(
        "/decks/",
        json={
            "template_id": template_id,
            "name": "Launch Deck",
            "slides": [slide.dict()],
            "storage_hints": {"keepIntermediates": 0},
        },
    )
    assert create_response.status_code == 201
    deck_id = create_response.json()["id"]
    assert create_response.json()["storage_hints"]["previewTTL"] == 3600
    render_response = client.post(f"/render/pdf/{deck_id}")
    assert render_response.status_code == 200
    pdf_path = Path(render_response.json()["path"])
    assert pdf_path.exists()
    assert pdf_path.suffix == ".pdf"
