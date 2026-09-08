"""Lab 06 — Heuristics, Honest and Otherwise.

Dijkstra is A* with h = 0. Inflate h and optimality dies.

    python labs/lab06_heuristics/check.py
    python labs/lab06_heuristics/demo.py
"""

from __future__ import annotations

from collections.abc import Callable

from flightlab.worlds import Cell, Costmap, reconstruct

Heuristic = Callable[[Cell, Cell], float]


# ---------------------------------------------------------------------------
# TODO 1 — Dijkstra  (≤15 lines)
# ---------------------------------------------------------------------------
def dijkstra(costmap: Costmap, start: Cell, goal: Cell) -> tuple[list[Cell], list[Cell], float]:
    """Uniform-cost search. Return ``(path, expanded, path_cost)``.

    Edge cost of ``u → v`` is ``costmap.enter_cost(v)``. Use a heap
    (``import heapq``). Count a node as expanded when you *pop* it first.
    """
    # TODO(1)
    raise NotImplementedError("TODO 1: dijkstra")


# ---------------------------------------------------------------------------
# TODO 2 — A*  (≤15 lines)
# ---------------------------------------------------------------------------
def astar(
    costmap: Costmap,
    start: Cell,
    goal: Cell,
    heuristic: Heuristic,
) -> tuple[list[Cell], list[Cell], float]:
    """Same as Dijkstra, but priority is ``g + h(v, goal)``."""
    # TODO(2)
    raise NotImplementedError("TODO 2: astar")


# ---------------------------------------------------------------------------
# TODO 3 — inflate a heuristic  (≤3 lines)
# ---------------------------------------------------------------------------
def inflate(heuristic: Heuristic, factor: float) -> Heuristic:
    """Return ``λ a,b: factor * heuristic(a,b)``."""
    # TODO(3)
    raise NotImplementedError("TODO 3: inflate")
