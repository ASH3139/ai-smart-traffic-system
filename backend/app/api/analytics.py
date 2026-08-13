from fastapi import APIRouter, Depends

from backend.app.dependencies.system import get_system
from backend.app.services.system.service import TrafficSystemService

router = APIRouter()


@router.get("/analytics")
def analytics(
    system: TrafficSystemService = Depends(get_system),
):
    """
    Returns the latest traffic analytics.
    """

    result = system.get_latest_result()

    if result is None:
        return {"message": "Traffic system is starting..."}

    statistics = result.statistics

    return {
        "current_vehicle_count": statistics.current_vehicle_count,
        "total_vehicle_count": statistics.total_vehicle_count,
        "average_speed": statistics.average_speed,
        "density": statistics.density,
        "queue_length": statistics.queue_length,
        "waiting_vehicles": statistics.waiting_vehicles,
        "average_waiting_time": statistics.average_waiting_time,
        "maximum_waiting_time": statistics.maximum_waiting_time,
        "pcu": statistics.pcu,
        "traffic_flow": statistics.traffic_flow,
        "vehicles_passed_last_minute": statistics.vehicles_passed_last_minute,
    }
