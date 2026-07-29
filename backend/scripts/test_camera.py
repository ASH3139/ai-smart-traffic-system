from backend.app.services.camera.service import CameraService


def main():

    service = CameraService()

    camera = service.create_camera(
        camera_id=1,
        name="Camera 1",
        location="North Road",
        junction="Junction A",
    )

    print(camera)


if __name__ == "__main__":
    main()
