import time

from .config import TrafficSignalConfig
from .models import TrafficSignal, SignalState


class TrafficSignalService:
    """
    Controls the traffic signal state machine.
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
        Update the signal timer.
        """

        now = time.time()

        elapsed = now - self.last_update

        if elapsed < 1:
            return self.signal

        self.last_update = now

        self.signal.remaining_time -= 1

        if self.signal.remaining_time > 0:
            return self.signal

        self._next_state()

        return self.signal

    def get_state(self):

        return self.signal

    # ----------------------------------
    # Internal State Machine
    # ----------------------------------

    def _next_state(self):

        if self.signal.state == SignalState.GREEN:

            self.signal.state = SignalState.YELLOW
            self.signal.remaining_time = self.signal.yellow_time

            return

        if self.signal.state == SignalState.YELLOW:

            self.signal.current_green_lane += 1

            if self.signal.current_green_lane > self.config.lane_count:
                self.signal.current_green_lane = 1

            self.signal.state = SignalState.GREEN

            self.signal.remaining_time = self.signal.green_time
