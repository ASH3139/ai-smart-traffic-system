"""
Analytics execution pipeline.

Each calculator updates the shared
TrafficStatistics object.
"""

from backend.app.services.analytics.calculators.vehicle_counter import VehicleCounter
from backend.app.services.analytics.calculators.average_speed import AverageSpeedCalculator

PIPELINE = [

    VehicleCounter(),

    AverageSpeedCalculator(),

]