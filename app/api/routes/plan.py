"""Travel plan creation route."""

import threading
import uuid

from fastapi import APIRouter, HTTPException

from app.agents.logger import event_logger
from app.api.schemas import PlanRequest
from app.models import TravelPreferences, TravelRequest
from app.services.planning_jobs import run_maestro_background

router = APIRouter()

@router.post("/api/plan")
async def generate_travel_plan(request: PlanRequest):
    """
    Start travel plan generation.

    Returns a request_id so the client can follow progress through SSE.
    """
    try:
        request_id = str(uuid.uuid4())
        event_logger.create_queue(request_id)

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