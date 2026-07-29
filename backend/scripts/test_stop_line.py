import cv2

from backend.app.services.video_ingestion.service import VideoService
from backend.app.services.stop_line.service import StopLineService


def main():

    video = VideoService()
    video.start()

    stop_line = StopLineService()

    while True:

        frame = video.get_frame()

        image = frame.image.copy()

        stop_line.draw(image)

        cv2.imshow("Stop Line Test", image)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    video.stop()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
