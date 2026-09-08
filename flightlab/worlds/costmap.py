"""Nonuniform terrain costs for Dijkstra / A* (Lab 06)."""

from __future__ import annotations

import numpy as np

from flightlab.worlds.grid import Cell, OccupancyGrid


class Costmap:
    """``cost[r, c]`` is the cost to *enter* that cell. Walls are ``np.inf``."""

    def __init__(self, cost: np.ndarray) -> None:
        self.cost = np.asarray(cost, dtype=float)
        self.grid = OccupancyGrid(~np.isfinite(self.cost))

    @property
    def rows(self) -> int:
        return self.cost.shape[0]

    @property
    def cols(self) -> int:
        return self.cost.shape[1]

    def enter_cost(self, cell: Cell) -> float:
        return float(self.cost[cell])

    def neighbors(self, cell: Cell) -> list[Cell]:
        return self.grid.neighbors(cell)


def manhattan(a: Cell, b: Cell) -> float:
    return float(abs(a[0] - b[0]) + abs(a[1] - b[1]))


def euclidean(a: Cell, b: Cell) -> float:
    return float(np.hypot(a[0] - b[0], a[1] - b[1]))


def open_field_lab06() -> tuple[Costmap, Cell, Cell]:
    """Large uniform room — Dijkstra floods, admissible A* aims."""
    h, w = 21, 31
    cost = np.ones((h, w), dtype=float)
    start, goal = (10, 1), (10, 29)
    return Costmap(cost), start, goal


def terrain_lab06() -> tuple[Costmap, Cell, Cell]:
    """Cheap long detour vs expensive short hallway.

    Admissible A* matches Dijkstra. Inflated Manhattan prefers the hallway
    and comes out suboptimal.
    """
    h, w = 9, 15
    cost = np.ones((h, w), dtype=float)
    cost[1:8, 7] = np.inf  # vertical wall
    cost[4, 7] = 12.0  # expensive door (the shortcut)
    start, goal = (4, 1), (4, 13)
    cost[start] = 1.0
    cost[goal] = 1.0
    return Costmap(cost), start, goal
