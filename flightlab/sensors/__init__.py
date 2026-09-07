"""Synthetic sensors with known noise (Phase 3)."""

from flightlab.sensors.hover_flight import H, discrete_hover, hover_dataset
from flightlab.sensors.imu import IMU
from flightlab.sensors.noise import as_rng, bounded, gaussian
from flightlab.sensors.range import RangeSensor, raycast

__all__ = [
    "H",
    "IMU",
    "RangeSensor",
    "as_rng",
    "bounded",
    "discrete_hover",
    "gaussian",
    "hover_dataset",
    "raycast",
]
