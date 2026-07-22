class VideoSourceError(Exception):
    """Raised when a video source cannot be opened."""
    pass


class FrameReadError(Exception):
    """Raised when a frame cannot be read."""
    pass