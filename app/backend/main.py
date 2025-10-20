from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI

from . import context
from .routers import ai, assets, auth, clean, decks, render, templates


def create_app() -> FastAPI:
    app = FastAPI(title="PPT Generator API", version="0.2.0")
    app.state.ctx = context.build_context(Path.cwd())

    app.include_router(auth.router, prefix="/auth", tags=["auth"])
    app.include_router(templates.router, prefix="/templates", tags=["templates"])
    app.include_router(clean.router, prefix="/clean", tags=["clean"])
    app.include_router(ai.router, prefix="/ai", tags=["ai"])
    app.include_router(decks.router, prefix="/decks", tags=["decks"])
    app.include_router(render.router, prefix="/render", tags=["render"])
    app.include_router(assets.router, prefix="/assets", tags=["assets"])

    @app.get("/healthz", tags=["health"])
    async def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
