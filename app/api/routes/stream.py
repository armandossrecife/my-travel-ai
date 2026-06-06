"""Server-sent events route for travel plan progress logs."""

import asyncio
import json

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from app.agents.logger import event_logger
from app.services.planning_jobs import get_result

router = APIRouter()


@router.get("/api/stream/{request_id}")
async def stream_logs(request_id: str, request: Request):
    """Stream processing events for a request_id using SSE."""
    q = event_logger.get_queue(request_id)
    if not q:
        return {"error": "request_id não encontrado ou já finalizado."}

    async def event_generator():
        while True:
            if await request.is_disconnected():
                break

            try:
                if not q.empty():
                    event = q.get_nowait()
                    data = event.to_dict()
                    yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
                else:
                    result = get_result(request_id)
                    if result is not None:
                        data = {"event": "done", "result": result}
                        yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
                        break
                    await asyncio.sleep(0.5)
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

