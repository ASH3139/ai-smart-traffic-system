from backend.app.database.session_manager import get_db_session
from backend.app.services.persistence.service import PersistenceService
from backend.app.services.video_ingestion.multi_camera import (
    MultiCameraService,
)


def main():

    persistence = PersistenceService()

    with get_db_session() as session:

        cameras = persistence.get_cameras_by_junction(
            session=session,
            junction_id=1,
        )

        if not cameras:
            print("No cameras found.")
            return

        multi_camera = MultiCameraService(cameras)

        print("=" * 50)
        print("Multi-Camera Test")
        print("=" * 50)

        print(f"Camera count: " f"{multi_camera.camera_count}")

        print(f"Lane IDs: " f"{multi_camera.lane_ids}")

        multi_camera.start()

        print("All configured cameras started.")

        frames = multi_camera.get_frames()

        for lane_id, frame in frames.items():

            print(
                f"Lane {lane_id}: "
                f"Frame {frame.frame_id} | "
                f"Shape {frame.image.shape}"
            )

        multi_camera.stop()

        print("All cameras stopped.")


if __name__ == "__main__":
    main()
