"""Reference implementation for Lab 10 — Where Could I Possibly Be?"""

from __future__ import annotations

import numpy as np

from flightlab.worlds import OccupancyGrid, successors


def predict(belief: np.ndarray, grid: OccupancyGrid, action: tuple[int, int]) -> np.ndarray:
    out = np.zeros_like(belief, dtype=bool)
    for cell in zip(*np.where(belief), strict=True):
        for nxt in successors(grid, (int(cell[0]), int(cell[1])), action):
            out[nxt] = True
    return out


def update(belief: np.ndarray, consistent: np.ndarray) -> np.ndarray:
    return np.asarray(belief, dtype=bool) & np.asarray(consistent, dtype=bool)


def step(
    belief: np.ndarray,
    grid: OccupancyGrid,
    action: tuple[int, int],
    consistent: np.ndarray | None,
) -> np.ndarray:
    nxt = predict(belief, grid, action)
    if consistent is None:
        return nxt
    return update(nxt, consistent)
