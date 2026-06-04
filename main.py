"""
main.py — Ponto de entrada da aplicação FastAPI.

Expõe os endpoints da API REST e serve a interface web estática.
"""

import os
import sys
import threading
import uuid
from datetime import datetime
from queue import Queue

# Garante que os módulos do projeto sejam encontrados
sys.path.insert(0, os.path.dirname(__file__))

from datetime import date
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from agents import maestro
from agents.logger import event_logger
from models import TravelPlan, TravelPreferences, TravelRequest

# ──────────────────────────────────────────────────────────────
# Modelos de entrada da API (compatíveis com formulário web)
# ──────────────────────────────────────────────────────────────


class PlanRequest(BaseModel):
    cidade_destino: str = Field(..., description="Cidade de destino")
    data_saida: date = Field(..., description="Data de início (YYYY-MM-DD)")
    data_retorno: date = Field(..., description="Data de retorno (YYYY-MM-DD)")
    cidade_origem: Optional[str] = Field(
        default=None, description="Cidade de origem (opcional)"
    )
    quantidade_viajantes: int = Field(
        default=1, ge=1, description="Número de viajantes"
    )
    preferencia_voo: str = Field(default="melhor_custo_beneficio")
    preferencia_hotel: str = Field(default="melhor_custo_beneficio")
    categoria_hotel: Optional[str] = Field(default=None)
    ritmo_roteiro: str = Field(default="moderado")
    interesses: List[str] = Field(default_factory=list)


# ──────────────────────────────────────────────────────────────
# Armazenamento de resultados (thread-safe)
# ──────────────────────────────────────────────────────────────
results_lock = threading.Lock()
results_store: Dict[str, Any] = {}


def run_maestro_background(request_id: str, travel_req: TravelRequest):
    """Executa o maestro em thread separada e armazena o resultado."""
    try:
        plano = maestro.run(travel_req, request_id=request_id)
        with results_lock:
            results_store[request_id] = plano.model_dump()
        # Sinaliza fim da execução
        event_logger.log(request_id, "system", "success", "PROCESSAMENTO_CONCLUIDO")
    except Exception as e:
        with results_lock:
            results_store[request_id] = {"error": str(e)}
        event_logger.log(request_id, "system", "error", f"ERRO: {str(e)}")
    finally:
        # Aguarda um pouco antes de limpar a fila para o SSE receber os últimos eventos
        import time

        time.sleep(10)  # Tempo suficiente para o SSE receber os eventos
        event_logger.remove_queue(request_id)


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
        "active_logs": len(event_logger._queues),
    }


@app.post("/api/plan")
async def generate_travel_plan(request: PlanRequest):
    """
    Gera um plano de viagem integrado.

    Aciona os agentes maestro, agente_aereo, agente_hotel e agente_turismo em paralelo
    e retorna um request_id para acompanhar o progresso via SSE.
    """
    try:
        # Gera um request_id único
        request_id = str(uuid.uuid4())

        # Cria uma fila para este request_id
        event_logger.create_queue(request_id)

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

        # Inicia o processamento em thread separada
        thread = threading.Thread(
            target=run_maestro_background, args=(request_id, travel_req)
        )
        thread.start()

        return {
            "request_id": request_id,
            "status": "processing",
            "message": "Processamento iniciado. Use GET /api/stream/"
            + request_id
            + " para acompanhar.",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stream/{request_id}")
async def stream_logs(request_id: str, request: Request):
    """
    Endpoint SSE para streaming de logs em tempo real.
    """
    q = event_logger.get_queue(request_id)
    if not q:
        return {"error": "request_id não encontrado ou já finalizado."}

    async def event_generator():
        while True:
            # Verifica se o cliente desconectou
            if await request.is_disconnected():
                break

            try:
                # Non-blocking get
                if not q.empty():
                    event = q.get_nowait()
                    data = event.to_dict()
                    yield f"data: {__import__('json').dumps(data, ensure_ascii=False)}\n\n"
                else:
                    # Se o resultado já estiver disponível, envia evento de conclusão
                    with results_lock:
                        result = results_store.get(request_id)
                    if result is not None:
                        yield f"data: {__import__('json').dumps({'event': 'done', 'result': result}, ensure_ascii=False)}\n\n"
                        break
                    await __import__("asyncio").sleep(0.5)
            except Exception:
                break

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@app.get("/api/result/{request_id}")
async def get_result(request_id: str):
    """
    Retorna o resultado do processamento após conclusão.
    """
    with results_lock:
        result = results_store.get(request_id)
    if result is None:
        return {"status": "processing"}
    return result


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
