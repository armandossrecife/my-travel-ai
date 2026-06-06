"""Application factory for the TravelAI FastAPI app."""

from fastapi import FastAPI

from app.api.routes import health, plan, result, stream
from app.ui.static import mount_static_ui


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    api_app = FastAPI(
        title="🌍 Agente de Planejamento de Viagens",
        description="API multiagente para geração de planos de viagem integrados: voos, hotéis e roteiro turístico.",
        version="1.2.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    api_app.include_router(health.router)
    api_app.include_router(plan.router)
    api_app.include_router(stream.router)
    api_app.include_router(result.router)
    mount_static_ui(api_app)

    return api_app


app = create_app()

