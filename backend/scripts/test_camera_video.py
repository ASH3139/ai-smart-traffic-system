import cv2

from backend.app.database.session_manager import get_db_session
from backend.app.services.persistence.service import PersistenceService
from backend.app.services.video_ingestion.service import VideoService


def main():

    persistence = PersistenceService()

    with get_db_session() as session:

        camera = persistence.get_active_camera(session)

        if camera is None:
            print("No active camera found.")
            return

        print(f"Using camera source: {camera.source}")

        video = VideoService(source=camera.source)

        video.start()

        print(video.video_info)

        frame = video.get_frame()

        print(f"First frame shape: {frame.image.shape}")

        video.stop()


if __name__ == "__main__":
    main()
