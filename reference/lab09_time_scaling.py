"""Reference implementation for Lab 09 — Time Is the Free Variable."""

from __future__ import annotations

import numpy as np

from flightlab.dynamics import PlanarQuadrotor
from flightlab.resolve import get

_LAB08 = None


def _lab08():
    global _LAB08
    if _LAB08 is None:
        _LAB08 = get("lab08")
    return _LAB08


def peak_rotor(us: np.ndarray) -> float:
    return float(np.max(np.abs(us)))


def sample_scaled(plant: PlanarQuadrotor, scale: float, dt: float = 0.03):
    return _lab08().sample_flat_traj(plant, dt=dt, scale=scale)


def min_feasible_scale(
    plant: PlanarQuadrotor,
    u_max: float,
    *,
    lo: float = 0.35,
    hi: float = 2.5,
    tol: float = 0.02,
) -> float:
    # Invariant: hi is feasible, lo is not (or below the window).
    _, _, us_hi = sample_scaled(plant, hi)
    if peak_rotor(us_hi) > u_max:
        return hi
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        _, _, us = sample_scaled(plant, mid)
        if peak_rotor(us) <= u_max:
            hi = mid
        else:
            lo = mid
    return hi
