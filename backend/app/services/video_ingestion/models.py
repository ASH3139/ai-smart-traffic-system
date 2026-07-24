from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class VideoFrame:
    """
    Represents a single frame with its metadata.
    """

    frame_id: int
    timestamp: datetime
    image: Any