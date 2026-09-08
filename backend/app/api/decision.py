from fastapi import APIRouter, Depends
from backend.app.dependencies.system import get_system
from backend.app.services.system.service import TrafficSystemService
from backend.app.schemas.decision import DecisionResponse
from backend.app.dependencies.auth import require_admin
from backend.app.database.tables.user import User

router = APIRouter(
    tags=["AI Decision"],
)


@router.get(
    "/decision",
    summary="Get the latest AI traffic decision",
    response_model=DecisionResponse,
)
def decision(
    system: TrafficSystemService = Depends(get_system),
    current_user: User = Depends(require_admin),
):

    latest = system.decision.last_decision

    if latest is None:

        return {"message": "No decision available yet"}

    return DecisionResponse(
        selected_lane=latest.selected_lane,
        green_time=latest.green_time,
        reason=latest.reason,
    )
