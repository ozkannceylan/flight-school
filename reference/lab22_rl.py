"""Reference implementation for Lab 22 — Learning to Hover Without Being Told How."""

from __future__ import annotations

import numpy as np

from flightlab.dynamics import PlanarQuadrotor
from flightlab.integrate import rk4


def episode_return(
    K: np.ndarray,
    plant: PlanarQuadrotor,
    x0: np.ndarray,
    *,
    dt: float = 0.02,
    t_end: float = 2.0,
) -> float:
    K = np.asarray(K, dtype=float).reshape(2, 6)
    x_eq = plant.reset()
    u_eq = plant.hover_input()
    x = np.asarray(x0, dtype=float).reshape(6)
    n = int(round(t_end / dt))
    ret = 0.0
    for _ in range(n):
        u = u_eq - K @ (x - x_eq)
        u = np.clip(u, 0.0, 3.0 * plant.m * plant.g)
        ret -= (x[0] ** 2 + (x[1] - 1.0) ** 2 + 0.01 * float(np.sum((u - u_eq) ** 2))) * dt
        x = rk4(plant.f, x, u, dt)
    return float(ret)


def cem_update(samples: np.ndarray, scores: np.ndarray, n_elite: int) -> tuple[np.ndarray, np.ndarray]:
    idx = np.argsort(np.asarray(scores, dtype=float))[-int(n_elite) :]
    elite = np.asarray(samples, dtype=float)[idx]
    mu = elite.mean(axis=0)
    std = elite.std(axis=0) + 1e-3
    return mu, std


def cem(
    plant: PlanarQuadrotor,
    *,
    n_iter: int = 8,
    n_samp: int = 16,
    n_elite: int = 4,
    seed: int = 0,
) -> tuple[np.ndarray, list[float]]:
    rng = np.random.default_rng(seed)
    dim = 12
    mu = np.zeros(dim)
    std = np.full(dim, 0.45)
    x0 = plant.reset() + np.array([0.12, 0.04, 0.05, 0.0, 0.0, 0.0])
    hist: list[float] = []
    best_K = mu.reshape(2, 6)
    best = -1e9
    for _ in range(n_iter):
        samples = mu + std * rng.normal(size=(n_samp, dim))
        scores = np.array(
            [episode_return(s.reshape(2, 6), plant, x0) for s in samples],
            dtype=float,
        )
        mu, std = cem_update(samples, scores, n_elite)
        hist.append(float(scores.max()))
        if scores.max() > best:
            best = float(scores.max())
            best_K = samples[int(np.argmax(scores))].reshape(2, 6)
    return best_K, hist
