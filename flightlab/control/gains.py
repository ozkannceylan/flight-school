"""Gain containers. Values live in labs/reference — this is just the shape."""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class CascadeGains:
    """Inner-attitude / outer-position PD on the planar quadrotor."""

    kp_y: float
    kd_y: float
    kp_z: float
    kd_z: float
    kp_th: float
    kd_th: float

    def timescale_ratio(self) -> float:
        """ω_n,inner / ω_n,outer ≈ √(kp_θ / kp_y). Want ≥ 5."""
        if self.kp_y <= 0:
            return float("inf")
        return math.sqrt(self.kp_th / self.kp_y)
