import cv2

from backend.app.services.video_ingestion.frame_reader import FrameReader
from backend.app.services.detection.service import DetectionService


def main():

    reader = FrameReader()
    reader.open()

    detector = DetectionService()

    while True:

        frame = reader.read()

        detections = detector.detect(frame.image)

        image = frame.image.copy()

        for detection in detections:

            cv2.rectangle(
                image,
                (detection.x1, detection.y1),
                (detection.x2, detection.y2),
                (0, 255, 0),
                2
            )

            label = (
                f"{detection.class_name} "
                f"{detection.confidence:.2f}"
            )

            cv2.putText(
                image,
                label,
                (detection.x1, detection.y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

        cv2.imshow("YOLO Vehicle Detection", image)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    reader.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()