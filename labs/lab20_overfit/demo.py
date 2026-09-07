"""SEE IT — diverging curves, then L2. media/lab20_thumb.png."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from flightlab.learning import sine_dataset
from flightlab.resolve import get
from flightlab.viz import MEDIA, ensure_media, learning_curves_figure


def _curve(impl, Phi_tr, y_tr, Phi_va, y_va, l2, steps=40, lr=0.08):
    """GD path so the gif has a curve, not a single point."""
    w = np.zeros(Phi_tr.shape[1])
    tr, va = [], []
    I = np.eye(w.size)
    I[0, 0] = 0.0
    for _ in range(steps):
        r = Phi_tr @ w - y_tr.reshape(-1)
        g = (Phi_tr.T @ r) / len(y_tr) + l2 * (I @ w)
        w = w - lr * g
        tr.append(impl.mse(Phi_tr, y_tr, w))
        va.append(impl.mse(Phi_va, y_va, w))
    return np.asarray(tr), np.asarray(va)


def main() -> Path:
    impl = get("lab20")
    xtr, ytr, xva, yva = sine_dataset(n_train=8, n_val=30, seed=0, noise=0.10)
    Ptr, Pva = impl.poly_features(xtr, 8), impl.poly_features(xva, 8)
    tr0, va0 = _curve(impl, Ptr, ytr, Pva, yva, l2=0.0)
    tr1, va1 = _curve(impl, Ptr, ytr, Pva, yva, l2=0.4)
    ensure_media()
    dest = learning_curves_figure(tr0, va0, tr1, va1, path=MEDIA / "lab20_thumb.png")
    print(f"wrote {dest}")
    return dest


if __name__ == "__main__":
    main()
