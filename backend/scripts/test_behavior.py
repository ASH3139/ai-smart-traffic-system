from backend.app.services.behavior.service import BehaviorService
from backend.app.services.tracking.models import Track


def main():

    behavior = BehaviorService(
        stop_line_y=300,
        counting_line_y=220,
    )

    track = Track(
        track_id=1,
        class_id=2,
        class_name="car",
        confidence=0.95,
        x1=100,
        y1=150,
        x2=180,
        y2=210,
    )

    print("Frame 1")
    print(behavior.update(track))

    track.y1 += 40
    track.y2 += 40

    print("Frame 2")
    print(behavior.update(track))

    track.y1 += 60
    track.y2 += 60

    print("Frame 3")
    print(behavior.update(track))

    track.y1 += 120
    track.y2 += 120

    print("Frame 4")
    print(behavior.update(track))


if __name__ == "__main__":
    main()
