import time

from backend.app.services.traffic_signal.service import TrafficSignalService


def main():

    signal = TrafficSignalService()

    print("=" * 50)
    print("Traffic Signal Test")
    print("=" * 50)

    while True:

        state = signal.update()

        print(
            f"Lane {state.current_green_lane} | "
            f"{state.state.value} | "
            f"{state.remaining_time}s"
        )

        time.sleep(1)


if __name__ == "__main__":
    main()
