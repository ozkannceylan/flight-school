"""CHECK — Lab 13. Runs in <5 s."""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

import numpy as np

from flightlab.checks import Criterion, assert_true, run_table
from flightlab.geometry import oplus
from flightlab.resolve import ROOT, _load_file
from flightlab.sensors import RangeSensor
from flightlab.worlds import office_lab13, start_pose_lab13

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

LAB_DIR = Path(__file__).resolve().parent
HINTS = [
    "u is (forward, dθ). Noise those two, then oplus(pose, [dx, 0, dθ]).",
    "ẑ = sensor.expected(pose, grid). Product of Gaussians = sum of squares in the exp.",
    "Systematic resample, then overwrite a fraction with uniform_particles.",
    "Without injection the cloud stays at the old room after a teleport.",
]


def load_impl(*, reference: bool):
    if reference:
        return importlib.import_module("reference.lab13_mcl")
    return _load_file(LAB_DIR / "lab.py", "lab13_student_check")


def _path(n: int = 36):
    """Stay in the long hallway (rows 6–7) so the beam signature is unique."""
    pose = start_pose_lab13()
    cmds = [(0.40, 0.0)] * 10 + [(0.0, np.pi)] + [(0.40, 0.0)] * 8
    cmds += [(0.0, 0.4)] * max(0, n - len(cmds))
    poses = [pose.copy()]
    for u in cmds:
        pose = oplus(pose, np.array([u[0], 0.0, u[1]]))
        poses.append(pose.copy())
    return np.asarray(poses), cmds


def _mcl(
    impl,
    grid,
    poses,
    cmds,
    sensor,
    *,
    inject: float,
    kidnap_at: int | None,
    seed: int,
    init: str = "uniform",
):
    rng = np.random.default_rng(seed)
    if init == "tight":
        parts = poses[0] + rng.normal(0.0, [0.12, 0.12, 0.08], size=(180, 3))
    else:
        parts = impl.uniform_particles(180, grid, rng)
    err = []
    clouds = [parts.copy()]
    truth = poses[0].copy()
    kidnapped = False
    for t, u in enumerate(cmds):
        if kidnap_at is not None and t == kidnap_at:
            # Distinctive pose in the right-hand room. After this, spin in place
            # so the beam signature stays put long enough to re-seed.
            truth = np.array([10.5, 2.5, np.pi], dtype=float)
            kidnapped = True
            u = (0.0, 0.35)
        elif kidnapped:
            u = (0.0, 0.35)
            truth = oplus(truth, np.array([u[0], 0.0, u[1]], dtype=float))
        else:
            truth = poses[t + 1].copy()
        z = sensor.measure(truth, grid, rng)
        parts = impl.motion_update(parts, np.asarray(u), rng)
        w = impl.weight(parts, z, grid, sensor)
        parts = impl.resample(parts, w, rng, grid, inject=inject)
        mu = impl.mean_pose(parts)
        err.append(float(np.hypot(mu[0] - truth[0], mu[1] - truth[1])))
        clouds.append(parts.copy())
    return np.asarray(err), clouds, truth


def criteria(impl) -> list[Criterion]:
    grid = office_lab13()
    sensor = RangeSensor(n_beams=5, fov=np.pi, max_range=7.0, sigma=0.12, step=0.25)
    poses, cmds = _path(38)

    def converges():
        late = []
        for seed in (3, 7, 11):
            err, *_ = _mcl(impl, grid, poses, cmds, sensor, inject=0.0, kidnap_at=None, seed=seed)
            late.append(float(np.mean(err[16:28])))
        med = float(np.median(late))
        assert_true(med < 1.8, f"median late error {med:.2f} over seeds {late}")

    def recovers():
        err, *_ = _mcl(impl, grid, poses, cmds, sensor, inject=0.22, kidnap_at=16, seed=8)
        assert_true(err[-1] < 2.2, f"with injection, final error {err[-1]:.2f} (need <2.2)")

    def fails_without():
        err, *_ = _mcl(
            impl, grid, poses, cmds, sensor, inject=0.0, kidnap_at=16, seed=8, init="tight"
        )
        assert_true(err[-1] > 2.4, f"without injection should stay lost, error {err[-1]:.2f}")

    return [
        Criterion("converges from a uniform prior in <40 steps", converges, HINTS[1]),
        Criterion("recovers from kidnapping when injection is on", recovers, HINTS[2]),
        Criterion("fails to recover when injection is off", fails_without, HINTS[3]),
    ]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Lab 13 checks")
    p.add_argument("--reference", action="store_true")
    p.add_argument("--hints", action="store_true")
    args = p.parse_args(argv)
    if args.hints:
        print("LAB 13 hints")
        for i, h in enumerate(HINTS, 1):
            print(f"  {i}. {h}")
        return 0
    impl = load_impl(reference=args.reference)
    src = "reference" if args.reference else "lab.py"
    report = run_table(f"LAB 13 — Known Map, Unknown Pose  ({src})", criteria(impl))
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
