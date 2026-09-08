"""Reference implementation for Lab 19 — The Shape of the Descent."""

from __future__ import annotations

import numpy as np


def loss(w: np.ndarray) -> float:
    w = np.asarray(w, dtype=float).reshape(2)
    return float((w[0] - 1.0) ** 2 + 25.0 * (w[1] + 0.5) ** 2)


def grad(w: np.ndarray) -> np.ndarray:
    w = np.asarray(w, dtype=float).reshape(2)
    return np.array([2.0 * (w[0] - 1.0), 50.0 * (w[1] + 0.5)], dtype=float)


def sgd_step(w: np.ndarray, g: np.ndarray, lr: float) -> np.ndarray:
    return np.asarray(w, dtype=float) - lr * np.asarray(g, dtype=float)


def momentum_step(w: np.ndarray, g: np.ndarray, v: np.ndarray, lr: float, beta: float = 0.8):
    v = beta * np.asarray(v, dtype=float) + np.asarray(g, dtype=float)
    w = np.asarray(w, dtype=float) - lr * v
    return w, v


def adam_step(
    w: np.ndarray,
    g: np.ndarray,
    m: np.ndarray,
    v: np.ndarray,
    t: int,
    lr: float,
    b1: float = 0.9,
    b2: float = 0.999,
    eps: float = 1e-8,
):
    g = np.asarray(g, dtype=float)
    m = b1 * np.asarray(m, dtype=float) + (1.0 - b1) * g
    v = b2 * np.asarray(v, dtype=float) + (1.0 - b2) * (g * g)
    mh = m / (1.0 - b1**t)
    vh = v / (1.0 - b2**t)
    w = np.asarray(w, dtype=float) - lr * mh / (np.sqrt(vh) + eps)
    return w, m, v


def first_divergent_lr(lrs: np.ndarray, n_steps: int = 40, w0: np.ndarray | None = None) -> float:
    w0 = np.array([0.0, 0.0], dtype=float) if w0 is None else np.asarray(w0, dtype=float)
    L0 = loss(w0)
    for lr in np.sort(np.asarray(lrs, dtype=float)):
        w = w0.copy()
        diverged = False
        for _ in range(n_steps):
            w = sgd_step(w, grad(w), float(lr))
            L = loss(w)
            if (not np.isfinite(L)) or L > max(80.0, 4.0 * L0):
                diverged = True
                break
        if diverged:
            return float(lr)
    return float("inf")
