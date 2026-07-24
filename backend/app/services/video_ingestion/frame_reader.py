import cv2
from datetime import datetime

from .config import VideoConfig
from .exceptions import VideoSourceError, FrameReadError
from .models import VideoFrame


class FrameReader:

    def __init__(self):

        self.config = VideoConfig()
        self.capture = None
        self.frame_id = 0

    def open(self):

        self.capture = cv2.VideoCapture(self.config.source)

        if not self.capture.isOpened():
            raise VideoSourceError(
                f"Cannot open video source: {self.config.source}"
            )

        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.height)

    def read(self):

        if self.capture is None:
            raise VideoSourceError("Video source is not opened.")

        success, frame = self.capture.read()

        if not success:

            if self.config.loop_video:
                self.capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
                success, frame = self.capture.read()

            if not success:
                raise FrameReadError("End of video or unable to read frame.")

        self.frame_id += 1

        return VideoFrame(
            frame_id=self.frame_id,
            timestamp=datetime.now(),
            image=frame
        )

    def release(self):

        if self.capture is not None:
            self.capture.release()