import cv2
import numpy as np

from .config import ROIConfig
from .models import ROI


class ROIService:

    def __init__(self):

        self.config = ROIConfig()

        self.roi = ROI(self.config.polygon)

    def draw(self, image):

        points = np.array(
            self.roi.points,
            dtype=np.int32,
        )

        cv2.polylines(
            image,
            [points],
            isClosed=True,
            color=(0, 0, 255),
            thickness=2,
        )

        return image
