import cv2

from backend.app.services import counting_line
from backend.app.services.video_ingestion.service import VideoService
from backend.app.services.counting_line.service import CountingLineService


def main():

    video = VideoService()
    video.start()

    counting_line = CountingLineService()

    while True:

        frame = video.get_frame()

        image = frame.image.copy()

        counting_line.draw(image)

        cv2.imshow("Counting Line Test", image)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    video.stop()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
