"""Background execution and in-memory result storage for travel plans."""

import threading
import time
from typing import Any, Dict

from app.agents import maestro
from app.agents.logger import event_logger
from app.models import TravelRequest

results_lock = threading.Lock()
results_store: Dict[str, Any] = {}


def run_maestro_background(request_id: str, travel_req: TravelRequest):
    """Run maestro in a background thread and store the serialized result."""
    try:
        plano = maestro.run(travel_req, request_id=request_id)
        with results_lock:
            results_store[request_id] = plano.model_dump()
        event_logger.log(request_id, "system", "success", "PROCESSAMENTO_CONCLUIDO")
    except Exception as e:
        with results_lock:
            results_store[request_id] = {"error": str(e)}
        event_logger.log(request_id, "system", "error", f"ERRO: {str(e)}")
    finally:
        # Keep the queue briefly available so SSE clients can receive final events.
        time.sleep(10)
        event_logger.remove_queue(request_id)


def get_result(request_id: str):
    """Return a stored result, or None while it is still processing."""
    with results_lock:
        return results_store.get(request_id)

