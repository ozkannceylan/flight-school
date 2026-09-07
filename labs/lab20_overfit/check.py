"""CHECK — Lab 20. Runs in <5 s."""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

from flightlab.checks import Criterion, assert_true, run_table
from flightlab.learning import sine_dataset
from flightlab.resolve import ROOT, _load_file

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

LAB_DIR = Path(__file__).resolve().parent
HINTS = [
    "Normal equations with λI, but leave I[0,0]=0 so the intercept is free.",
    "MSE is mean (Φw − y)² on whichever split you pass.",
    "Gap = (val − train) / (val + train). No L2: large. With L2: under 0.18.",
]


def load_impl(*, reference: bool):
    if reference:
        return importlib.import_module("reference.lab20_overfit")
    return _load_file(LAB_DIR / "lab.py", "lab20_student_check")


def criteria(impl) -> list[Criterion]:
    xtr, ytr, xva, yva = sine_dataset(n_train=8, n_val=30, seed=0, noise=0.10)
    Ptr, Pva = impl.poly_features(xtr, 8), impl.poly_features(xva, 8)

    def gap_induced():
        w = impl.fit_poly(Ptr, ytr, l2=0.0)
        tr, va = impl.mse(Ptr, ytr, w), impl.mse(Pva, yva, w)
        gap = impl.relative_gap(tr, va)
        assert_true(gap > 0.50, f"unregularised gap {gap:.2f} (need >0.50) train={tr:.3f} val={va:.3f}")

    def gap_closed():
        w = impl.fit_poly(Ptr, ytr, l2=0.4)
        tr, va = impl.mse(Ptr, ytr, w), impl.mse(Pva, yva, w)
        gap = impl.relative_gap(tr, va)
        assert_true(gap < 0.18, f"L2 gap {gap:.2f} (need <0.18) train={tr:.3f} val={va:.3f}")
        assert_true(va < 0.5, f"val MSE {va:.3f} still huge — λ too big or solve wrong")

    return [
        Criterion("tiny data + high degree induces a train/val gap", gap_induced, HINTS[2]),
        Criterion("L2 closes the gap to <0.18", gap_closed, HINTS[0]),
    ]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Lab 20 checks")
    p.add_argument("--reference", action="store_true")
    p.add_argument("--hints", action="store_true")
    args = p.parse_args(argv)
    if args.hints:
        print("LAB 20 hints")
        for i, h in enumerate(HINTS, 1):
            print(f"  {i}. {h}")
        return 0
    impl = load_impl(reference=args.reference)
    src = "reference" if args.reference else "lab.py"
    report = run_table(f"LAB 20 — When Fitting Better Means Knowing Less  ({src})", criteria(impl))
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
