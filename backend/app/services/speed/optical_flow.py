import cv2
import numpy as np


class OpticalFlowEngine:
    """
    Computes dense optical flow using Farneback's algorithm.
    """

    def __init__(self, config):

        self.config = config

        self.previous_gray = None