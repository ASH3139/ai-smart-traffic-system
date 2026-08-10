from backend.app.services.decision_engine.service import (
    DecisionEngineService,
)
from backend.app.services.lane_analytics.models import LaneStatistics


def main():

    lane_statistics = [
        LaneStatistics(
            lane_id=1,
            vehicle_count=8,
            average_speed=18,
            density=0.40,
            queue_length=5,
            traffic_flow=480,
        ),
        LaneStatistics(
            lane_id=2,
            vehicle_count=3,
            average_speed=28,
            density=0.15,
            queue_length=1,
            traffic_flow=180,
        ),
        LaneStatistics(
            lane_id=3,
            vehicle_count=6,
            average_speed=12,
            density=0.30,
            queue_length=7,
            traffic_flow=360,
        ),
    ]

    engine = DecisionEngineService()

    decision = engine.process(
        lane_statistics,
        current_green_lane=1,
    )

    print("=" * 50)
    print("AI DECISION")
    print("=" * 50)

    print(f"Selected Lane : {decision.selected_lane}")
    print(f"Green Time    : {decision.green_time} sec")
    print(f"Reason        : {decision.reason}")


if __name__ == "__main__":
    main()
