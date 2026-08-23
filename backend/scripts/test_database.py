from backend.app.database.session_manager import get_db_session
from backend.app.services.persistence.service import PersistenceService

from backend.app.services.analytics.models import TrafficStatistics
from backend.app.services.lane_analytics.models import LaneStatistics
from backend.app.services.tracking.models import Track
from backend.app.services.decision_engine.models import Decision


def main():

    persistence = PersistenceService()

    with get_db_session() as session:

        # --------------------------------
        # Traffic Analytics
        # --------------------------------

        statistics = TrafficStatistics(
            current_vehicle_count=10,
            total_vehicle_count=25,
            average_speed=42.5,
            density=0.35,
            queue_length=4,
            waiting_vehicles=2,
            average_waiting_time=8.5,
            maximum_waiting_time=15.0,
            pcu=11.2,
            traffic_flow=25.0,
        )

        persistence.save_traffic_statistics(
            session,
            statistics,
        )

        # --------------------------------
        # Lane Analytics
        # --------------------------------

        lane_statistics = [
            LaneStatistics(
                lane_id=1,
                vehicle_count=6,
                average_speed=40.0,
                density=0.30,
                queue_length=2,
                traffic_flow=15.0,
            ),
            LaneStatistics(
                lane_id=2,
                vehicle_count=4,
                average_speed=35.0,
                density=0.25,
                queue_length=3,
                traffic_flow=10.0,
            ),
        ]

        persistence.save_lane_statistics(
            session,
            lane_statistics,
        )

        # --------------------------------
        # Vehicle Event
        # --------------------------------

        track = Track(
            track_id=101,
            class_id=2,
            class_name="car",
            confidence=0.92,
            x1=100,
            y1=100,
            x2=200,
            y2=200,
            lane_id=1,
        )

        persistence.save_vehicle_event(
            session,
            track,
            event_type="Counting Line Crossed",
            speed=45.0,
        )

        # --------------------------------
        # Signal Decision
        # --------------------------------

        decision = Decision(
            selected_lane=2,
            green_time=30,
            reason="High Queue",
        )

        persistence.save_signal_decision(
            session,
            decision,
        )

        # --------------------------------
        # Camera
        # --------------------------------

        persistence.save_camera(
            session,
            name="Test Camera",
            source="test_video.mp4",
            source_type="file",
            location="Test Junction",
        )

    print("All database inserts completed successfully.")


if __name__ == "__main__":
    main()
