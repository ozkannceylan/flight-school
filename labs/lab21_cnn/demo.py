"""SEE IT — the filter grid. media/lab21_thumb.png."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from flightlab.learning import gate_dataset
from flightlab.resolve import get
from flightlab.viz import MEDIA, ensure_media, filter_grid_figure


def main() -> Path:
    impl = get("lab21")
    x, y = gate_dataset(n=80, size=24, seed=0)
    rng = np.random.default_rng(0)
    conv_w = 0.3 * rng.normal(size=(4, 3, 3))
    conv_w[0] += np.array([[-1.0, 0.0, 1.0], [-1.0, 0.0, 1.0], [-1.0, 0.0, 1.0]])
    fc_w = 0.05 * rng.normal(size=22)
    fc_b = 12.0
    lr = 0.08
    for _ in range(40):
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
    ensure_media()
    dest = filter_grid_figure(conv_w, path=MEDIA / "lab21_thumb.png")
    print(f"wrote {dest}  backend={impl.backend()}")
    return dest


if __name__ == "__main__":
    main()
