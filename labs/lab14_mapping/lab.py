"""Lab 14 — Known Pose, Unknown Map.

The mirror of Lab 13. Inverse sensor model + log-odds, because multiplying
probabilities is a trap.

    python labs/lab14_mapping/check.py
    python labs/lab14_mapping/demo.py
"""

from __future__ import annotations

import numpy as np

from flightlab.sensors import RangeSensor, raycast
from flightlab.worlds import OccupancyGrid  # noqa: F401 — useful while tinkering

L_OCC = float(np.log(0.70 / 0.30))
L_FREE = float(np.log(0.30 / 0.70))


# ---------------------------------------------------------------------------
# TODO 1 — inverse beam: free along the ray, occupied at the hit  (≤15 lines)
# ---------------------------------------------------------------------------
def inverse_beam(
    shape: tuple[int, int],
    pose: np.ndarray,
    z: float,
    angle: float,
    *,
    step: float = 0.25,
    max_range: float = 7.0,
    l_occ: float = L_OCC,
    l_free: float = L_FREE,
) -> np.ndarray:
    """Return a log-odds *increment* field. Beyond the hit, leave zeros."""
    # TODO(1): walk the ray like raycast; mark free cells; mark the hit occupied
    raise NotImplementedError("TODO 1: inverse_beam")


# ---------------------------------------------------------------------------
# TODO 2 — log-odds accumulate  (≤6 lines)
# ---------------------------------------------------------------------------
def logodds_update(l_map: np.ndarray, increment: np.ndarray, clip: float = 8.0) -> np.ndarray:
    """``l ← clip(l + increment, ±clip)``."""
    # TODO(2)
    raise NotImplementedError("TODO 2: logodds_update")


# ---------------------------------------------------------------------------
# TODO 3 — the naive probability update that underflows  (≤8 lines)
# ---------------------------------------------------------------------------
def naive_miss(p: float, n: int, p_occ_given_miss: float = 0.05) -> float:
    """Apply a miss update ``n`` times: ``p ← p·q / (p·q + (1-p)·(1-q))``."""
    # TODO(3)
    raise NotImplementedError("TODO 3: naive_miss")


def integrate_scan(
    l_map: np.ndarray,
    pose: np.ndarray,
    z: np.ndarray,
    sensor: RangeSensor,
) -> np.ndarray:
    """Apply every beam. Provided — calls your inverse_beam + logodds_update."""
    out = np.asarray(l_map, dtype=float)
    for ang, zi in zip(sensor.angles, np.asarray(z, dtype=float), strict=True):
        inc = inverse_beam(out.shape, pose, float(zi), float(ang), max_range=sensor.max_range, step=sensor.step)
        out = logodds_update(out, inc)
    return out


def occupancy(l_map: np.ndarray) -> np.ndarray:
    return np.asarray(l_map, dtype=float) > 0.0
