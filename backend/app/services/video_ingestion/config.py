from pathlib import Path
import yaml


CONFIG_FILE = Path("configs/video.yaml")


class VideoConfig:

    def __init__(self):

        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)["video"]

        self.source = config["source"]
        self.width = config["width"]
        self.height = config["height"]
        self.target_fps = config["target_fps"]
        self.loop_video = config["loop_video"]
        self.buffer_size = config["buffer_size"]
        self.display = config["display"]