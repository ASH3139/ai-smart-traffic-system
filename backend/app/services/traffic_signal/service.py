import time

from .config import TrafficSignalConfig
from .models import TrafficSignal, SignalState


class TrafficSignalService:
    """
    Controls the traffic signal.
    """

    def __init__(self):

        self.config = TrafficSignalConfig()

        self.signal = TrafficSignal(
            current_green_lane=1,
            state=SignalState.GREEN,
            green_time=self.config.default_green_time,
            yellow_time=self.config.yellow_time,
            red_time=self.config.default_green_time,
            remaining_time=self.config.default_green_time,
        )

        self.last_update = time.time()

    # ----------------------------------
    # Public API
    # ----------------------------------

    def update(self):
        """
        Update the traffic signal timer.

        Returns:
            bool: True if a new AI decision is required.
        """

        now = time.time()

        elapsed = now - self.last_update

        if elapsed < 1:
            return False

        self.last_update = now

        self.signal.remaining_time -= 1

        if self.signal.remaining_time > 0:
            return False

        return True

    def get_state(self):

        return self.signal

    def apply_decision(self, decision):
        """
        Apply a new decision from the AI.
        """

        self.signal.current_green_lane = decision.selected_lane

        self.signal.green_time = decision.green_time

        self.signal.remaining_time = decision.green_time

        self.signal.state = SignalState.GREEN

        self.signal.last_reason = decision.reason
