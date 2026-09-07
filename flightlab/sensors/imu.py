"""Planar IMU: gyro (yaw rate) + body-frame accelerometer, with a constant bias."""

from __future__ import annotations

import numpy as np

from flightlab.sensors.noise import as_rng


class IMU:
    """``measure(omega, accel) -> (gyro, accel_meas)``. Bias is added to the gyro."""

    def __init__(
        self,
        gyro_sigma: float = 0.02,
        accel_sigma: float = 0.08,
        gyro_bias: float = 0.0,
    ) -> None:
        self.gyro_sigma = float(gyro_sigma)
        self.accel_sigma = float(accel_sigma)
        self.gyro_bias = float(gyro_bias)

    def measure(
        self,
        omega: float,
        accel: np.ndarray,
        rng: int | np.random.Generator | None = 0,
    ) -> tuple[float, np.ndarray]:
        g = as_rng(rng)
        gyro = float(omega) + self.gyro_bias + float(g.normal(0.0, self.gyro_sigma))
        acc = np.asarray(accel, dtype=float).reshape(-1) + g.normal(
            0.0, self.accel_sigma, size=np.asarray(accel).size
        )
        return gyro, acc
