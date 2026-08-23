from fastapi import APIRouter, Depends

from backend.app.dependencies.system import get_system
from backend.app.services.system.service import TrafficSystemService

router = APIRouter(
    tags=["System Status"],
)


@router.get(
    "/status",
    summary="Get traffic system status",
)
def status(
    system: TrafficSystemService = Depends(get_system),
):
    """
    Returns the current processing status.
    """

    if system.running:

        if system.get_latest_image() is not None:
            state = "RUNNING"
        else:
            state = "STARTING"

    else:
        state = "STOPPED"

    return {
        "state": state,
        "running": system.running,
        "frame_available": (system.get_latest_image() is not None),
    }
