import cv2


from backend.app.services.video_ingestion.service import VideoService
from backend.app.services.tracking.service import TrackingService
from backend.app.services.speed.config import SpeedConfig
from backend.app.services.speed.optical_flow import OpticalFlow
from backend.app.services.speed.service import SpeedService
from backend.app.services.analytics.service import AnalyticsService
from backend.app.services.lane.service import LaneService
from backend.app.services.roi.service import ROIService
from backend.app.services.stop_line.service import StopLineService
from backend.app.services.counting_line.service import CountingLineService
from backend.app.services.behavior.service import BehaviorService


def main():

    # -----------------------------
    # Initialize Services
    # -----------------------------

    video = VideoService()
    video.start()

    tracker = TrackingService()

    speed_config = SpeedConfig()

    optical_flow = OpticalFlow(speed_config.optical_flow)

    speed_service = SpeedService(speed_config)

    analytics = AnalyticsService()
    lane_service = LaneService()
    roi_service = ROIService()
    stop_line_service = StopLineService()
    counting_line_service = CountingLineService()

    behavior = BehaviorService(
        stop_line_y=stop_line_service.stop_line.start[1],
        counting_line_y=counting_line_service.counting_line.start[1],
    )

    print("=" * 60)
    print("Traffic Analytics Started")
    print("=" * 60)

    # -----------------------------
    # Main Loop
    # -----------------------------

    while True:

        frame = video.get_frame()

        image = frame.image.copy()
        # -----------------------------
        # Spatial Layer
        # -----------------------------

        roi_service.draw(image)
        stop_line_service.draw(image)
        counting_line_service.draw(image)

        # -----------------------------
        # Tracking
        # -----------------------------

        tracks = tracker.track(image)
        for track in tracks:
            lane_service.assign_lane(track)

        # -----------------------------
        # Optical Flow
        # -----------------------------

        flow = optical_flow.compute(image)

        # -----------------------------
        # Speed
        # -----------------------------

        speeds = speed_service.calculate(
            flow,
            tracks,
        )

        # -----------------------------
        # Analytics
        # -----------------------------

        statistics = analytics.process(
            frame,
            tracks,
            speeds,
        )

        # -----------------------------
        # Draw Tracks
        # -----------------------------

        speed_lookup = {speed.track_id: speed for speed in speeds}

        for track in tracks:
            events = behavior.update(track)
            if events["counting_line_crossed"]:
                print(f"Track {track.track_id} crossed Counting Line")

            if events["stop_line_crossed"]:
                print(f"Track {track.track_id} crossed Stop Line")

            cv2.rectangle(
                image,
                (track.x1, track.y1),
                (track.x2, track.y2),
                (0, 255, 0),
                2,
            )

        vehicle_speed = 0.0
        if track.track_id in speed_lookup:
            vehicle_speed = speed_lookup[track.track_id].speed_kmh

        label = (
            f"ID:{track.track_id} " f"L:{track.lane_id} " f"{vehicle_speed:.1f} km/h"
        )

        cv2.putText(
            image,
            label,
            (track.x1, track.y1 - 8),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 255, 0),
            2,
        )

        # -----------------------------
        # Analytics Dashboard
        # -----------------------------

        cv2.putText(
            image,
            f"Current Vehicles : {statistics.current_vehicle_count}",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (0, 255, 255),
            2,
        )

        cv2.putText(
            image,
            f"Total Vehicles : {statistics.total_vehicle_count}",
            (20, 65),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (0, 255, 255),
            2,
        )

        cv2.putText(
            image,
            f"Average Speed : {statistics.average_speed:.1f} km/h",
            (20, 95),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (0, 255, 255),
            2,
        )
        cv2.putText(
            image,
            f"Traffic Density : {statistics.density:.2f}",
            (20, 125),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (0, 255, 255),
            2,
        )
        cv2.putText(
            image,
            f"Queue Length : {statistics.queue_length}",
            (20, 155),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (0, 255, 255),
            2,
        )
        cv2.putText(
            image,
            f"Waiting Vehicles : {statistics.waiting_vehicles}",
            (20, 185),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (0, 255, 255),
            2,
        )

        cv2.putText(
            image,
            f"Avg Waiting : {statistics.average_waiting_time:.1f}s",
            (20, 215),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (0, 255, 255),
            2,
        )

        cv2.putText(
            image,
            f"Max Waiting : {statistics.maximum_waiting_time:.1f}s",
            (20, 245),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (0, 255, 255),
            2,
        )
        cv2.putText(
            image,
            f"PCU : {statistics.pcu:.1f}",
            (20, 275),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (0, 255, 255),
            2,
        )
        cv2.putText(
            image,
            f"Vehicles Passed (1 min): {statistics.vehicles_passed_last_minute}",
            (20, 305),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (0, 255, 255),
            2,
        )

        cv2.putText(
            image,
            f"Traffic Flow : {statistics.traffic_flow:.0f} veh/hr",
            (20, 335),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (0, 255, 255),
            2,
        )
        cv2.imshow(
            "Traffic Analytics",
            image,
        )

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    video.stop()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
