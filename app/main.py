"""FastAPI surface: GET /digest returns the ranked digest + draft email."""
from __future__ import annotations

from fastapi import FastAPI

from .config import settings
from .engine import build_digest

app = FastAPI(title="Origination Signal Engine", version="1.0.0")


@app.get("/digest")
async def digest() -> dict:
    return build_digest(settings.targets_csv)


@app.get("/healthz")
async def healthz() -> dict:
    return {"status": "ok"}
