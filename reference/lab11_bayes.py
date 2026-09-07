"""Reference implementation for Lab 11 — Prior, Likelihood, Posterior."""

from __future__ import annotations

import numpy as np


def predict(bel: np.ndarray, p_fwd: float = 0.8, p_stay: float = 0.2) -> np.ndarray:
    bel = np.asarray(bel, dtype=float).reshape(-1)
    n = bel.size
    out = np.zeros(n, dtype=float)
    for i in range(n):
        out[i] += p_stay * bel[i]
        out[min(i + 1, n - 1)] += p_fwd * bel[i]
    s = out.sum()
    return out / s if s > 0 else out


def likelihood(doors: np.ndarray, z_door: bool, p_hit: float = 0.9, p_false: float = 0.2) -> np.ndarray:
    doors = np.asarray(doors, dtype=bool).reshape(-1)
    if z_door:
        return np.where(doors, p_hit, p_false).astype(float)
    return np.where(doors, 1.0 - p_hit, 1.0 - p_false).astype(float)


def update(bel: np.ndarray, like: np.ndarray) -> np.ndarray:
    post = np.asarray(bel, dtype=float).reshape(-1) * np.asarray(like, dtype=float).reshape(-1)
    s = post.sum()
    if s <= 0:
        return np.full_like(post, 1.0 / post.size)
    return post / s


def inverted_likelihood(doors: np.ndarray, z_door: bool, p_hit: float = 0.9, p_false: float = 0.2) -> np.ndarray:
    return likelihood(doors, z_door, p_hit=p_false, p_false=p_hit)
