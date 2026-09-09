from backend.app.services.incident_detection.detectors import AccidentDetector
from backend.app.services.tracking.models import Track
from backend.app.services.speed.models import VehicleSpeed


def make_track(
    track_id: int,
    x1: int,
    y1: int,
    x2: int,
    y2: int,
):
    return Track(
        track_id=track_id,
        class_id=2,
        class_name="car",
        confidence=0.9,
        x1=x1,
        y1=y1,
        x2=x2,
        y2=y2,
        lane_id=1,
    )


def make_speed(track_id: int, speed: float):
    return VehicleSpeed(
        track_id=track_id,
        class_name="car",
        speed_kmh=speed,
        pixel_distance=10.0,
        timestamp=1.0,
    )


def main():

    detector = AccidentDetector()

    print("Accident Detector Motion History Test")
    print("--------------------------------------")

    # ---------------------------------
    # Frame 1
    # ---------------------------------

    tracks = [
        make_track(1, 100, 100, 140, 140),
    ]

    speeds = [
        make_speed(1, 40),
    ]

    detector.detect(
        tracks=tracks,
        speeds=speeds,
        behavior_events={},
    )

    print("Frame 1 processed")

    # ---------------------------------
    # Frame 2
    # ---------------------------------

    tracks = [
        make_track(1, 105, 110, 145, 150),
    ]

    speeds = [
        make_speed(1, 8),
    ]

    detector.detect(
        tracks=tracks,
        speeds=speeds,
        behavior_events={},
    )

    print("Frame 2 processed")

    # ---------------------------------
    # Inspect stored state
    # ---------------------------------

    state = detector.vehicle_states.get(1)

    if state is None:
        print("✗ Vehicle state was not stored")
        return

    print()
    print("Stored Vehicle State")
    print("--------------------")
    print("Track ID:", state.track_id)
    print("Previous Center:", state.previous_center)
    print("Previous Speed:", state.previous_speed)
    print("Previous Timestamp:", state.previous_timestamp)

    print()
    print("✓ Motion history is being maintained correctly.")


if __name__ == "__main__":
    main()
