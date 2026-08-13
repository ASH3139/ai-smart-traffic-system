from backend.app.services.video_ingestion.service import VideoService
from backend.app.services.tracking.service import TrackingService

from backend.app.services.speed.config import SpeedConfig
from backend.app.services.speed.optical_flow import OpticalFlow
from backend.app.services.speed.service import SpeedService

from backend.app.services.analytics.service import AnalyticsService
from backend.app.services.lane.service import LaneService
from backend.app.services.lane_analytics.service import LaneAnalyticsService

from backend.app.services.roi.service import ROIService
from backend.app.services.stop_line.service import StopLineService
from backend.app.services.counting_line.service import CountingLineService
from backend.app.services.behavior.service import BehaviorService

from backend.app.services.traffic_signal.service import TrafficSignalService
from backend.app.services.decision_engine.service import DecisionEngineService
from .models import FrameResult
from .drawing import SystemDrawer
import threading
import time


class TrafficSystemService:
    """
    Central orchestrator for the entire traffic analytics system.
    """

    def __init__(self):

        # -----------------------------
        # Video
        # -----------------------------
        self.video = VideoService()

        # -----------------------------
        # Tracking
        # -----------------------------
        self.tracker = TrackingService()

        # -----------------------------
        # Speed
        # -----------------------------
        speed_config = SpeedConfig()

        self.optical_flow = OpticalFlow(speed_config.optical_flow)

        self.speed = SpeedService(speed_config)

        # -----------------------------
        # Analytics
        # -----------------------------
        self.analytics = AnalyticsService()

        self.lane_analytics = LaneAnalyticsService()

        # -----------------------------
        # Spatial
        # -----------------------------
        self.lane = LaneService()

        self.roi = ROIService()

        self.stop_line = StopLineService()

        self.counting_line = CountingLineService()

        self.behavior = BehaviorService(
            stop_line_y=self.stop_line.stop_line.start[1],
            counting_line_y=self.counting_line.counting_line.start[1],
        )

        # -----------------------------
        # AI
        # -----------------------------
        self.signal = TrafficSignalService()

        self.decision = DecisionEngineService()
        self.drawer = SystemDrawer()
        # -----------------------------
        # Background Processing
        # -----------------------------

        self.running = False
        self.thread = None
        self.latest_result = None
        self.latest_image = None

    # -----------------------------
    # Public API
    # -----------------------------

    def start(self):
        """
        Start background processing.
        """

        self.video.start()

        self.running = True

        self.thread = threading.Thread(
            target=self._processing_loop,
            daemon=True,
        )

        self.thread.start()

    def stop(self):
        """
        Stop background processing.
        """

        self.running = False

        if self.thread is not None:
            self.thread.join()

        self.video.stop()

    def process_frame(self):
        """
        Process one complete frame through the AI pipeline.
        """

        frame = self.video.get_frame()

        image = frame.image.copy()

        # -----------------------------
        # Tracking
        # -----------------------------
        tracks = self.tracker.track(image)

        for track in tracks:
            self.lane.assign_lane(track)

        # -----------------------------
        # Optical Flow
        # -----------------------------

        flow = self.optical_flow.compute(image)
        # -----------------------------
        # Speed
        # -----------------------------

        speeds = self.speed.calculate(
            flow,
            tracks,
        )

        # -----------------------------
        # Analytics
        # -----------------------------
        statistics = self.analytics.process(
            frame,
            tracks,
            speeds,
        )

        lane_statistics = self.lane_analytics.process(
            tracks,
            speeds,
        )

        # -----------------------------
        # Behavior
        # -----------------------------
        behavior_events = {}

        for track in tracks:

            behavior_events[track.track_id] = self.behavior.update(track)

        # -----------------------------
        # Decision Engine
        # -----------------------------

        needs_decision = self.signal.update()

        if needs_decision:

            decision = self.decision.process(
                lane_statistics,
                self.signal.get_state().current_green_lane,
            )

            self.signal.apply_decision(decision)
        result = FrameResult(
            frame=frame,
            image=image,
            tracks=tracks,
            speeds=speeds,
            statistics=statistics,
            lane_statistics=lane_statistics,
            behavior_events=behavior_events,
            signal=self.signal.get_state(),
        )

        image = self.drawer.draw(
            image,
            result,
            self,
        )

        result.image = image
        self.latest_result = result
        self.latest_image = image.copy()
        return result

    def _processing_loop(self):

        while self.running:

            try:

                self.process_frame()

            except Exception as e:

                import traceback

                traceback.print_exc()

                break

            time.sleep(0.001)

    def get_latest_result(self):
        """
        Returns the latest processed frame.
        """

        return self.latest_result

    def get_latest_image(self):
        """
        Returns the latest processed image.
        """

        return self.latest_image
