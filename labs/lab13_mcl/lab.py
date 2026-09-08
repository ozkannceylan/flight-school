"""Lab 13 — Known Map, Unknown Pose.

Monte Carlo localization. Then kidnap the robot and watch depletion.

    python labs/lab13_mcl/check.py
    python labs/lab13_mcl/demo.py
"""

from __future__ import annotations

import numpy as np

from flightlab.geometry import oplus
from flightlab.sensors import RangeSensor
from flightlab.worlds import OccupancyGrid


# ---------------------------------------------------------------------------
# TODO 1 — sample the odometry model  (≤10 lines)
# ---------------------------------------------------------------------------
def motion_update(
    particles: np.ndarray,
    u: np.ndarray,
    rng: np.random.Generator,
    trans_std: float = 0.08,
    rot_std: float = 0.08,
) -> np.ndarray:
    """``u = (dx, dθ)`` in the body frame. Add noise, then ``oplus`` each pose."""
    # TODO(1)
    raise NotImplementedError("TODO 1: motion_update")


# ---------------------------------------------------------------------------
# TODO 2 — beam likelihood  (≤12 lines)
# ---------------------------------------------------------------------------
def weight(
    particles: np.ndarray,
    z: np.ndarray,
    grid: OccupancyGrid,
    sensor: RangeSensor,
    sigma: float = 0.25,
) -> np.ndarray:
    """``w_i ∝ exp(-½ Σ ((z − ẑ_i)/σ)²)``. Use ``sensor.expected(pose, grid)``."""
    # TODO(2): return weights that sum to 1
    raise NotImplementedError("TODO 2: weight")


# ---------------------------------------------------------------------------
# TODO 3 — resample, optionally inject uniform poses  (≤12 lines)
# ---------------------------------------------------------------------------
def resample(
    particles: np.ndarray,
    weights: np.ndarray,
    rng: np.random.Generator,
    grid: OccupancyGrid,
    inject: float = 0.0,
) -> np.ndarray:
    """Systematic resample, then replace ``inject`` fraction with uniform free poses."""
    # TODO(3)
    raise NotImplementedError("TODO 3: resample")


def uniform_particles(n: int, grid: OccupancyGrid, rng: np.random.Generator) -> np.ndarray:
    """Sample free cells, heading ~ U[−π, π]. Provided."""
    free = np.argwhere(~grid.occ)
    idx = rng.integers(0, len(free), size=n)
    cells = free[idx].astype(float)
    th = rng.uniform(-np.pi, np.pi, size=n)
    return np.column_stack([cells[:, 1] + 0.5, cells[:, 0] + 0.5, th])


def mean_pose(particles: np.ndarray) -> np.ndarray:
    c = np.mean(np.cos(particles[:, 2]))
    s = np.mean(np.sin(particles[:, 2]))
    return np.array([particles[:, 0].mean(), particles[:, 1].mean(), float(np.arctan2(s, c))])
