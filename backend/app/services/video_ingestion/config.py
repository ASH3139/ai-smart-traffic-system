from backend.app.shared.config_manager import ConfigManager


class VideoConfig:

    def __init__(self):

        config = ConfigManager.get("video")["video"]

        self.source = config["source"]
        self.target_fps = config["target_fps"]
        self.width = config["width"]
        self.height = config["height"]
        self.buffer_size = config["buffer_size"]