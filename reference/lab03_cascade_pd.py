"""Reference implementation for Lab 03 — Cascade PD."""

from __future__ import annotations

import numpy as np

from flightlab.control import CascadeGains
from flightlab.dynamics import PlanarQuadrotor

DEFAULT_GAINS = CascadeGains(kp_y=10.0, kd_y=8.0, kp_z=16.0, kd_z=8.0, kp_th=300.0, kd_th=24.0)


def linearize(f, x0, u0, eps: float = 1e-5):
    x0 = np.asarray(x0, dtype=float).reshape(-1)
    u0 = np.asarray(u0, dtype=float).reshape(-1)
    f0 = np.asarray(f(x0, u0), dtype=float).reshape(-1)
    n, m = x0.size, u0.size
    A = np.zeros((n, n))
    B = np.zeros((n, m))
    for i in range(n):
        dx = np.zeros(n)
        dx[i] = eps
        A[:, i] = (np.asarray(f(x0 + dx, u0), dtype=float).reshape(-1) - f0) / eps
    for j in range(m):
        du = np.zeros(m)
        du[j] = eps
        B[:, j] = (np.asarray(f(x0, u0 + du), dtype=float).reshape(-1) - f0) / eps
    return A, B


def cascade_pd(
    plant: PlanarQuadrotor,
    x: np.ndarray,
    setpoint: np.ndarray,
    gains: CascadeGains = DEFAULT_GAINS,
) -> np.ndarray:
    y, z, th, vy, vz, omega = np.asarray(x, dtype=float).reshape(-1)
    yd, zd = float(setpoint[0]), float(setpoint[1])
    ay = gains.kp_y * (yd - y) - gains.kd_y * vy
    az = gains.kp_z * (zd - z) - gains.kd_z * vz
    th_des = float(np.clip(-ay / plant.g, -0.6, 0.6))
    T = plant.m * (az + plant.g)
    T = float(np.clip(T, 0.15 * plant.m * plant.g, 2.5 * plant.m * plant.g))
    tau = plant.I * (gains.kp_th * (th_des - th) - gains.kd_th * omega)
    u1 = T / 2.0 + tau / (2.0 * plant.L)
    u2 = T / 2.0 - tau / (2.0 * plant.L)
    return np.array([u1, u2], dtype=float)


def controller(x: np.ndarray, t: float = 0.0, *, plant: PlanarQuadrotor | None = None) -> np.ndarray:
    plant = plant or PlanarQuadrotor()
    return cascade_pd(plant, x, plant.reset()[:2], DEFAULT_GAINS)
