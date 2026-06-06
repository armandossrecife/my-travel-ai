"""Travel plan result route."""

from fastapi import APIRouter

from app.services.planning_jobs import get_result

router = APIRouter()


@router.get("/api/result/{request_id}")
async def get_travel_plan_result(request_id: str):
    """Return the travel plan result after completion."""
    result = get_result(request_id)
    if result is None:
        return {"status": "processing"}
    return result

