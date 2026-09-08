"""CHECK — Lab 05. Runs in <5 s."""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

from flightlab.checks import Criterion, assert_true, run_table
from flightlab.resolve import ROOT, _load_file
from flightlab.worlds import maze_lab05

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

LAB_DIR = Path(__file__).resolve().parent
HINTS = [
    "Queue: append / popleft. That's BFS.",
    "Stack: append / pop. That's DFS.",
    "Mark on enqueue (came_from[nbr]=node) so you don't push twice. reconstruct() is provided.",
    "BFS on a 4-connected unit grid is shortest (edge count). DFS has no such promise.",
]


def load_impl(*, reference: bool):
    if reference:
        return importlib.import_module("reference.lab05_search_visualized")
    return _load_file(LAB_DIR / "lab.py", "lab05_student_check")


def criteria(impl) -> list[Criterion]:
    grid, start, goal = maze_lab05()

    def fifo():
        q = impl.QueueFrontier()
        q.push((0, 0))
        q.push((0, 1))
        assert_true(q.pop() == (0, 0), "QueueFrontier should be FIFO")

    def lifo():
        s = impl.StackFrontier()
        s.push((0, 0))
        s.push((0, 1))
        assert_true(s.pop() == (0, 1), "StackFrontier should be LIFO")

    def bfs_optimal():
        path, expanded = impl.bfs(grid, start, goal)
        assert_true(path[:1] == [start] and path[-1:] == [goal], "BFS path must run start→goal")
        # Independent BFS for the known optimum (edge count).
        from reference.lab05_search_visualized import bfs as bfs_ref

        opt, _ = bfs_ref(grid, start, goal)
        assert_true(len(path) == len(opt), f"BFS length {len(path)-1} edges, need {len(opt)-1}")
        assert_true(len(expanded) > 0, "log the expansion list")

    def dfs_not_shorter():
        bpath, bexp = impl.bfs(grid, start, goal)
        dpath, dexp = impl.dfs(grid, start, goal)
        assert_true(dpath[:1] == [start] and dpath[-1:] == [goal], "DFS must also reach G")
        assert_true(len(dpath) >= len(bpath), f"DFS {len(dpath)-1} edges < BFS {len(bpath)-1}")
        assert_true(len(dexp) > 0 and len(bexp) > 0, "both searches must log expansions")

    return [
        Criterion("TODO 1 — QueueFrontier is FIFO", fifo, HINTS[0]),
        Criterion("TODO 2 — StackFrontier is LIFO", lifo, HINTS[1]),
        Criterion("TODO 3 — BFS path length == known optimum", bfs_optimal, HINTS[2]),
        Criterion("DFS path ≥ BFS; expansions logged", dfs_not_shorter, HINTS[3]),
    ]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Lab 05 checks")
    p.add_argument("--reference", action="store_true")
    p.add_argument("--hints", action="store_true")
    args = p.parse_args(argv)
    if args.hints:
        print("LAB 05 hints")
        for i, h in enumerate(HINTS, 1):
            print(f"  {i}. {h}")
        return 0
    impl = load_impl(reference=args.reference)
    src = "reference" if args.reference else "lab.py"
    report = run_table(f"LAB 05 — Search, Visualized  ({src})", criteria(impl))
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
