import cv2

from backend.app.services.video_ingestion.frame_reader import FrameReader
from backend.app.services.tracking.service import TrackingService


def main():

    reader = FrameReader()
    reader.open()

    tracker = TrackingService()

    while True:

        frame = reader.read()

        tracks = tracker.track(frame.image)

        image = frame.image.copy()

        for track in tracks:

            cv2.rectangle(
                image,
                (track.x1, track.y1),
                (track.x2, track.y2),
                (0, 255, 0),
                2,
            )

            label = f"{track.class_name}  ID:{track.track_id}"

            cv2.putText(
                image,
                label,
                (track.x1, track.y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2,
            )

        cv2.imshow("ByteTrack", image)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    reader.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()