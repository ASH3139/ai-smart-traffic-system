import cv2

from backend.app.services.system.service import TrafficSystemService
import time


def main():

    system = TrafficSystemService()

    start = time.perf_counter()

    system.start()

    print(f"System.start() took {time.perf_counter() - start:.2f} sec")

    print("=" * 60)
    print("Traffic Analytics Started")
    print("=" * 60)

    try:

        while True:

            image = system.get_latest_image()

            if image is None:
                continue

            cv2.imshow(
                "Traffic Analytics",
                image,
            )

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

    finally:

        system.stop()

        cv2.destroyAllWindows()


if __name__ == "__main__":

    main()
