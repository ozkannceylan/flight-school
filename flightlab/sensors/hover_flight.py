"""Shared hover-flight rollouts for Lab 12 (KF / PF)."""

from __future__ import annotations

import numpy as np

from flightlab.control import linearize
from flightlab.dynamics import PlanarQuadrotor
from flightlab.integrate import rk4
from flightlab.sensors.noise import as_rng


# Observe y, z, theta — enough to keep the hover KF honest.
H = np.array(
    [
        [1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
    ]
)


def discrete_hover(plant: PlanarQuadrotor, dt: float) -> tuple[np.ndarray, np.ndarray]:
    A, B = linearize(plant.f, plant.reset(), plant.hover_input())
    return np.eye(6) + dt * A, dt * B


def hover_dataset(
    plant: PlanarQuadrotor,
    K: np.ndarray,
    x0: np.ndarray,
    *,
    dt: float = 0.02,
    n: int = 50,
    process_std: float = 0.015,
    meas_std: tuple[float, float, float] = (0.04, 0.04, 0.03),
    seed: int = 0,
    closed_loop: bool = True,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return ``xs (n+1,6)``, ``us (n+1,2)``, ``zs (n+1,3)`` on the nonlinear plant.

    Process noise is applied to *velocities only* so a hover LQR stays bounded
    under RK4. Attitude noise here is an easy way to tumble the plant.
    """
    rng = as_rng(seed)
    x_eq = plant.reset()
    u_eq = plant.hover_input()
    x = np.asarray(x0, dtype=float).reshape(6)
    xs = np.zeros((n + 1, 6))
    us = np.zeros((n + 1, 2))
    zs = np.zeros((n + 1, 3))
    Rdiag = np.asarray(meas_std, dtype=float)
    noise_mask = np.array([0.0, 0.0, 0.0, 1.0, 1.0, 0.0])
    u_lim = 3.0 * plant.m * plant.g
    for i in range(n + 1):
        if closed_loop:
            u = u_eq - K @ (x - x_eq)
            u = np.clip(u, 0.0, u_lim)
        else:
            u = u_eq.copy()
        xs[i] = x
        us[i] = u
        zs[i] = H @ x + rng.normal(0.0, Rdiag)
        if i < n:
            x = rk4(plant.f, x, u, dt)
            x = x + noise_mask * rng.normal(0.0, process_std, size=6)
    return xs, us, zs
