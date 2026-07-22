import cv2

from .config import VideoConfig
from .exceptions import VideoSourceError, FrameReadError


class FrameReader:
    """
    Reads frames from a video source.
    """

    def __init__(self, config: VideoConfig):
        self.config = config
        self.capture = None

    def open(self):
        """
        Open the video source.
        """
        self.capture = cv2.VideoCapture(self.config.source)

        if not self.capture.isOpened():
            raise VideoSourceError(
                f"Unable to open video source: {self.config.source}"
            )

        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.height)
        self.capture.set(cv2.CAP_PROP_FPS, self.config.fps)

    def read(self):
        """
        Read a single frame.
        """
        if self.capture is None:
            raise VideoSourceError("Video source is not opened.")

        success, frame = self.capture.read()

        if not success:
            raise FrameReadError("Unable to read frame.")

        return frame

    def release(self):
        """
        Release the video source.
        """
        if self.capture is not None:
            self.capture.release()