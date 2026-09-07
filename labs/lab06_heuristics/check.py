"""CHECK — Lab 06. Runs in <5 s."""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

from flightlab.checks import Criterion, assert_true, run_table
from flightlab.resolve import ROOT, _load_file
from flightlab.worlds import manhattan, open_field_lab06, terrain_lab06

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

LAB_DIR = Path(__file__).resolve().parent
HINTS = [
    "heapq with (g, node). Edge cost is enter_cost(v). Mark expanded on first pop.",
    "A* is Dijkstra with priority g+h. Same came_from / reconstruct.",
    "inflate(h, 2) is λ a,b: 2*h(a,b). Admissible h stays optimal; inflated need not.",
    "If A* didn't save expansions, the map is too easy — use terrain_lab06().",
]


def load_impl(*, reference: bool):
    if reference:
        return importlib.import_module("reference.lab06_heuristics")
    return _load_file(LAB_DIR / "lab.py", "lab06_student_check")


def criteria(impl) -> list[Criterion]:
    cmap, start, goal = terrain_lab06()

    def same_cost():
        p_d, e_d, c_d = impl.dijkstra(cmap, start, goal)
        p_a, e_a, c_a = impl.astar(cmap, start, goal, manhattan)
        assert_true(p_d and p_d[-1] == goal, "Dijkstra must reach G")
        assert_true(abs(c_a - c_d) < 1e-9, f"A* cost {c_a} != Dijkstra {c_d}")

    def fewer_expansions():
        field, s, g = open_field_lab06()
        _, e_d, _ = impl.dijkstra(field, s, g)
        _, e_a, _ = impl.astar(field, s, g, manhattan)
        assert_true(
            len(e_a) <= 0.70 * len(e_d),
            f"A* expanded {len(e_a)}, Dijkstra {len(e_d)} (need ≥30% fewer)",
        )

    def inflated_suboptimal():
        _, _, c_d = impl.dijkstra(cmap, start, goal)
        h2 = impl.inflate(manhattan, 2.0)
        _, _, c_w = impl.astar(cmap, start, goal, h2)
        assert_true(c_w > c_d + 1e-9, f"inflated cost {c_w} should beat (exceed) optimal {c_d}")

    return [
        Criterion("TODO 1+2 — admissible A* cost == Dijkstra", same_cost, HINTS[1]),
        Criterion("A* expands ≥30% fewer nodes", fewer_expansions, HINTS[3]),
        Criterion("TODO 3 — inflated h is suboptimal", inflated_suboptimal, HINTS[2]),
    ]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Lab 06 checks")
    p.add_argument("--reference", action="store_true")
    p.add_argument("--hints", action="store_true")
    args = p.parse_args(argv)
    if args.hints:
        print("LAB 06 hints")
        for i, h in enumerate(HINTS, 1):
            print(f"  {i}. {h}")
        return 0
    impl = load_impl(reference=args.reference)
    src = "reference" if args.reference else "lab.py"
    report = run_table(f"LAB 06 — Heuristics, Honest and Otherwise  ({src})", criteria(impl))
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
