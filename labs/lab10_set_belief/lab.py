"""Lab 10 — Where Could I Possibly Be?

A belief is a *set* of cells. Motion grows it. A sensor measurement cuts it.

    python labs/lab10_set_belief/check.py
    python labs/lab10_set_belief/demo.py
"""

from __future__ import annotations

import numpy as np

from flightlab.worlds import OccupancyGrid, successors


# ---------------------------------------------------------------------------
# TODO 1 — predict: expand every live cell by the motion set  (≤12 lines)
# ---------------------------------------------------------------------------
def predict(belief: np.ndarray, grid: OccupancyGrid, action: tuple[int, int]) -> np.ndarray:
    """``belief`` is a bool array shaped like the grid. Union of ``successors``."""
    # TODO(1): for each True cell, mark every successor of (cell, action)
    raise NotImplementedError("TODO 1: predict")


# ---------------------------------------------------------------------------
# TODO 2 — update: intersect with the cells that could have produced z  (≤6 lines)
# ---------------------------------------------------------------------------
def update(belief: np.ndarray, consistent: np.ndarray) -> np.ndarray:
    """Keep cells that are still believed *and* consistent with the observation."""
    # TODO(2): boolean AND
    raise NotImplementedError("TODO 2: update")


# ---------------------------------------------------------------------------
# TODO 3 — one step  (≤8 lines)
# ---------------------------------------------------------------------------
def step(
    belief: np.ndarray,
    grid: OccupancyGrid,
    action: tuple[int, int],
    consistent: np.ndarray | None,
) -> np.ndarray:
    """Predict, then update if ``consistent`` is not None (open-loop otherwise)."""
    # TODO(3)
    raise NotImplementedError("TODO 3: step")
