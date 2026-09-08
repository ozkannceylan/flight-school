"""Reference implementation for Lab 04 — Let the Math Tune It."""

from __future__ import annotations

import numpy as np
from scipy.linalg import solve_continuous_are

from flightlab.dynamics import PlanarQuadrotor
from flightlab.resolve import get


def design_QR() -> tuple[np.ndarray, np.ndarray]:
    Q = np.diag([12.0, 8.0, 4.0, 1.0, 1.0, 0.5])
    R = np.diag([0.2, 0.2])
    return Q, R


def lqr(A: np.ndarray, B: np.ndarray, Q: np.ndarray, R: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    P = solve_continuous_are(A, B, Q, R)
    K = np.linalg.solve(R, B.T @ P)
    return K, P


def lqr_control(x: np.ndarray, x_eq: np.ndarray, u_eq: np.ndarray, K: np.ndarray) -> np.ndarray:
    return u_eq - K @ (np.asarray(x, dtype=float).reshape(-1) - np.asarray(x_eq, dtype=float).reshape(-1))


def controller(x: np.ndarray, t: float = 0.0, *, plant: PlanarQuadrotor | None = None) -> np.ndarray:
    plant = plant or PlanarQuadrotor()
    lab03 = get("lab03")
    x_eq = plant.reset()
    u_eq = plant.hover_input()
    A, B = lab03.linearize(plant.f, x_eq, u_eq)
    Q, R = design_QR()
    K, _ = lqr(A, B, Q, R)
    return lqr_control(x, x_eq, u_eq, K)
