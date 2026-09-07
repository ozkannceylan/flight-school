"""Lab 05 — Search, Visualized.

One loop, two frontiers: a queue blooms, a stack snakes.

    python labs/lab05_search_visualized/check.py
    python labs/lab05_search_visualized/demo.py
"""

from __future__ import annotations

from collections import deque

from flightlab.worlds import Cell, OccupancyGrid, reconstruct


# ---------------------------------------------------------------------------
# TODO 1 — FIFO frontier (BFS)  (≤8 lines)
# ---------------------------------------------------------------------------
class QueueFrontier:
    def __init__(self) -> None:
        self._q: deque[Cell] = deque()

    def push(self, item: Cell) -> None:
        # TODO(1): enqueue
        raise NotImplementedError("TODO 1: QueueFrontier.push")

    def pop(self) -> Cell:
        # TODO(1): dequeue from the front
        raise NotImplementedError("TODO 1: QueueFrontier.pop")

    def __len__(self) -> int:
        return len(self._q)

    def __bool__(self) -> bool:
        return bool(self._q)


# ---------------------------------------------------------------------------
# TODO 2 — LIFO frontier (DFS)  (≤6 lines)
# ---------------------------------------------------------------------------
class StackFrontier:
    def __init__(self) -> None:
        self._q: list[Cell] = []

    def push(self, item: Cell) -> None:
        # TODO(2): push
        raise NotImplementedError("TODO 2: StackFrontier.push")

    def pop(self) -> Cell:
        # TODO(2): pop from the back
        raise NotImplementedError("TODO 2: StackFrontier.pop")

    def __len__(self) -> int:
        return len(self._q)

    def __bool__(self) -> bool:
        return bool(self._q)


# ---------------------------------------------------------------------------
# TODO 3 — the shared search loop  (≤15 lines)
# ---------------------------------------------------------------------------
def graph_search(
    grid: OccupancyGrid,
    start: Cell,
    goal: Cell,
    frontier,
) -> tuple[list[Cell], list[Cell]]:
    """Return ``(path, expanded)``. Mark on enqueue. Use ``grid.neighbors``."""
    # TODO(3): frontier.push(start); came_from = {start: None}; then the loop
    raise NotImplementedError("TODO 3: graph_search")


def bfs(grid, start, goal):
    return graph_search(grid, start, goal, QueueFrontier())


def dfs(grid, start, goal):
    return graph_search(grid, start, goal, StackFrontier())
