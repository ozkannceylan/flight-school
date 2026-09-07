"""CHECK — Lab 11. Runs in <5 s."""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

import numpy as np

from flightlab.checks import Criterion, assert_true, run_table
from flightlab.resolve import ROOT, _load_file
from flightlab.worlds import corridor_lab11

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

LAB_DIR = Path(__file__).resolve().parent
HINTS = [
    "predict is a convolution: stay or step +1, clip at n-1, then renormalize.",
    "p(z=door | door)=p_hit, p(z=door | empty)=p_false. Multiply, divide by the sum.",
    "After eight door/empty observations the mode should sit on the true cell.",
    "Swap p_hit and p_false. The filter gets confident about the wrong cells.",
]


def load_impl(*, reference: bool):
    if reference:
        return importlib.import_module("reference.lab11_bayes")
    return _load_file(LAB_DIR / "lab.py", "lab11_student_check")


def _run(impl, like_fn, n_obs: int = 8):
    doors, x0 = corridor_lab11()
    n = doors.size
    bel = np.full(n, 1.0 / n)
    x = x0
    rng = np.random.default_rng(2)
    for _ in range(n_obs):
        # truth: step +1 if possible (deterministic walk)
        x = min(x + 1, n - 1)
        # sensor: mostly correct
        z = bool(doors[x]) if rng.random() < 0.92 else (not bool(doors[x]))
        bel = impl.predict(bel)
        like = like_fn(doors, z)
        bel = impl.update(bel, like)
    return bel, x


def criteria(impl) -> list[Criterion]:
    doors, _ = corridor_lab11()

    def sums_to_one():
        n = doors.size
        bel = np.full(n, 1.0 / n)
        bel = impl.predict(bel)
        assert_true(abs(float(bel.sum()) - 1.0) < 1e-9, f"predict sum {bel.sum()}")
        like = impl.likelihood(doors, True)
        bel = impl.update(bel, like)
        assert_true(abs(float(bel.sum()) - 1.0) < 1e-9, f"update sum {bel.sum()}")
        assert_true(np.all(bel >= -1e-12), "negative mass")

    def converges():
        bel, x = _run(impl, impl.likelihood, 8)
        mode = int(np.argmax(bel))
        assert_true(mode == x, f"mode {mode} vs truth {x}; mass={bel[x]:.3f}")
        assert_true(bel[x] > 0.25, f"truth mass {bel[x]:.3f} is weak")

    def confident_wrong():
        bel, x = _run(impl, impl.inverted_likelihood, 8)
        mode = int(np.argmax(bel))
        assert_true(mode != x, f"inverted model still peaked at truth {x}")
        assert_true(float(bel.max()) > 0.25, f"max mass {bel.max():.3f} — not confident enough")

    return [
        Criterion("posterior (and predict) sums to 1", sums_to_one, HINTS[0]),
        Criterion("converges to the true cell within 8 observations", converges, HINTS[2]),
        Criterion("wrong sensor model is confident-and-wrong", confident_wrong, HINTS[3]),
    ]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Lab 11 checks")
    p.add_argument("--reference", action="store_true")
    p.add_argument("--hints", action="store_true")
    args = p.parse_args(argv)
    if args.hints:
        print("LAB 11 hints")
        for i, h in enumerate(HINTS, 1):
            print(f"  {i}. {h}")
        return 0
    impl = load_impl(reference=args.reference)
    src = "reference" if args.reference else "lab.py"
    report = run_table(f"LAB 11 — Prior, Likelihood, Posterior  ({src})", criteria(impl))
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
