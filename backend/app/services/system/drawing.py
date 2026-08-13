import cv2


class SystemDrawer:
    """
    Draws every visual element of the traffic system.
    """

    def draw(
        self,
        image,
        result,
        system,
    ):
        self._draw_spatial(
            image,
            system,
        )

        self._draw_tracks(
            image,
            result,
        )

        self._draw_global_dashboard(
            image,
            result,
        )

        self._draw_lane_dashboard(
            image,
            result,
        )

        self._draw_signal(
            image,
            result,
        )
        return image

    def _draw_spatial(
        self,
        image,
        system,
    ):
        """
        Draw ROI, stop line and counting line.
        """

        system.roi.draw(image)

        system.stop_line.draw(image)

        system.counting_line.draw(image)

    def _draw_tracks(
        self,
        image,
        result,
    ):
        """
        Draw tracked vehicles with speed labels.
        """

        speed_lookup = {speed.track_id: speed for speed in result.speeds}

        for track in result.tracks:

            events = result.behavior_events.get(
                track.track_id,
                {},
            )

            if events.get("counting_line_crossed"):

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
                f"ID:{track.track_id} "
                f"L:{track.lane_id} "
                f"{vehicle_speed:.1f} km/h"
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

    def _draw_global_dashboard(
        self,
        image,
        result,
    ):
        """
        Draw overall traffic analytics.
        """

        statistics = result.statistics

        dashboard_color = (0, 255, 255)
        heading_color = (0, 255, 0)
        font = cv2.FONT_HERSHEY_SIMPLEX

        y = 30

        cv2.putText(
            image,
            "GLOBAL ANALYTICS",
            (20, y),
            font,
            0.8,
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
            f"Avg Waiting      : {statistics.average_waiting_time:.1f}s",
            f"Max Waiting      : {statistics.maximum_waiting_time:.1f}s",
            f"PCU              : {statistics.pcu:.1f}",
            f"Traffic Flow     : {statistics.traffic_flow:.0f} veh/hr",
        ]

        for text in dashboard:

            cv2.putText(
                image,
                text,
                (20, y),
                font,
                0.60,
                dashboard_color,
                2,
            )

            y += 28

    def _draw_lane_dashboard(
        self,
        image,
        result,
    ):
        """
        Draw lane-wise analytics.
        """

        dashboard_color = (0, 255, 255)
        lane_heading_color = (255, 200, 0)
        font = cv2.FONT_HERSHEY_SIMPLEX

        y = 365

        cv2.putText(
            image,
            "LANE ANALYTICS",
            (20, y),
            font,
            0.8,
            lane_heading_color,
            2,
        )

        y += 35

        for lane in result.lane_statistics:

            cv2.putText(
                image,
                f"Lane {lane.lane_id}",
                (20, y),
                font,
                0.65,
                (255, 255, 255),
                2,
            )

            y += 25

            items = [
                f"Vehicles : {lane.vehicle_count}",
                f"Avg Speed : {lane.average_speed:.1f} km/h",
                f"Density : {lane.density:.2f}",
                f"Queue : {lane.queue_length}",
                f"Flow : {lane.traffic_flow:.0f} veh/hr",
            ]

            for item in items:

                cv2.putText(
                    image,
                    item,
                    (40, y),
                    font,
                    0.55,
                    dashboard_color,
                    2,
                )

                y += 23

            y += 12

    def _draw_signal(
        self,
        image,
        result,
    ):
        """
        Draw current traffic signal information.
        """

        signal = result.signal

        dashboard_color = (0, 255, 255)
        heading_color = (0, 255, 0)
        font = cv2.FONT_HERSHEY_SIMPLEX

        x = 700
        y = 30

        cv2.putText(
            image,
            "TRAFFIC SIGNAL",
            (x, y),
            font,
            0.8,
            heading_color,
            2,
        )

        y += 35

        items = [
            f"Green Lane : {signal.current_green_lane}",
            f"State : {signal.state.value}",
            f"Remaining : {signal.remaining_time}s",
            f"Green Time : {signal.green_time}s",
            f"Reason : {signal.last_reason}",
        ]

        for item in items:

            cv2.putText(
                image,
                item,
                (x, y),
                font,
                0.60,
                dashboard_color,
                2,
            )

            y += 28

    # ---------------------------------
