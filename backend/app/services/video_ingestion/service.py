from .frame_reader import FrameReader


class VideoService:
    """
    High-level interface for video ingestion.
    """

    def __init__(self):

        self.reader = FrameReader()

    def start(self):

        self.reader.open()

    def get_frame(self):

        return self.reader.read()

    def stop(self):

        self.reader.release()

    @property
    def fps(self):

        return self.reader.fps

    @property
    def video_info(self):

        return self.reader.video_info