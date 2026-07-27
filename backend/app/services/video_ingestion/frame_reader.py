import cv2
import time

from .config import VideoConfig
from .exceptions import VideoOpenError, FrameReadError
from .models import Frame, VideoInfo


class FrameReader:
    """
    Reads frames from a video source.

    Supports:
    - MP4 videos
    - USB cameras
    - RTSP streams
    """

    def __init__(self):

        self.config = VideoConfig()

        self.capture = None

        self.frame_id = 0

        self.video_info = None

    @property
    def fps(self):
        if self.video_info:
            return self.video_info.fps
        return self.config.target_fps

    def open(self):

        self.capture = cv2.VideoCapture(
            self.config.source
        )

        if not self.capture.isOpened():
            raise VideoOpenError(
                f"Unable to open video source: {self.config.source}"
            )

        width = int(
            self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        )

        height = int(
            self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        )

        fps = self.capture.get(
            cv2.CAP_PROP_FPS
        )

        if fps <= 0:
            fps = self.config.target_fps

        total_frames = int(
            self.capture.get(
                cv2.CAP_PROP_FRAME_COUNT
            )
        )

        if total_frames <= 0:
            total_frames = None

        self.video_info = VideoInfo(
            width=width,
            height=height,
            fps=fps,
            total_frames=total_frames,
            source=self.config.source,
        )

    def read(self):

        if self.capture is None:
            raise VideoOpenError(
                "Video source is not opened."
            )

        success, image = self.capture.read()

        if not success:
            raise FrameReadError(
                "End of video reached."
            )

        self.frame_id += 1

        return Frame(
            frame_id=self.frame_id,
            image=image,
            timestamp=time.time(),
        )

    def release(self):

        if self.capture is not None:
            self.capture.release()

        self.capture = None

    def is_open(self):

        return (
            self.capture is not None
            and self.capture.isOpened()
        )