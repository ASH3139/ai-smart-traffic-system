import cv2

from backend.app.services.video_ingestion.service import VideoService
from backend.app.services.roi.service import ROIService


def main():

    video = VideoService()
    video.start()

    roi = ROIService()

    while True:

        frame = video.get_frame()

        image = frame.image.copy()

        roi.draw(image)

        cv2.imshow("ROI Test", image)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    video.stop()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
