"""CHECK — Lab 09. Runs in <5 s."""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

from flightlab.checks import Criterion, assert_true, run_table
from flightlab.dynamics import PlanarQuadrotor
from flightlab.resolve import ROOT, _load_file

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

LAB_DIR = Path(__file__).resolve().parent
HINTS = [
    "peak = max |u| over both rotors and all times.",
    "scale multiplies DURATIONS. get('lab08').sample_flat_traj(..., scale=scale).",
    "Binary search: if peak≤u_max the scale is feasible (try faster / smaller).",
    "5% faster means scale * 0.95. That one should break the bound.",
]


def load_impl(*, reference: bool):
    if reference:
        return importlib.import_module("reference.lab09_time_scaling")
    return _load_file(LAB_DIR / "lab.py", "lab09_student_check")


def criteria(impl) -> list[Criterion]:
    plant = PlanarQuadrotor()
    # Tight enough that the nominal scale=1 is comfortable but not infinitely so.
    u_max = 0.72 * plant.m * plant.g  # per rotor; hover is 0.5 mg

    def peak_ok():
        us = __import__("numpy").array([[1.0, 2.0], [0.5, -3.0]])
        assert_true(abs(impl.peak_rotor(us) - 3.0) < 1e-12, f"got {impl.peak_rotor(us)}")

    def feasible_at_star():
        s = impl.min_feasible_scale(plant, u_max)
        _, _, us = impl.sample_scaled(plant, s)
        pk = impl.peak_rotor(us)
        assert_true(pk <= u_max + 1e-6, f"scale={s:.3f} peak={pk:.3f} > u_max={u_max:.3f}")
        assert_true(0.4 <= s <= 2.4, f"scale {s:.3f} left the search window")

    def faster_violates():
        s = impl.min_feasible_scale(plant, u_max)
        _, _, us = impl.sample_scaled(plant, 0.95 * s)
        pk = impl.peak_rotor(us)
        assert_true(pk > u_max, f"0.95×scale peak {pk:.3f} should exceed {u_max:.3f}")

    return [
        Criterion("TODO 1 — peak_rotor is max |u|", peak_ok, HINTS[0]),
        Criterion("TODO 2+3 — min scale stays inside u_max", feasible_at_star, HINTS[2]),
        Criterion("5% faster scaling violates the bound", faster_violates, HINTS[3]),
    ]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Lab 09 checks")
    p.add_argument("--reference", action="store_true")
    p.add_argument("--hints", action="store_true")
    args = p.parse_args(argv)
    if args.hints:
        print("LAB 09 hints")
        for i, h in enumerate(HINTS, 1):
            print(f"  {i}. {h}")
        return 0
    impl = load_impl(reference=args.reference)
    src = "reference" if args.reference else "lab.py"
    report = run_table(f"LAB 09 — Time Is the Free Variable  ({src})", criteria(impl))
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
