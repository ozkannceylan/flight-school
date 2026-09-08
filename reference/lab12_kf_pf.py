"""Reference implementation for Lab 12 — Two Ways to Carry a Belief."""

from __future__ import annotations

import numpy as np

from flightlab.dynamics import PlanarQuadrotor
from flightlab.integrate import euler


def kf_predict(mu: np.ndarray, P: np.ndarray, A: np.ndarray, Q: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    mu = np.asarray(A, dtype=float) @ np.asarray(mu, dtype=float).reshape(-1)
    P = np.asarray(A, dtype=float) @ np.asarray(P, dtype=float) @ np.asarray(A, dtype=float).T + np.asarray(
        Q, dtype=float
    )
    return mu, P


def kf_update(
    mu: np.ndarray,
    P: np.ndarray,
    H: np.ndarray,
    z: np.ndarray,
    R: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    mu = np.asarray(mu, dtype=float).reshape(-1)
    P = np.asarray(P, dtype=float)
    H = np.asarray(H, dtype=float)
    z = np.asarray(z, dtype=float).reshape(-1)
    R = np.asarray(R, dtype=float)
    y = z - H @ mu
    S = H @ P @ H.T + R
    K = P @ H.T @ np.linalg.inv(S)
    I = np.eye(mu.size)
    mu = mu + K @ y
    P = (I - K @ H) @ P @ (I - K @ H).T + K @ R @ K.T
    return mu, P


def pf_predict(
    particles: np.ndarray,
    u: np.ndarray,
    plant: PlanarQuadrotor,
    dt: float,
    std: float,
    rng: np.random.Generator,
) -> np.ndarray:
    out = np.empty_like(particles, dtype=float)
    for i, x in enumerate(particles):
        out[i] = euler(plant.f, x, u, dt)
    out = out + rng.normal(0.0, std, size=out.shape)
    return out


def resample(particles: np.ndarray, weights: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    w = np.asarray(weights, dtype=float).reshape(-1)
    w = w / w.sum()
    n = w.size
    cdf = np.cumsum(w)
    u0 = float(rng.uniform(0.0, 1.0 / n))
    idx = np.searchsorted(cdf, u0 + np.arange(n) / n)
    idx = np.clip(idx, 0, n - 1)
    return np.asarray(particles, dtype=float)[idx]


def pf_weights(particles: np.ndarray, z: np.ndarray, H: np.ndarray, R: np.ndarray) -> np.ndarray:
    innov = z.reshape(1, -1) - particles @ H.T
    Rinv = np.linalg.inv(R)
    q = np.sum((innov @ Rinv) * innov, axis=1)
    w = np.exp(-0.5 * (q - q.min()))
    s = w.sum()
    return w / s if s > 0 else np.full(len(w), 1.0 / len(w))


def nees(mu: np.ndarray, P: np.ndarray, x: np.ndarray) -> float:
    e = np.asarray(x, dtype=float).reshape(-1) - np.asarray(mu, dtype=float).reshape(-1)
    return float(e @ np.linalg.solve(P, e))
