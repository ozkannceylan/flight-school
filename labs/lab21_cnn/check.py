"""CHECK — Lab 21. Runs in <5 s. NumPy default; BACKEND=torch is optional."""

from __future__ import annotations

import argparse
import importlib
import os
import sys
from pathlib import Path

import numpy as np

from flightlab.checks import Criterion, assert_true, run_table
from flightlab.learning import gate_dataset
from flightlab.resolve import ROOT, _load_file

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

LAB_DIR = Path(__file__).resolve().parent
HINTS = [
    "Valid conv: for each filter and offset, sum(patch * kernel).",
    "ReLU conv, mean over filters+rows, argmax over width, then +1 (valid-conv shift).",
    "CNN and MLP should have about the same number of scalars.",
    "A vertical-bar dataset rewards a vertical-edge filter. Look at |∇kernel|.",
]


def load_impl(*, reference: bool):
    if reference:
        return importlib.import_module("reference.lab21_cnn")
    return _load_file(LAB_DIR / "lab.py", "lab21_student_check")


def _pool8(x):
    # 24→8 by 3×3 average — ~65 MLP params vs ~59 CNN.
    n, h, w = x.shape
    return x.reshape(n, 8, h // 8, 8, w // 8).mean(axis=(2, 4))


def _train_cnn(impl, x, y, steps=50, lr=0.08, seed=0):
    rng = np.random.default_rng(seed)
    conv_w = 0.3 * rng.normal(size=(4, 3, 3))
    conv_w[0] += np.array([[-1.0, 0.0, 1.0], [-1.0, 0.0, 1.0], [-1.0, 0.0, 1.0]])
    # width after valid 3×3 on 24 is 22
    fc_w = 0.05 * rng.normal(size=22)
    fc_b = 12.0
    for _ in range(steps):
        pre = impl.conv2d(x, conv_w)
        h = np.maximum(pre, 0.0)
        energy = h.mean(axis=(1, 2))
        fc_w, fc_b = impl.train_readout(energy, y, fc_w, fc_b, lr)
        yhat = energy @ fc_w + fc_b
        err = (2.0 / len(y)) * (yhat - y)
        dE = err[:, None] * fc_w[None, :]
        n, f, oh, ow = pre.shape
        dh = np.broadcast_to(dE[:, None, None, :] / (f * oh), pre.shape).copy()
        dh *= pre > 0
        dw = np.zeros_like(conv_w)
        for fi in range(f):
            for i in range(oh):
                for j in range(ow):
                    dw[fi] += np.mean(x[:, i : i + 3, j : j + 3] * dh[:, fi, i, j][:, None, None], axis=0)
        conv_w = conv_w - 0.3 * lr * dw
    return conv_w, fc_w, fc_b


def _train_mlp(impl, x, y, steps=50, lr=0.08, seed=1):
    xs = _pool8(x)
    flat = xs.reshape(len(x), -1)
    rng = np.random.default_rng(seed)
    w = 0.05 * rng.normal(size=flat.shape[1])
    b = 0.0
    for _ in range(steps):
        w, b = impl.train_readout(flat, y, w, b, lr)
    return w, b


def criteria(impl) -> list[Criterion]:
    x, y = gate_dataset(n=80, size=24, seed=0)
    xte, yte = gate_dataset(n=40, size=24, seed=99)
    # Hold out right-side gates so a memorising MLP cannot cheat.
    tr = y < 16
    x, y = x[tr], y[tr]
    te = yte >= 10
    xte, yte = xte[te], yte[te]

    def conv_ok():
        xx = np.ones((2, 4, 4))
        ww = np.zeros((1, 2, 2))
        ww[0, 0, 0] = 1.0
        out = impl.conv2d(xx, ww)
        assert_true(out.shape == (2, 1, 3, 3), f"shape {out.shape}")
        assert_true(abs(float(out[0, 0, 0, 0]) - 1.0) < 1e-9, "valid conv of ones")

    def cnn_beats_mlp():
        conv_w, fc_w, fc_b = _train_cnn(impl, x, y)
        mw, mb = _train_mlp(impl, x, y)
        pc = impl.n_params_cnn(conv_w, fc_w, np.array([fc_b]))
        pm = impl.n_params_mlp(mw, np.array([mb]))
        assert_true(abs(pc - pm) / max(pm, 1) < 0.35, f"param counts CNN {pc} vs MLP {pm}")
        pred_c = impl.cnn_forward(xte, conv_w, fc_w, fc_b)
        pred_m = impl.mlp_forward(_pool8(xte), mw, mb)
        acc_c = float(np.mean(np.abs(pred_c - yte) < 2.5))
        acc_m = float(np.mean(np.abs(pred_m - yte) < 2.5))
        assert_true(acc_c > acc_m, f"CNN acc {acc_c:.2f} ≤ MLP {acc_m:.2f}")
        assert_true(acc_c > 0.55, f"CNN acc {acc_c:.2f} is weak")

    def filters_edgy():
        conv_w, *_ = _train_cnn(impl, x, y, steps=40)
        # spatial gradient energy vs a random Gaussian kernel
        g = np.mean(np.abs(np.diff(conv_w, axis=1))) + np.mean(np.abs(np.diff(conv_w, axis=2)))
        rnd = 0.3 * np.random.default_rng(0).normal(size=conv_w.shape)
        gr = np.mean(np.abs(np.diff(rnd, axis=1))) + np.mean(np.abs(np.diff(rnd, axis=2)))
        assert_true(g > 1.15 * gr, f"filter edge energy {g:.3f} vs random {gr:.3f}")

    return [
        Criterion("TODO 1 — valid conv2d shape and value", conv_ok, HINTS[0]),
        Criterion("CNN accuracy > param-matched MLP", cnn_beats_mlp, HINTS[2]),
        Criterion("first-layer filters look like edges", filters_edgy, HINTS[3]),
    ]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Lab 21 checks")
    p.add_argument("--reference", action="store_true")
    p.add_argument("--hints", action="store_true")
    args = p.parse_args(argv)
    if args.hints:
        print("LAB 21 hints")
        for i, h in enumerate(HINTS, 1):
            print(f"  {i}. {h}")
        return 0
    if os.environ.get("BACKEND", "numpy").lower() == "torch":
        try:
            import torch  # noqa: F401
        except ImportError:
            print("BACKEND=torch requested but torch is not installed; using NumPy.")
            os.environ["BACKEND"] = "numpy"
    impl = load_impl(reference=args.reference)
    src = "reference" if args.reference else "lab.py"
    report = run_table(f"LAB 21 — Weight Sharing Earns Its Keep  ({src})", criteria(impl))
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
