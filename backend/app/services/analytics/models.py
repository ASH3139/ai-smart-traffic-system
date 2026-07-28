from dataclasses import dataclass


@dataclass(slots=True)
class TrafficStatistics:

    current_vehicle_count: int = 0
    total_vehicle_count: int = 0

    average_speed: float = 0.0

    density: float = 0.0

    queue_length: int = 0

    waiting_vehicles: int = 0

    pcu: float = 0.0

    traffic_flow: float = 0.0