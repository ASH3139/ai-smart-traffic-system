from dataclasses import dataclass
from typing import Union


@dataclass
class VideoConfig:
    """
    Configuration for video sources.
    """

    source: Union[int, str] = 0
    width: int = 1280
    height: int = 720
    fps: int = 30