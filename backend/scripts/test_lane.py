from backend.app.services.lane.service import LaneService


def main():

    service = LaneService()

    test_points = [150, 700, 1400, 1850]

    for x in test_points:

        lane = service.get_lane(x)

        if lane:

            print(f"Vehicle at x={x} -> {lane.name}")

        else:

            print(f"Vehicle at x={x} -> No Lane")


if __name__ == "__main__":
    main()
