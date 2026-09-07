"""SEE IT — three paths on a contour. media/lab19_thumb.png."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from flightlab.resolve import get
from flightlab.viz import MEDIA, descent_figure, ensure_media


def _path(step_fn, n=60):
    w = np.array([-0.5, 1.0], dtype=float)
    out = [w.copy()]
    for i in range(n):
        w = step_fn(w, i)
        out.append(np.asarray(w, dtype=float).copy())
    return np.stack(out)


def main() -> Path:
    impl = get("lab19")
    sgd = _path(lambda w, _i: impl.sgd_step(w, impl.grad(w), 0.02), 70)
    v = np.zeros(2)

    def mom(w, _i):
        nonlocal v
        w, v = impl.momentum_step(w, impl.grad(w), v, 0.015)
        return w

    m = np.zeros(2)
    va = np.zeros(2)

    def adam(w, i):
        nonlocal m, va
        w, m, va = impl.adam_step(w, impl.grad(w), m, va, i + 1, 0.05)
        return w

    ensure_media()
    dest = descent_figure(
        [("SGD", sgd), ("momentum", _path(mom, 50)), ("Adam", _path(adam, 40))],
        path=MEDIA / "lab19_thumb.png",
    )
    print(f"wrote {dest}  cliff lr={impl.first_divergent_lr(np.array([0.01,0.03,0.08,0.2,1.0]))}")
    return dest


if __name__ == "__main__":
    main()
