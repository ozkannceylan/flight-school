"""CHECK — Lab 23. Runs in <5 s."""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

import numpy as np

from flightlab.checks import Criterion, assert_true, run_table
from flightlab.render import (
    IMG_H,
    IMG_W,
    analytic_flow,
    blank,
    default_K,
    render_ground,
    sample_track_points,
    wavy,
)
from flightlab.resolve import ROOT, _load_file, get

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

LAB_DIR = Path(__file__).resolve().parent
HINTS = [
    "Return a markdown string. Paste the four paths from REQUIRED_CITATIONS verbatim.",
    "np.gradient(I) is (Iy, Ix). Energy is mean hypot(Ix, Iy).",
    "If energy is low, return None. Do not invent a velocity from a singular G.",
    "The old assumption is 'LK always outputs a flow'. On blank, that error is large.",
]

REQUIRED = (
    "labs/lab11_bayes/check.py",
    "labs/lab17_optical_flow/check.py",
    "labs/lab21_cnn/check.py",
    "labs/lab22_rl/README.md",
)


def load_impl(*, reference: bool):
    if reference:
        return importlib.import_module("reference.lab23_red_team")
    return _load_file(LAB_DIR / "lab.py", "lab23_student_check")


def criteria(impl) -> list[Criterion]:
    K = default_K()
    py, pz, th, dpy = 0.0, 1.5, 0.0, 0.012
    I_w1 = render_ground(py, pz, th, texture=wavy)
    I_w2 = render_ground(py + dpy, pz, th, texture=wavy)
    I_b1 = render_ground(py, pz, th, texture=blank)
    I_b2 = render_ground(py + dpy, pz, th, texture=blank)
    pts = sample_track_points(IMG_W, IMG_H, n=25, margin=16)
    gt = analytic_flow(K, py, pz, th, dpy, 0.0, 0.0, pts)
    lab17 = get("lab17")

    def analysis_cites():
        text = impl.failure_analysis()
        assert_true(isinstance(text, str) and len(text) >= 600, f"analysis is {len(text) if isinstance(text, str) else type(text)} chars (need ≥600)")
        missing = [p for p in REQUIRED if p not in text]
        assert_true(not missing, f"missing citations: {missing}")
        low = text.lower()
        assert_true(
            any(w in low for w in ("safety", "liability", "refuse", "assumption")),
            "name the stake: safety, liability, refuse, or assumption",
        )

    def old_assumption_red():
        fl = lab17.lucas_kanade(I_b1, I_b2, pts, win=6)
        err = float(np.nanmean(np.linalg.norm(fl - gt, axis=1)))
        assert_true(err > 0.6, f"blank LK error {err:.3f} should be large (old assumption is red)")

    def mitigation_green():
        e_w = impl.texture_energy(I_w1)
        e_b = impl.texture_energy(I_b1)
        assert_true(e_w > 4.0 * e_b + 0.02, f"wavy energy {e_w:.4f} vs blank {e_b:.4f}")
        refused = impl.trusted_flow(I_b1, I_b2, pts)
        assert_true(refused is None, f"blank must return None, got {type(refused)}")
        trusted = impl.trusted_flow(I_w1, I_w2, pts)
        assert_true(trusted is not None, "wavy must return a flow")
        err = float(np.nanmean(np.linalg.norm(np.asarray(trusted) - gt, axis=1)))
        assert_true(err < 0.45, f"trusted wavy flow error {err:.3f}")

    return [
        Criterion("written analysis cites the four lab artifacts", analysis_cites, HINTS[0]),
        Criterion("old assumption (always-trust LK) is red on blank", old_assumption_red, HINTS[3]),
        Criterion("mitigation refuses blank and trusts wavy", mitigation_green, HINTS[2]),
    ]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Lab 23 checks")
    p.add_argument("--reference", action="store_true")
    p.add_argument("--hints", action="store_true")
    args = p.parse_args(argv)
    if args.hints:
        print("LAB 23 hints")
        for i, h in enumerate(HINTS, 1):
            print(f"  {i}. {h}")
        return 0
    impl = load_impl(reference=args.reference)
    src = "reference" if args.reference else "lab.py"
    report = run_table(f"LAB 23 — Red-Team Your Own Stack  ({src})", criteria(impl))
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
