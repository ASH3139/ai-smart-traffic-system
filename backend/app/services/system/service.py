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
from backend.app.services.incident_detection.service import IncidentDetectionService

from backend.app.services.traffic_signal.service import TrafficSignalService
from backend.app.services.decision_engine.service import DecisionEngineService
from .models import FrameResult
from .drawing import SystemDrawer
import threading
import time

from backend.app.database.session_manager import get_db_session
from backend.app.services.persistence.service import PersistenceService
from backend.app.services.video_ingestion.exceptions import VideoEndOfStream


class TrafficSystemService:
    """
    Central orchestrator for the entire traffic analytics system.
    """

    def __init__(self):

        # -----------------------------
        # Video
        # -----------------------------
        self.video = None

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

        self.incident_detection = IncidentDetectionService()

        # -----------------------------
        # AI
        # -----------------------------
        self.signal = TrafficSignalService()

        self.decision = DecisionEngineService()
        self.drawer = SystemDrawer()
        self.persistence = PersistenceService()

        self.last_persistence_time = 0.0
        self.persistence_interval = 10.0
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

        camera_source = None

        try:
            with get_db_session() as session:

                camera = self.persistence.get_active_camera(session)

                if camera is not None:
                    camera_source = camera.source

                    print(f"Using active camera: " f"{camera.name}")

        except Exception:

            import traceback

            print(
                "Unable to load camera from database. "
                "Falling back to YAML configuration."
            )

            traceback.print_exc()

        self.video = VideoService(source=camera_source)

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

        if self.video is not None:
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
        # Incident Detection
        # -----------------------------

        incidents = self.incident_detection.process(
            tracks=tracks,
            speeds=speeds,
            behavior_events=behavior_events,
        )

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

            with get_db_session() as session:

                self.persistence.save_signal_decision(
                    session,
                    decision,
                )
        self._persist_result(
            statistics,
            lane_statistics,
        )
        result = FrameResult(
            frame=frame,
            image=image,
            tracks=tracks,
            speeds=speeds,
            statistics=statistics,
            lane_statistics=lane_statistics,
            behavior_events=behavior_events,
            signal=self.signal.get_state(),
            incidents=incidents,
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

    def _persist_result(self, statistics, lane_statistics):
        """
        Persist periodic traffic analytics and lane analytics.
        """

        current_time = time.monotonic()

        if current_time - self.last_persistence_time < self.persistence_interval:
            return

        with get_db_session() as session:

            self.persistence.save_traffic_statistics(
                session,
                statistics,
            )

            self.persistence.save_lane_statistics(
                session,
                lane_statistics,
            )

        self.last_persistence_time = current_time

    def _processing_loop(self):

        while self.running:

            try:

                self.process_frame()

            except VideoEndOfStream:

                print("Video stream ended.")

                self.running = False
                break

            except Exception:

                import traceback

                traceback.print_exc()

                self.running = False
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
