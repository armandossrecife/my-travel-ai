"""Health check route."""

import os

from fastapi import APIRouter

from app.agents.logger import event_logger

router = APIRouter()


@router.get("/api/health")
async def health_check():
    """Check whether the API is operational."""
    return {
        "status": "ok",
        "service": "Travel Planner Multiagent API",
        "version": "1.0.0",
        "llm_enabled": bool(os.environ.get("GEMINI_API_KEY")),
        "active_logs": len(event_logger._queues),
    }

