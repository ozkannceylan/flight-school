"""CHECK — Lab 12. Runs in <5 s."""

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
from flightlab.sensors import H, discrete_hover, hover_dataset

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

LAB_DIR = Path(__file__).resolve().parent
HINTS = [
    "Predict: μ=Aμ, P=APAᵀ+Q. Then μ ← μ + Bu (input is deterministic).",
    "S = HPHᵀ+R, K = PHᵀ S⁻¹, μ ← μ+Ky. Joseph form keeps P SPD.",
    "Each particle: euler(plant.f, x, u, dt) then add N(0,std²).",
    "Systematic: one U[0,1/N] offset, then walk the CDF in 1/N steps.",
]


def load_impl(*, reference: bool):
    if reference:
        return importlib.import_module("reference.lab12_kf_pf")
    return _load_file(LAB_DIR / "lab.py", "lab12_student_check")


def _K(plant):
    lab04 = get("lab04")
    A, B = linearize(plant.f, plant.reset(), plant.hover_input())
    Q, R = lab04.design_QR()
    K, _ = lab04.lqr(A, B, Q, R)
    return K


def _filters(impl, plant, xs, us, zs, dt, *, n_particles=80, seed=0, mu0=None, part_std=0.1):
    Ad, Bd = discrete_hover(plant, dt)
    Q = (0.025**2) * np.eye(6)
    Rmeas = np.diag([0.04, 0.04, 0.03]) ** 2
    mu = np.asarray(xs[0] if mu0 is None else mu0, dtype=float).copy()
    P = (0.1**2) * np.eye(6)
    rng = np.random.default_rng(seed)
    parts = mu + rng.normal(0.0, part_std, size=(n_particles, 6))
    nees_hist = []
    kf_err = []
    pf_err = []
    mus = []
    sigmas = []
    last_parts = parts
    x_eq = plant.reset()
    u_eq = plant.hover_input()
    for i in range(len(xs)):
        if i > 0:
            # Error-state predict about hover: x⁺ = x_eq + A(x−x_eq) + B(u−u_eq)
            dmu, P = impl.kf_predict(mu - x_eq, P, Ad, Q)
            mu = x_eq + dmu + Bd @ (us[i - 1] - u_eq)
            parts = impl.pf_predict(parts, us[i - 1], plant, dt, 0.03, rng)
        mu, P = impl.kf_update(mu, P, H, zs[i], Rmeas)
        w = impl.pf_weights(parts, zs[i], H, Rmeas)
        parts = impl.resample(parts, w, rng)
        P = 0.5 * (P + P.T) + 1e-9 * np.eye(6)
        nees_hist.append(impl.nees(mu, P, xs[i]))
        kf_err.append(np.linalg.norm(mu[:2] - xs[i, :2]))
        pf_err.append(np.linalg.norm(parts[:, :2].mean(axis=0) - xs[i, :2]))
        mus.append(mu.copy())
        sigmas.append(P.copy())
        last_parts = parts
    return (
        np.asarray(nees_hist),
        np.asarray(kf_err),
        np.asarray(pf_err),
        np.asarray(mus),
        np.asarray(sigmas),
        last_parts,
    )


def criteria(impl) -> list[Criterion]:
    plant = PlanarQuadrotor()
    K = _K(plant)
    dt = 0.02
    xs, us, zs = hover_dataset(plant, K, plant.reset(), dt=dt, n=50, seed=3)

    def kf_consistent():
        nees, *_ = _filters(impl, plant, xs, us, zs, dt, seed=3)
        tail = nees[5:]
        m = float(np.mean(tail))
        frac = float(np.mean(tail < 16.8))
        assert_true(1.0 < m < 16.0, f"mean NEES {m:.2f} (want ~6, 95% band)")
        assert_true(frac >= 0.70, f"only {frac:.0%} of NEES inside χ²_6 0.99")

    def pf_tracks():
        _n, _kf_err, pf_err, *_ = _filters(impl, plant, xs, us, zs, dt, seed=3)
        rmse = float(np.sqrt(np.mean(pf_err[5:] ** 2)))
        assert_true(rmse < 0.18, f"PF position RMSE {rmse:.3f} (need <0.18)")

    def kf_breaks_far():
        x0 = np.array([0.55, 1.4, 1.25, 0.0, 0.0, 0.0])
        xs_f, us_f, zs_f = hover_dataset(
            plant, K, x0, dt=dt, n=40, seed=4, closed_loop=False
        )
        _n, kf_err, pf_err, *_ = _filters(
            impl,
            plant,
            xs_f,
            us_f,
            zs_f,
            dt,
            seed=4,
            mu0=plant.reset(),
            part_std=0.55,
        )
        kf_rmse = float(np.sqrt(np.mean(kf_err[8:] ** 2)))
        pf_rmse = float(np.sqrt(np.mean(pf_err[8:] ** 2)))
        assert_true(pf_rmse < 0.35, f"PF should survive, RMSE {pf_rmse:.3f}")
        assert_true(kf_rmse > 1.15 * pf_rmse, f"KF {kf_rmse:.3f} should lose to PF {pf_rmse:.3f}")

    return [
        Criterion("KF NEES in the 95% consistency band", kf_consistent, HINTS[0]),
        Criterion("PF position RMSE below threshold", pf_tracks, HINTS[2]),
        Criterion("far from hover: KF breaks, PF survives", kf_breaks_far, HINTS[2]),
    ]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Lab 12 checks")
    p.add_argument("--reference", action="store_true")
    p.add_argument("--hints", action="store_true")
    args = p.parse_args(argv)
    if args.hints:
        print("LAB 12 hints")
        for i, h in enumerate(HINTS, 1):
            print(f"  {i}. {h}")
        return 0
    impl = load_impl(reference=args.reference)
    src = "reference" if args.reference else "lab.py"
    report = run_table(f"LAB 12 — Two Ways to Carry a Belief  ({src})", criteria(impl))
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
