"""Reference implementation for Lab 06 — Heuristics, Honest and Otherwise."""

from __future__ import annotations

import heapq
from collections.abc import Callable

from flightlab.worlds import Cell, Costmap, reconstruct

Heuristic = Callable[[Cell, Cell], float]


def _search(costmap: Costmap, start: Cell, goal: Cell, heuristic: Heuristic):
    pq: list[tuple[float, int, Cell]] = [(heuristic(start, goal), 0, start)]
    g = {start: 0.0}
    came: dict[Cell, Cell | None] = {start: None}
    expanded: list[Cell] = []
    seen: set[Cell] = set()
    tie = 1
    while pq:
        _f, _k, u = heapq.heappop(pq)
        if u in seen:
            continue
        seen.add(u)
        expanded.append(u)
        if u == goal:
            break
        for v in costmap.neighbors(u):
            ng = g[u] + costmap.enter_cost(v)
            if ng < g.get(v, float("inf")):
                g[v] = ng
                came[v] = u
                heapq.heappush(pq, (ng + heuristic(v, goal), tie, v))
                tie += 1
    path = reconstruct(came, start, goal)
    cost = g.get(goal, float("inf"))
    return path, expanded, float(cost)


def dijkstra(costmap: Costmap, start: Cell, goal: Cell):
    return _search(costmap, start, goal, lambda a, b: 0.0)


def astar(costmap: Costmap, start: Cell, goal: Cell, heuristic: Heuristic):
    return _search(costmap, start, goal, heuristic)


def inflate(heuristic: Heuristic, factor: float) -> Heuristic:
    return lambda a, b: factor * heuristic(a, b)
