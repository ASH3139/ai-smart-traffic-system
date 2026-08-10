import cv2


from backend.app.services.lane.service import LaneService
from backend.app.services.roi.service import ROIService
from backend.app.services.stop_line.service import StopLineService
from backend.app.services.counting_line.service import CountingLineService

from backend.app.services.traffic_signal.models import SignalState

from backend.app.services.behavior.service import BehaviorService
from backend.app.services.system.service import TrafficSystemService


def draw_tracks(
    image,
    tracks,
    speed_lookup,
    behavior_events,
):

    for track in tracks:

        events = behavior_events.get(track.track_id, {})

        if events.get("counting_line_crossed"):
            print(f"Track {track.track_id} crossed Counting Line")

        if events.get("stop_line_crossed"):
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


def main():

    # ---------------------------------
    # Initialize Services
    # ---------------------------------

    system = TrafficSystemService()
    system.start()

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

    # ---------------------------------
    # Main Loop
    # ---------------------------------

    while True:

        result = system.process_frame()

        frame = result.frame
        image = result.image
        tracks = result.tracks
        speeds = result.speeds
        statistics = result.statistics
        lane_statistics = result.lane_statistics
        behavior_events = result.behavior_events
        signal = result.signal

        # ---------------------------------
        # Spatial Layer
        # ---------------------------------

        roi_service.draw(image)

        stop_line_service.draw(image)

        counting_line_service.draw(image)

        speed_lookup = {speed.track_id: speed for speed in speeds}

        # ---------------------------------
        # Draw Tracks
        # ---------------------------------

        draw_tracks(
            image,
            tracks,
            speed_lookup,
            behavior_events,
        )
        # ---------------------------------
        # Global Analytics Dashboard
        # ---------------------------------

        dashboard_color = (0, 255, 255)
        heading_color = (0, 255, 0)
        lane_heading_color = (255, 200, 0)
        font = cv2.FONT_HERSHEY_SIMPLEX

        x = 20
        y = 30

        cv2.putText(
            image,
            "GLOBAL ANALYTICS",
            (x, y),
            font,
            0.75,
            heading_color,
            2,
        )

        y += 35

        dashboard = [
            f"Current Vehicles : {statistics.current_vehicle_count}",
            f"Total Vehicles   : {statistics.total_vehicle_count}",
            f"Average Speed    : {statistics.average_speed:.1f} km/h",
            f"Density          : {statistics.density:.2f}",
            f"Queue Length     : {statistics.queue_length}",
            f"Waiting Vehicles : {statistics.waiting_vehicles}",
            f"Traffic Flow     : {statistics.traffic_flow:.0f} veh/hr",
        ]

        for text in dashboard:

            cv2.putText(
                image,
                text,
                (x, y),
                font,
                0.58,
                dashboard_color,
                2,
            )

            y += 26

        # ---------------------------------
        # Lane Analytics Dashboard
        # ---------------------------------

        y += 15

        cv2.putText(
            image,
            "LANE ANALYTICS",
            (x, y),
            font,
            0.75,
            lane_heading_color,
            2,
        )

        y += 32

        for lane in lane_statistics:

            lane_text = (
                f"Lane {lane.lane_id} | "
                f"V:{lane.vehicle_count}  "
                f"S:{lane.average_speed:.1f}  "
                f"Q:{lane.queue_length}"
            )

            cv2.putText(
                image,
                lane_text,
                (x, y),
                font,
                0.56,
                (255, 255, 255),
                2,
            )

            y += 25

        # ---------------------------------
        # Display
        # ---------------------------------

        cv2.imshow(
            "Traffic Analytics",
            image,
        )

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

        cv2.putText(
            image,
            "AI DECISION",
            (20, y),
            font,
            0.75,
            (0, 255, 0),
            2,
        )

    y += 30

    cv2.putText(
        image,
        f"Green Lane : {signal.selected_lane}",
        (20, y),
        font,
        0.58,
        dashboard_color,
        2,
    )

    y += 25

    cv2.putText(
        image,
        f"Green Time : {signal.green_time} sec",
        (20, y),
        font,
        0.58,
        dashboard_color,
        2,
    )

    y += 25

    cv2.putText(
        image,
        f"Reason : {signal.reason}",
        (20, y),
        font,
        0.58,
        dashboard_color,
        2,
    )
    y += 40

    cv2.putText(
        image,
        "TRAFFIC SIGNAL",
        (20, y),
        font,
        0.75,
        (255, 200, 0),
        2,
    )

    y += 30

    for lane in range(1, 4):

        color = "RED"

    if lane == signal.current_green_lane and signal.state == SignalState.GREEN:
        color = "GREEN"

    elif lane == signal.current_green_lane and signal.state == SignalState.YELLOW:
        color = "YELLOW"

    cv2.putText(
        image,
        f"Lane {lane} : {color}",
        (20, y),
        font,
        0.58,
        dashboard_color,
        2,
    )

    y += 25

    cv2.putText(
        image,
        f"Remaining : {signal.remaining_time}s",
        (20, y),
        font,
        0.58,
        dashboard_color,
        2,
    )

    # ---------------------------------
    # Cleanup
    # ---------------------------------

    system.stop()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
