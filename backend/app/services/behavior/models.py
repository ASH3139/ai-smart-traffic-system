from dataclasses import dataclass


@dataclass(slots=True)
class VehicleState:

    track_id: int

    previous_center: tuple[int, int]

    crossed_stop_line: bool = False

    crossed_counting_line: bool = False
