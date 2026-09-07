"""CHECK — Lab 18. Runs in <5 s."""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

import numpy as np

from flightlab.checks import Criterion, assert_true, run_table
from flightlab.dynamics import PlanarQuadrotor
from flightlab.integrate import rollout
from flightlab.learning import lqr_policy_dataset
from flightlab.resolve import ROOT, _load_file

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

LAB_DIR = Path(__file__).resolve().parent
HINTS = [
    "h = relu(x W1 + b1), y = h W2 + b2. Cache x, z1, h for backward.",
    "dL/dy = 2(yhat−y)/yhat.size (mean over every entry). Chain through W2, then the ReLU mask.",
    "Finite differences: nudge one weight by 1e-5, compare ΔL/ε to your grad.",
    "Train 400 steps on the LQR dataset, then close the loop. It should hover.",
]


def load_impl(*, reference: bool):
    if reference:
        return importlib.import_module("reference.lab18_mlp")
    return _load_file(LAB_DIR / "lab.py", "lab18_student_check")


def _train(impl, xs, us, steps=700, lr=0.25, seed=0):
    rng = np.random.default_rng(seed)
    p = impl.init_params(rng)
    for _ in range(steps):
        yhat, cache = impl.forward(xs, p["W1"], p["b1"], p["W2"], p["b2"])
        g = impl.backward(yhat, us, cache)
        p = impl.gd_step(p, g, lr)
    return p


def criteria(impl) -> list[Criterion]:
    rng = np.random.default_rng(2)
    x = rng.normal(size=(12, 6))
    y = rng.normal(size=(12, 2))
    p = impl.init_params(rng)

    def grads_match():
        yhat, cache = impl.forward(x, p["W1"], p["b1"], p["W2"], p["b2"])
        g = impl.backward(yhat, y, cache)
        eps = 1e-5
        for key, idx in (("W2", (0, 0)), ("b2", (0,)), ("W1", (1, 2)), ("b1", (3,))):
            pert = p[key].copy()
            pert[idx] += eps
            kw = {**{k: p[k] for k in ("W1", "b1", "W2", "b2")}, key: pert}
            y2, _ = impl.forward(x, kw["W1"], kw["b1"], kw["W2"], kw["b2"])
            y0, _ = impl.forward(x, p["W1"], p["b1"], p["W2"], p["b2"])
            fd = (impl.mse(y2, y) - impl.mse(y0, y)) / eps
            an = float(np.asarray(g[key])[idx])
            assert_true(abs(fd - an) < 1e-4, f"{key}{idx} fd={fd:.3e} analytic={an:.3e}")

    def policy_hovers():
        xs, us = lqr_policy_dataset(120, seed=3)
        p = _train(impl, xs, us)
        plant = PlanarQuadrotor()
        x_eq = plant.reset()

        def pi(x, _t):
            yhat, _ = impl.forward(x.reshape(1, -1), p["W1"], p["b1"], p["W2"], p["b2"])
            return yhat.reshape(-1)

        x0 = x_eq + np.array([0.08, 0.05, 0.04, 0, 0, 0])
        _, xs_r, _ = rollout(plant.f, x0, dt=0.03, t_end=2.4, policy=pi)
        assert_true(np.max(np.abs(xs_r[-8:, 0])) < 0.12, f"final |y| {np.max(np.abs(xs_r[-8:,0])):.3f}")
        assert_true(np.max(np.abs(xs_r[-8:, 1] - 1.0)) < 0.18, f"final |z-1| {np.max(np.abs(xs_r[-8:,1]-1)):.3f}")

    return [
        Criterion("analytic grads match finite differences", grads_match, HINTS[2]),
        Criterion("learned policy stabilizes a hover nudge", policy_hovers, HINTS[3]),
    ]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Lab 18 checks")
    p.add_argument("--reference", action="store_true")
    p.add_argument("--hints", action="store_true")
    args = p.parse_args(argv)
    if args.hints:
        print("LAB 18 hints")
        for i, h in enumerate(HINTS, 1):
            print(f"  {i}. {h}")
        return 0
    impl = load_impl(reference=args.reference)
    src = "reference" if args.reference else "lab.py"
    report = run_table(f"LAB 18 — An MLP You Can Read  ({src})", criteria(impl))
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
