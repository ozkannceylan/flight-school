"""Lab 09 — Time Is the Free Variable.

The path is fixed. Speed is the only knob. Binary-search until u saturates.

    python labs/lab09_time_scaling/check.py
    python labs/lab09_time_scaling/demo.py
"""

from __future__ import annotations

import numpy as np

from flightlab.dynamics import PlanarQuadrotor
from flightlab.resolve import get


# ---------------------------------------------------------------------------
# TODO 1 — peak rotor command along a scaled traj  (≤8 lines)
# ---------------------------------------------------------------------------
def peak_rotor(us: np.ndarray) -> float:
    """Max of |u1|, |u2| over the trajectory."""
    # TODO(1)
    raise NotImplementedError("TODO 1: peak_rotor")


# ---------------------------------------------------------------------------
# TODO 2 — sample at a duration scale  (≤6 lines)
# ---------------------------------------------------------------------------
def sample_scaled(plant: PlanarQuadrotor, scale: float, dt: float = 0.03):
    """``get('lab08').sample_flat_traj(plant, dt, scale)`` — return t, xs, us."""
    # TODO(2)
    raise NotImplementedError("TODO 2: sample_scaled")


# ---------------------------------------------------------------------------
# TODO 3 — binary-search the fastest feasible scale  (≤15 lines)
# ---------------------------------------------------------------------------
def min_feasible_scale(
    plant: PlanarQuadrotor,
    u_max: float,
    *,
    lo: float = 0.35,
    hi: float = 2.5,
    tol: float = 0.02,
) -> float:
    """Smallest ``scale`` (duration multiplier) with ``peak_rotor(us) ≤ u_max``.

    ``scale < 1`` is *faster*. Search until ``hi - lo < tol`` and return ``hi``.
    """
    # TODO(3)
    raise NotImplementedError("TODO 3: min_feasible_scale")
