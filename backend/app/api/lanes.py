from fastapi import APIRouter, Depends

from backend.app.dependencies.system import get_system
from backend.app.services.system.service import TrafficSystemService
from backend.app.schemas.lane import LaneResponse

router = APIRouter(
    tags=["Analytics"],
)


@router.get(
    "/lanes",
    summary="Get lane-wise traffic analytics",
    response_model=list[LaneResponse],
)
def lanes(
    system: TrafficSystemService = Depends(get_system),
):
    """
    Returns lane-wise traffic analytics.
    """

    result = system.get_latest_result()

    if result is None:
        return []

    response = []

    for lane in result.lane_statistics:

        response.append(
            LaneResponse(
                lane_id=lane.lane_id,
                vehicle_count=lane.vehicle_count,
                average_speed=lane.average_speed,
                density=lane.density,
                queue_length=lane.queue_length,
                traffic_flow=lane.traffic_flow,
            )
        )

    return response
