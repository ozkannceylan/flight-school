"""Reference implementation for Lab 05 — Search, Visualized."""

from __future__ import annotations

from collections import deque

from flightlab.worlds import Cell, OccupancyGrid, reconstruct


class QueueFrontier:
    def __init__(self) -> None:
        self._q: deque[Cell] = deque()

    def push(self, item: Cell) -> None:
        self._q.append(item)

    def pop(self) -> Cell:
        return self._q.popleft()

    def __len__(self) -> int:
        return len(self._q)

    def __bool__(self) -> bool:
        return bool(self._q)


class StackFrontier:
    def __init__(self) -> None:
        self._q: list[Cell] = []

    def push(self, item: Cell) -> None:
        self._q.append(item)

    def pop(self) -> Cell:
        return self._q.pop()

    def __len__(self) -> int:
        return len(self._q)

    def __bool__(self) -> bool:
        return bool(self._q)


def graph_search(
    grid: OccupancyGrid,
    start: Cell,
    goal: Cell,
    frontier,
) -> tuple[list[Cell], list[Cell]]:
    frontier.push(start)
    came: dict[Cell, Cell | None] = {start: None}
    expanded: list[Cell] = []
    while frontier:
        node = frontier.pop()
        expanded.append(node)
        if node == goal:
            break
        for nbr in grid.neighbors(node):
            if nbr not in came:
                came[nbr] = node
                frontier.push(nbr)
    return reconstruct(came, start, goal), expanded


def bfs(grid, start, goal):
    return graph_search(grid, start, goal, QueueFrontier())


def dfs(grid, start, goal):
    return graph_search(grid, start, goal, StackFrontier())
