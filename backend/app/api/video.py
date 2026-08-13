import cv2

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from backend.app.dependencies.system import get_system
from backend.app.services.system.service import TrafficSystemService

router = APIRouter(
    tags=["Video Stream"],
)


def generate_frames(
    system: TrafficSystemService,
):

    while True:

        image = system.get_latest_image()

        if image is None:
            continue

        success, buffer = cv2.imencode(
            ".jpg",
            image,
        )

        if not success:
            continue

        frame = buffer.tobytes()

        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@router.get(
    "/video",
    summary="Stream processed traffic video",
)
def video(
    system: TrafficSystemService = Depends(get_system),
):

    return StreamingResponse(
        generate_frames(system),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )
