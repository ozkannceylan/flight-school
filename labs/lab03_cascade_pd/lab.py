"""Lab 03 — Cascade PD.

Linearize about hover. Inner attitude, outer position. Timescale separation.

    python labs/lab03_cascade_pd/check.py
    python labs/lab03_cascade_pd/demo.py
"""

from __future__ import annotations

import numpy as np

from flightlab.control import CascadeGains
from flightlab.dynamics import PlanarQuadrotor

# A working set. Inner √kp_θ is >5× outer √kp_y.
DEFAULT_GAINS = CascadeGains(kp_y=10.0, kd_y=8.0, kp_z=16.0, kd_z=8.0, kp_th=300.0, kd_th=24.0)


# ---------------------------------------------------------------------------
# TODO 1 — numerical linearization  (≤12 lines)
# ---------------------------------------------------------------------------
def linearize(f, x0, u0, eps: float = 1e-5):
    """Forward-difference A = ∂f/∂x, B = ∂f/∂u at (x0, u0)."""
    x0 = np.asarray(x0, dtype=float).reshape(-1)
    u0 = np.asarray(u0, dtype=float).reshape(-1)
    # TODO(1): return A (n×n), B (n×m)
    raise NotImplementedError("TODO 1: implement linearize")


# ---------------------------------------------------------------------------
# TODO 2 — cascade PD  (≤15 lines)
# ---------------------------------------------------------------------------
def cascade_pd(
    plant: PlanarQuadrotor,
    x: np.ndarray,
    setpoint: np.ndarray,
    gains: CascadeGains = DEFAULT_GAINS,
) -> np.ndarray:
    """Outer position PD → θ_des, T; inner attitude PD → differential thrust.

    ay = kp_y (yd − y) − kd_y vy
    az = kp_z (zd − z) − kd_z vz
    θ_des = clip(−ay / g)
    T = m (az + g)
    τ = I (kp_θ (θ_des − θ) − kd_θ ω)
    u1 = T/2 + τ/(2L),  u2 = T/2 − τ/(2L)
    """
    y, z, th, vy, vz, omega = np.asarray(x, dtype=float).reshape(-1)
    yd, zd = float(setpoint[0]), float(setpoint[1])
    # TODO(2): return np.array([u1, u2])
    raise NotImplementedError("TODO 2: implement cascade_pd")


def controller(x: np.ndarray, t: float = 0.0, *, plant: PlanarQuadrotor | None = None) -> np.ndarray:
    """``(x, t) → u`` at the default hover setpoint. Used by Lab 04 via resolve."""
    plant = plant or PlanarQuadrotor()
    return cascade_pd(plant, x, plant.reset()[:2], DEFAULT_GAINS)
