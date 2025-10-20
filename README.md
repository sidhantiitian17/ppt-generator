# PPT Generator

This repository delivers a lean AI-powered presentation generator.  The backend is a FastAPI service that ingests custom templates (PDF/PPTX), cleans content, orchestrates AI copy, and exports lightweight PDFs with embedded subset fonts.  A Vite-powered React frontend consumes the API for Canva-like editing while keeping the deployable image size small.

## Backend

* FastAPI application under `app/backend` with routers for authentication, templates (including design DNA + blueprint catalog), cleaning, AI outline/refill, decks, rendering, and asset uploads.
* Services favour small storage footprints: previews stream through an on-disk LRU cache, templates/decks persist in a single SQLite database, assets enforce upload limits, and PDF exports prune intermediates by default.
* Optional OCR/inpainting lives behind the `ENABLE_OCR` flag so heavy dependencies can ship in a sidecar image.
* Tests located at `tests/backend` using `pytest` (see `tests/backend/test_app.py` for API smoke coverage).

### Environment flags

| Variable | Default | Description |
| --- | --- | --- |
| `ENABLE_OCR` | `0` | Toggle OCR/inpainting integration points (heavy deps stay external when `0`). |
| `PREVIEW_CACHE_MB` | `200` | Disk budget for preview cache (automatic LRU eviction + TTL). |
| `PREVIEW_TTL_SEC` | `3600` | Expiration window for cached previews. |
| `KEEP_INTERMEDIATES` | `0` | Retain previous PDF renders when `1`; otherwise pruned automatically. |
| `MAX_UPLOAD_MB` | `30` | Hard limit for uploaded asset payloads. |

### Running locally

```bash
pip install -e .
uvicorn app.backend.main:app --reload
```

The FastAPI docs (including blueprint and cleaning endpoints) are available at `http://localhost:8000/docs`.

## Frontend

* React application under `app/frontend` using Vite + TypeScript.
* State management via Redux Toolkit and Zustand with Konva-powered preview components.
* Tests written with Vitest and Testing Library.

### Running locally

```bash
cd app/frontend
npm install
npm run dev
```

## Tooling

* Multi-stage Dockerfiles for backend (`Dockerfile.backend`) and frontend (`Dockerfile.frontend`) that keep runtime layers minimal by copying only compiled artifacts.
* `docker-compose.yml` to run both services together with optional OCR sidecar toggled by environment variables.
* GitHub Actions workflow for linting, testing, and building both projects, including a guard that fails when the backend image exceeds the target footprint.

## Testing

```bash
pytest tests/backend
cd app/frontend && npm run test
```
