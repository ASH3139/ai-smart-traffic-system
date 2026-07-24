import cv2

from backend.app.services.video_ingestion.frame_reader import FrameReader


def main():

    reader = FrameReader()
    reader.open()

    while True:

        frame = reader.read()

        cv2.imshow(
            "Traffic Video",
            frame.image
        )

        key = cv2.waitKey(1)

        if key == ord("q"):
            break

    reader.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()