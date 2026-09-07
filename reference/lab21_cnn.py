"""Reference implementation for Lab 21 — Weight Sharing Earns Its Keep."""

from __future__ import annotations

import os

import numpy as np


def conv2d(x: np.ndarray, w: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    w = np.asarray(w, dtype=float)
    if backend() == "torch":
        try:
            import torch
            import torch.nn.functional as F

            xt = torch.as_tensor(x, dtype=torch.float32)[:, None]
            wt = torch.as_tensor(w, dtype=torch.float32)[:, None]
            return F.conv2d(xt, wt).detach().cpu().numpy()
        except ImportError:
            pass
    n, h, ww = x.shape
    f, kh, kw = w.shape
    oh, ow = h - kh + 1, ww - kw + 1
    out = np.zeros((n, f, oh, ow), dtype=float)
    for fi in range(f):
        for i in range(oh):
            for j in range(ow):
                patch = x[:, i : i + kh, j : j + kw]
                out[:, fi, i, j] = np.sum(patch * w[fi], axis=(1, 2))
    return out


def cnn_forward(x: np.ndarray, conv_w: np.ndarray, fc_w: np.ndarray, fc_b: np.ndarray) -> np.ndarray:
    h = np.maximum(conv2d(x, conv_w), 0.0)
    energy = h.mean(axis=(1, 2))
    return energy.argmax(axis=1).astype(float) + 1.0


def mlp_forward(x: np.ndarray, W: np.ndarray, b: np.ndarray) -> np.ndarray:
    flat = np.asarray(x, dtype=float).reshape(len(x), -1)
    return flat @ W + b


def train_readout(features: np.ndarray, y: np.ndarray, w: np.ndarray, b: np.ndarray, lr: float):
    features = np.asarray(features, dtype=float)
    y = np.asarray(y, dtype=float).reshape(-1)
    yhat = features @ w + b
    n = len(y)
    err = (2.0 / n) * (yhat - y)
    w = w - lr * (features.T @ err)
    b = b - lr * err.sum()
    return w, b


def backend() -> str:
    return os.environ.get("BACKEND", "numpy").strip().lower()


def n_params_cnn(conv_w: np.ndarray, fc_w: np.ndarray, fc_b: np.ndarray) -> int:
    return int(conv_w.size + fc_w.size + fc_b.size)


def n_params_mlp(W: np.ndarray, b: np.ndarray) -> int:
    return int(W.size + b.size)
