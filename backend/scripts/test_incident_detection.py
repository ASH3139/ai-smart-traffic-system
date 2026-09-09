from backend.app.services.incident_detection.service import (
    IncidentDetectionService,
)


def main():

    service = IncidentDetectionService()

    incidents = service.process(
        tracks=[],
        speeds=[],
        behavior_events={},
    )

    print("Incident Detection Service Test")
    print("--------------------------------")

    print("Incidents detected:", len(incidents))

    if not incidents:
        print("✓ Service initialized and processed empty input successfully.")


if __name__ == "__main__":
    main()
