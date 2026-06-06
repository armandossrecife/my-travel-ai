"""Static UI mounting for the TravelAI frontend."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


def mount_static_ui(app: FastAPI):
    """Mount the existing static frontend without changing public URLs."""
    static_dir = Path(__file__).resolve().parents[2] / "static"
    if not static_dir.exists():
        return

    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    @app.get("/")
    async def serve_frontend():
        """Serve the main web interface."""
        return FileResponse(static_dir / "index.html")

