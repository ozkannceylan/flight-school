"""Lab 07 — Sampling Your Way Out.

Grids die in high dimensions. Grow a tree instead.

    python labs/lab07_rrt/check.py
    python labs/lab07_rrt/demo.py
"""

from __future__ import annotations

import numpy as np

from flightlab.worlds import ObstacleField


# ---------------------------------------------------------------------------
# TODO 1 — RRT  (≤15 lines of the loop; helpers are yours)
# ---------------------------------------------------------------------------
def rrt(
    field: ObstacleField,
    start: np.ndarray,
    goal: np.ndarray,
    *,
    seed: int = 0,
    n_iter: int = 400,
    step: float = 0.35,
    goal_bias: float = 0.12,
    goal_tol: float = 0.30,
):
    """Return ``(path, nodes, parents)``. ``parents[i]`` is an index, ``-1`` at root.

    Sample, steer a ``step`` toward the sample, keep the node if the segment
    is free. Stop when a node lands within ``goal_tol`` of the goal.
    """
    # TODO(1)
    raise NotImplementedError("TODO 1: rrt")


# ---------------------------------------------------------------------------
# TODO 2 — RRT* rewiring  (≤15 lines beyond RRT)
# ---------------------------------------------------------------------------
def rrt_star(
    field: ObstacleField,
    start: np.ndarray,
    goal: np.ndarray,
    *,
    seed: int = 0,
    n_iter: int = 400,
    step: float = 0.35,
    goal_bias: float = 0.12,
    goal_tol: float = 0.30,
    radius: float = 0.8,
):
    """RRT plus: choose the cheapest parent in a ball, then rewire neighbors."""
    # TODO(2)
    raise NotImplementedError("TODO 2: rrt_star")


# ---------------------------------------------------------------------------
# TODO 3 — shortcut  (≤10 lines)
# ---------------------------------------------------------------------------
def shortcut(path: np.ndarray, field: ObstacleField, passes: int = 8) -> np.ndarray:
    """Greedily skip waypoints when the straight segment is free."""
    # TODO(3)
    raise NotImplementedError("TODO 3: shortcut")
