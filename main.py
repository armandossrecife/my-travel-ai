"""
main.py — Ponto de entrada da aplicação FastAPI.

Expõe os endpoints da API REST e serve a interface web estática.
"""
import sys
import os

# Garante que os módulos do projeto sejam encontrados
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List

from models import TravelRequest, TravelPreferences, TravelPlan
from agents import maestro


# ──────────────────────────────────────────────────────────────
# Modelos de entrada da API (compatíveis com formulário web)
# ──────────────────────────────────────────────────────────────

class PlanRequest(BaseModel):
    cidade_destino: str = Field(..., description="Cidade de destino")
    data_saida: date = Field(..., description="Data de início (YYYY-MM-DD)")
    data_retorno: date = Field(..., description="Data de retorno (YYYY-MM-DD)")
    cidade_origem: Optional[str] = Field(default=None, description="Cidade de origem (opcional)")
    quantidade_viajantes: int = Field(default=1, ge=1, description="Número de viajantes")
    preferencia_voo: str = Field(default="melhor_custo_beneficio")
    preferencia_hotel: str = Field(default="melhor_custo_beneficio")
    categoria_hotel: Optional[str] = Field(default=None)
    ritmo_roteiro: str = Field(default="moderado")
    interesses: List[str] = Field(default_factory=list)


# ──────────────────────────────────────────────────────────────
# Aplicação FastAPI
# ──────────────────────────────────────────────────────────────

app = FastAPI(
    title="🌍 Agente de Planejamento de Viagens",
    description="API multiagente para geração de planos de viagem integrados: voos, hotéis e roteiro turístico.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.get("/api/health")
async def health_check():
    """Verifica se a API está operacional."""
    return {
        "status": "ok",
        "service": "Travel Planner Multiagent API",
        "version": "1.0.0",
        "llm_enabled": bool(os.environ.get("GEMINI_API_KEY")),
    }


@app.post("/api/plan", response_model=None)
async def generate_travel_plan(request: PlanRequest):
    """
    Gera um plano de viagem integrado.
    
    Aciona os agentes maestro, agente_aereo, agente_hotel e agente_turismo em paralelo
    e retorna um plano consolidado com passagens, hotéis e roteiro turístico.
    """
    try:
        # Constrói TravelRequest a partir do PlanRequest da API
        travel_req = TravelRequest(
            cidade_destino=request.cidade_destino,
            data_saida=request.data_saida,
            data_retorno=request.data_retorno,
            cidade_origem=request.cidade_origem,
            preferencias=TravelPreferences(
                quantidade_viajantes=request.quantidade_viajantes,
                quantidade_hospedes=request.quantidade_viajantes,
                quantidade_quartos=max(1, request.quantidade_viajantes // 2),
                preferencia_voo=request.preferencia_voo,
                preferencia_hotel=request.preferencia_hotel,
                categoria_hotel=request.categoria_hotel,
                ritmo_roteiro=request.ritmo_roteiro,
                interesses=request.interesses,
            ),
        )

        plano = maestro.run(travel_req)

        if plano.status == "erro":
            raise HTTPException(status_code=422, detail={
                "message": "Não foi possível processar a solicitação.",
                "erros": plano.alertas,
            })

        return plano.model_dump()

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ──────────────────────────────────────────────────────────────
# Servir interface web
# ──────────────────────────────────────────────────────────────

static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    @app.get("/")
    async def serve_frontend():
        """Serve a interface web principal."""
        return FileResponse(os.path.join(static_dir, "index.html"))
