"""Occupancy grids — 4-connected, unit cells. Used by Labs 05–06."""

from __future__ import annotations

from collections.abc import Iterable

import numpy as np

Cell = tuple[int, int]  # (row, col)
_NEIGHBORS = ((-1, 0), (1, 0), (0, -1), (0, 1))


class OccupancyGrid:
    """``occ[r, c] == True`` is blocked. Row 0 is the top of the printed map."""

    def __init__(self, occ: np.ndarray) -> None:
        self.occ = np.asarray(occ, dtype=bool)
        self.rows, self.cols = self.occ.shape

    def in_bounds(self, cell: Cell) -> bool:
        r, c = cell
        return 0 <= r < self.rows and 0 <= c < self.cols

    def is_free(self, cell: Cell) -> bool:
        return self.in_bounds(cell) and not bool(self.occ[cell])

    def neighbors(self, cell: Cell) -> list[Cell]:
        r, c = cell
        out: list[Cell] = []
        for dr, dc in _NEIGHBORS:
            nxt = (r + dr, c + dc)
            if self.is_free(nxt):
                out.append(nxt)
        return out

    def cells(self) -> Iterable[Cell]:
        for r in range(self.rows):
            for c in range(self.cols):
                yield r, c


def grid_from_ascii(lines: list[str]) -> tuple[OccupancyGrid, Cell, Cell]:
    """``#`` wall, ``.`` free, ``S`` start, ``G`` goal."""
    rows = [list(s.rstrip("\n")) for s in lines if s.strip() != ""]
    h, w = len(rows), max(len(r) for r in rows)
    occ = np.ones((h, w), dtype=bool)
    start = goal = None
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch == "#":
                continue
            occ[r, c] = False
            if ch == "S":
                start = (r, c)
            elif ch == "G":
                goal = (r, c)
    if start is None or goal is None:
        raise ValueError("ascii map needs S and G")
    return OccupancyGrid(occ), start, goal


def maze_lab05() -> tuple[OccupancyGrid, Cell, Cell]:
    """Corridor maze. BFS shortest path length (in edges) is 16."""
    return grid_from_ascii(
        [
            "S..#........",
            ".#.#.######.",
            ".#.#......#.",
            ".#.####.#.#.",
            ".#......#.#.",
            ".########.#.",
            "..........G.",
        ]
    )


def reconstruct(came_from: dict[Cell, Cell | None], start: Cell, goal: Cell) -> list[Cell]:
    if goal not in came_from:
        return []
    path = [goal]
    cur = goal
    while cur != start:
        prev = came_from[cur]
        if prev is None:
            return []
        cur = prev
        path.append(cur)
    path.reverse()
    return path
