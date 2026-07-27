import cv2

from backend.app.services.video_ingestion.frame_reader import FrameReader
from backend.app.services.tracking.service import TrackingService

from backend.app.services.speed.config import SpeedConfig
from backend.app.services.speed.optical_flow import OpticalFlow
from backend.app.services.speed.service import SpeedService


def main():

    # -------------------------
    # Initialize
    # -------------------------

    reader = FrameReader()
    reader.open()

    tracker = TrackingService()

    speed_config = SpeedConfig()

    optical_flow = OpticalFlow(
        speed_config.optical_flow
    )

    speed_service = SpeedService(
        speed_config
    )

    print(f"Video FPS : {reader.fps:.2f}")

    # -------------------------
    # Main Loop
    # -------------------------

    while True:

        frame = reader.read()

        tracks = tracker.track(frame.image)

        flow = optical_flow.compute(
            frame.image
        )

        speeds = speed_service.calculate(
            flow,
            tracks
        )

        image = frame.image.copy()

        # Speed lookup dictionary
        speed_lookup = {
            speed.track_id: speed
            for speed in speeds
        }

        for track in tracks:

            # Bounding box
            cv2.rectangle(
                image,
                (track.x1, track.y1),
                (track.x2, track.y2),
                (0, 255, 0),
                2,
            )

            # Label
            if track.track_id in speed_lookup:

                vehicle_speed = speed_lookup[
                    track.track_id
                ]

                label = (
                    f"{track.class_name} "
                    f"ID:{track.track_id} "
                    f"{vehicle_speed.speed_kmh:.1f} km/h"
                )

            else:

                label = (
                    f"{track.class_name} "
                    f"ID:{track.track_id}"
                )

            cv2.putText(
                image,
                label,
                (track.x1, track.y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2,
            )

        cv2.imshow(
            "Vehicle Speed Estimation",
            image,
        )

        # Play video using original FPS
        delay = max(1, int(1000 / reader.fps))

        key = cv2.waitKey(delay) & 0xFF

        if key == ord("q"):
            break

    # -------------------------
    # Cleanup
    # -------------------------

    reader.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()