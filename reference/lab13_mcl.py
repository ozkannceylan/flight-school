"""Reference implementation for Lab 13 — Known Map, Unknown Pose."""

from __future__ import annotations

import numpy as np

from flightlab.geometry import oplus
from flightlab.sensors import RangeSensor
from flightlab.worlds import OccupancyGrid


def motion_update(
    particles: np.ndarray,
    u: np.ndarray,
    rng: np.random.Generator,
    trans_std: float = 0.08,
    rot_std: float = 0.08,
) -> np.ndarray:
    u = np.asarray(u, dtype=float).reshape(2)
    n = len(particles)
    dx = u[0] + rng.normal(0.0, trans_std, size=n)
    dth = u[1] + rng.normal(0.0, rot_std, size=n)
    out = np.empty_like(particles, dtype=float)
    for i in range(n):
        out[i] = oplus(particles[i], np.array([dx[i], 0.0, dth[i]]))
    return out


def weight(
    particles: np.ndarray,
    z: np.ndarray,
    grid: OccupancyGrid,
    sensor: RangeSensor,
    sigma: float = 0.25,
) -> np.ndarray:
    z = np.asarray(z, dtype=float).reshape(-1)
    q = np.empty(len(particles))
    for i, p in enumerate(particles):
        zhat = sensor.expected(p, grid)
        q[i] = np.sum(((z - zhat) / sigma) ** 2)
    w = np.exp(-0.5 * (q - q.min()))
    s = w.sum()
    return w / s if s > 0 else np.full(len(w), 1.0 / len(w))


def resample(
    particles: np.ndarray,
    weights: np.ndarray,
    rng: np.random.Generator,
    grid: OccupancyGrid,
    inject: float = 0.0,
) -> np.ndarray:
    w = np.asarray(weights, dtype=float).reshape(-1)
    w = w / w.sum()
    n = w.size
    cdf = np.cumsum(w)
    u0 = float(rng.uniform(0.0, 1.0 / n))
    idx = np.clip(np.searchsorted(cdf, u0 + np.arange(n) / n), 0, n - 1)
    out = np.asarray(particles, dtype=float)[idx]
    n_inj = int(round(inject * n))
    if n_inj > 0:
        out[:n_inj] = uniform_particles(n_inj, grid, rng)
    return out


def uniform_particles(n: int, grid: OccupancyGrid, rng: np.random.Generator) -> np.ndarray:
    free = np.argwhere(~grid.occ)
    idx = rng.integers(0, len(free), size=n)
    cells = free[idx].astype(float)
    th = rng.uniform(-np.pi, np.pi, size=n)
    return np.column_stack([cells[:, 1] + 0.5, cells[:, 0] + 0.5, th])


def mean_pose(particles: np.ndarray) -> np.ndarray:
    c = np.mean(np.cos(particles[:, 2]))
    s = np.mean(np.sin(particles[:, 2]))
    return np.array([particles[:, 0].mean(), particles[:, 1].mean(), float(np.arctan2(s, c))])
