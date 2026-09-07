"""Planar-quadrotor differential flatness helpers (Labs 08–09).

Flat outputs are ``(y(t), z(t))``. Attitude and thrust follow:

    θ = atan2(−ÿ, z̈ + g)
    T = m √(ÿ² + (z̈ + g)²)
    τ = I θ̈
    u1 = T/2 + τ/(2L),  u2 = T/2 − τ/(2L)
"""

from __future__ import annotations

import numpy as np

from flightlab.dynamics import PlanarQuadrotor


def quintic_coeffs(T: float, p0: float, p1: float, v0: float = 0.0, v1: float = 0.0, a0: float = 0.0, a1: float = 0.0) -> np.ndarray:
    """Rest-to-rest-capable 5th-order polynomial on ``[0, T]``."""
    T = float(T)
    if T <= 0:
        raise ValueError("T must be positive")
    # p(t) = c0 + c1 t + c2 t^2 + c3 t^3 + c4 t^4 + c5 t^5
    c0, c1, c2 = p0, v0, a0 / 2.0
    # remaining: p(T), v(T), a(T)
    A = np.array(
        [
            [T**3, T**4, T**5],
            [3 * T**2, 4 * T**3, 5 * T**4],
            [6 * T, 12 * T**2, 20 * T**3],
        ],
        dtype=float,
    )
    b = np.array(
        [
            p1 - (c0 + c1 * T + c2 * T**2),
            v1 - (c1 + 2 * c2 * T),
            a1 - (2 * c2),
        ],
        dtype=float,
    )
    c3, c4, c5 = np.linalg.solve(A, b)
    return np.array([c0, c1, c2, c3, c4, c5], dtype=float)


def eval_poly(c: np.ndarray, t: float) -> tuple[float, float, float, float, float]:
    """Return p, v, a, j, s at time ``t``."""
    c0, c1, c2, c3, c4, c5 = [float(x) for x in c]
    t = float(t)
    p = c0 + c1 * t + c2 * t**2 + c3 * t**3 + c4 * t**4 + c5 * t**5
    v = c1 + 2 * c2 * t + 3 * c3 * t**2 + 4 * c4 * t**3 + 5 * c5 * t**4
    a = 2 * c2 + 6 * c3 * t + 12 * c4 * t**2 + 20 * c5 * t**3
    j = 6 * c3 + 24 * c4 * t + 60 * c5 * t**2
    s = 24 * c4 + 120 * c5 * t
    return p, v, a, j, s


def piecewise_quintic(waypoints: np.ndarray, durations: np.ndarray) -> list[np.ndarray]:
    """Quintics with finite-difference interior velocities (rest at the ends)."""
    w = np.asarray(waypoints, dtype=float).reshape(-1)
    d = np.asarray(durations, dtype=float).reshape(-1)
    if len(d) != len(w) - 1:
        raise ValueError("need N-1 durations for N waypoints")
    t = np.concatenate([[0.0], np.cumsum(d)])
    v = np.zeros_like(w)
    for i in range(1, len(w) - 1):
        v[i] = (w[i + 1] - w[i - 1]) / (t[i + 1] - t[i - 1])
    return [
        quintic_coeffs(float(dt), float(w[i]), float(w[i + 1]), v0=float(v[i]), v1=float(v[i + 1]))
        for i, dt in enumerate(d)
    ]


def eval_piecewise(segments: list[np.ndarray], durations: np.ndarray, t: float) -> tuple[float, float, float, float, float]:
    d = np.asarray(durations, dtype=float).reshape(-1)
    t = float(max(0.0, t))
    acc = 0.0
    for c, dt in zip(segments, d, strict=True):
        if t <= acc + dt + 1e-12:
            return eval_poly(c, min(max(t - acc, 0.0), dt))
        acc += dt
    return eval_poly(segments[-1], float(d[-1]))


def flat_to_xu(
    y: float,
    z: float,
    yd: float,
    zd: float,
    ydd: float,
    zdd: float,
    yj: float,
    zj: float,
    ys: float,
    zs: float,
    plant: PlanarQuadrotor,
) -> tuple[np.ndarray, np.ndarray]:
    """Recover ``x = [y,z,θ,ẏ,ż,ω]`` and ``u = [u1,u2]`` from flat outputs."""
    g, m, I, L = plant.g, plant.m, plant.I, plant.L
    ay, az = ydd, zdd + g
    theta = float(np.arctan2(-ay, az))
    denom = ay * ay + az * az
    # θ̇ = d/dt atan2(-ay, az)
    omega = float((-az * yj + ay * zj) / denom) if denom > 1e-12 else 0.0
    # θ̈
    num_d = -zj * yj + ay * zs - (ys * az + zj * yj)
    # cleaner: differentiate omega = (-az yj + ay zj) / denom
    num = -az * yj + ay * zj
    dnum = -zs * yj - az * ys + yj * zj + ay * zs
    dden = 2.0 * (ay * yj + az * zj)
    alpha = float((dnum * denom - num * dden) / (denom**2)) if denom > 1e-12 else 0.0
    _ = num_d
    T = m * float(np.hypot(ay, az))
    tau = I * alpha
    u1 = T / 2.0 + tau / (2.0 * L)
    u2 = T / 2.0 - tau / (2.0 * L)
    x = np.array([y, z, theta, yd, zd, omega], dtype=float)
    u = np.array([u1, u2], dtype=float)
    return x, u


def sample_trajectory(
    wy: np.ndarray,
    wz: np.ndarray,
    durations: np.ndarray,
    dt: float,
    plant: PlanarQuadrotor,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Sample ``t, xs, us`` along a piecewise-quintic flat trajectory."""
    sy = piecewise_quintic(wy, durations)
    sz = piecewise_quintic(wz, durations)
    T = float(np.sum(durations))
    n = int(round(T / dt))
    t = np.linspace(0.0, n * dt, n + 1)
    xs = np.zeros((n + 1, 6))
    us = np.zeros((n + 1, 2))
    for i, ti in enumerate(t):
        y, yd, ydd, yj, ys = eval_piecewise(sy, durations, ti)
        z, zd, zdd, zj, zs = eval_piecewise(sz, durations, ti)
        xs[i], us[i] = flat_to_xu(y, z, yd, zd, ydd, zdd, yj, zj, ys, zs, plant)
    return t, xs, us
