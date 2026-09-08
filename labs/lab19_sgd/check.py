"""CHECK — Lab 19. Runs in <5 s."""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

import numpy as np

from flightlab.checks import Criterion, assert_true, run_table
from flightlab.resolve import ROOT, _load_file

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

LAB_DIR = Path(__file__).resolve().parent
HINTS = [
    "SGD is w ← w − lr g.",
    "v ← βv + g, then w ← w − lr v. Classic (not Nesterov).",
    "Adam: m,v EMA; divide by (1−β^t); w ← w − lr m̂ / (√v̂ + ε).",
    "Sweep sorted lrs. The cliff is the first one whose loss exceeds 80 or goes non-finite.",
]


def load_impl(*, reference: bool):
    if reference:
        return importlib.import_module("reference.lab19_sgd")
    return _load_file(LAB_DIR / "lab.py", "lab19_student_check")


def _run(step_fn, n=80, lr=0.02):
    w = np.array([-0.5, 1.0], dtype=float)
    for i in range(n):
        w = step_fn(w, i)
    return w


def criteria(impl) -> list[Criterion]:
    target = np.array([1.0, -0.5])

    def all_three():
        w_s = _run(lambda w, _i: impl.sgd_step(w, impl.grad(w), 0.02), n=120)
        v = np.zeros(2)
        def mom(w, _i):
            nonlocal v
            w, v = impl.momentum_step(w, impl.grad(w), v, 0.015)
            return w
        w_m = _run(mom, n=80)
        m = np.zeros(2)
        va = np.zeros(2)
        def adam(w, i):
            nonlocal m, va
            w, m, va = impl.adam_step(w, impl.grad(w), m, va, i + 1, 0.05)
            return w
        w_a = _run(adam, n=80)
        for name, w in (("SGD", w_s), ("momentum", w_m), ("Adam", w_a)):
            assert_true(impl.loss(w) < 0.05, f"{name} loss {impl.loss(w):.3f} (need <0.05)")
            assert_true(np.linalg.norm(w - target) < 0.25, f"{name} ended at {w}")

    def cliff():
        lrs = np.array([0.001, 0.01, 0.03, 0.08, 0.2, 1.0, 5.0])
        lr = impl.first_divergent_lr(lrs, n_steps=40)
        assert_true(0.03 < lr < 2.0, f"cliff at lr={lr} (expected between 0.08 and 1)")

    return [
        Criterion("SGD, momentum, and Adam all reach the bowl", all_three, HINTS[0]),
        Criterion("lr sweep locates the divergence boundary", cliff, HINTS[3]),
    ]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Lab 19 checks")
    p.add_argument("--reference", action="store_true")
    p.add_argument("--hints", action="store_true")
    args = p.parse_args(argv)
    if args.hints:
        print("LAB 19 hints")
        for i, h in enumerate(HINTS, 1):
            print(f"  {i}. {h}")
        return 0
    impl = load_impl(reference=args.reference)
    src = "reference" if args.reference else "lab.py"
    report = run_table(f"LAB 19 — The Shape of the Descent  ({src})", criteria(impl))
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
