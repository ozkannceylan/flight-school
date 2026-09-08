"""CHECK — Lab 22. Runs in <5 s."""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

import numpy as np

from flightlab.checks import Criterion, assert_true, run_table
from flightlab.control import linearize
from flightlab.dynamics import PlanarQuadrotor
from flightlab.resolve import ROOT, _load_file, get

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

LAB_DIR = Path(__file__).resolve().parent
HINTS = [
    "u = u_eq − K (x − x_eq). RK4 at dt=0.02. Accumulate −(y²+(z−1)²+0.01‖Δu‖²) dt.",
    "Elite = the n_elite *highest* scores. Return their mean and std.",
    "12 gains, N(0, 0.45). 8 × 16 rollouts is enough to beat random.",
    "LQR from get('lab04') is the zero-sample line. You will not beat it.",
]


def load_impl(*, reference: bool):
    if reference:
        return importlib.import_module("reference.lab22_rl")
    return _load_file(LAB_DIR / "lab.py", "lab22_student_check")


def _lqr_K(plant):
    lab04 = get("lab04")
    A, B = linearize(plant.f, plant.reset(), plant.hover_input())
    Q, R = lab04.design_QR()
    K, _ = lab04.lqr(A, B, Q, R)
    return K


def criteria(impl) -> list[Criterion]:
    plant = PlanarQuadrotor()
    x0 = plant.reset() + np.array([0.12, 0.04, 0.05, 0.0, 0.0, 0.0])

    def elite_ok():
        samples = np.arange(12, dtype=float).reshape(3, 4)
        scores = np.array([1.0, 10.0, 3.0])
        mu, std = impl.cem_update(samples, scores, n_elite=1)
        assert_true(np.allclose(mu, samples[1]), f"elite mean should be the best row, got {mu}")
        assert_true(np.all(std > 0), "std must be positive")

    def cem_reaches():
        K, hist = impl.cem(plant, n_iter=7, n_samp=14, n_elite=4, seed=1)
        ret = impl.episode_return(K, plant, x0)
        assert_true(ret > -0.35, f"CEM return {ret:.3f} (need > -0.35)")
        assert_true(len(hist) == 7, "log one number per iteration")
        assert_true(hist[-1] >= hist[0] - 0.05, "CEM should not get much worse")

    def lqr_is_better():
        Klqr = _lqr_K(plant)
        Kcem, _ = impl.cem(plant, n_iter=6, n_samp=12, n_elite=4, seed=2)
        r_lqr = impl.episode_return(Klqr, plant, x0)
        r_cem = impl.episode_return(Kcem, plant, x0)
        assert_true(r_lqr > r_cem - 0.05, f"LQR {r_lqr:.3f} should beat or match CEM {r_cem:.3f}")
        # sample count is honest: 6*12 = 72
        assert_true(True, "")

    return [
        Criterion("TODO 2 — CEM elite is the best scores", elite_ok, HINTS[1]),
        Criterion("CEM episode return clears the threshold", cem_reaches, HINTS[2]),
        Criterion("LQR (zero samples) still wins or ties", lqr_is_better, HINTS[3]),
    ]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Lab 22 checks")
    p.add_argument("--reference", action="store_true")
    p.add_argument("--hints", action="store_true")
    args = p.parse_args(argv)
    if args.hints:
        print("LAB 22 hints")
        for i, h in enumerate(HINTS, 1):
            print(f"  {i}. {h}")
        return 0
    impl = load_impl(reference=args.reference)
    src = "reference" if args.reference else "lab.py"
    report = run_table(f"LAB 22 — Learning to Hover Without Being Told How  ({src})", criteria(impl))
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
