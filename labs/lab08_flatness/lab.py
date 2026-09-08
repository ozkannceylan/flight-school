"""Lab 08 — Plan in Flat Space, Fly in Real Space.

The composition lab: path → min-snap → LQR + feedforward → Lab 01 plant.

    python labs/lab08_flatness/check.py
    python labs/lab08_flatness/demo.py
"""

from __future__ import annotations

import numpy as np

from flightlab.dynamics import PlanarQuadrotor
from flightlab.planning.flatness import eval_piecewise, piecewise_quintic

WAYPOINTS = np.array(
    [
        [0.0, 1.0],
        [1.0, 1.55],
        [2.1, 1.15],
        [3.0, 1.70],
    ]
)
DURATIONS = np.array([1.4, 1.4, 1.4])


# ---------------------------------------------------------------------------
# TODO 1 — invert the flat outputs  (≤12 lines)
# ---------------------------------------------------------------------------
def flat_to_xu(y, z, yd, zd, ydd, zdd, yj, zj, ys, zs, plant: PlanarQuadrotor):
    """θ = atan2(−ÿ, z̈+g), T = m ‖(ÿ, z̈+g)‖, τ = I θ̈, split T±τ.

    Return ``x`` (6,), ``u`` (2,).
    """
    # TODO(1)
    raise NotImplementedError("TODO 1: flat_to_xu")


# ---------------------------------------------------------------------------
# TODO 2 — sample the piecewise-quintic trajectory  (≤12 lines)
# ---------------------------------------------------------------------------
def sample_flat_traj(plant: PlanarQuadrotor, dt: float = 0.02, scale: float = 1.0):
    """Return ``t, xs, us`` along ``WAYPOINTS`` with durations ``scale * DURATIONS``.

    ``piecewise_quintic`` / ``eval_piecewise`` are provided. Use *your* ``flat_to_xu``.
    """
    # TODO(2)
    raise NotImplementedError("TODO 2: sample_flat_traj")


# ---------------------------------------------------------------------------
# TODO 3 — feedforward + LQR feedback  (≤8 lines)
# ---------------------------------------------------------------------------
def ff_fb_control(x, x_nom, u_nom, K):
    """u = u_nom − K (x − x_nom)."""
    # TODO(3)
    raise NotImplementedError("TODO 3: ff_fb_control")


def fb_only_control(x, x_nom, u_hover, K):
    """Same K, but feedforward is just hover. The baseline."""
    return u_hover - K @ (np.asarray(x, dtype=float) - np.asarray(x_nom, dtype=float))
