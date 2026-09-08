"""Reference implementation for Lab 02 — Into 3D, and the First Loop."""

from __future__ import annotations

from typing import Any

import numpy as np

from flightlab.dynamics.plant import as_input, as_state
from flightlab.dynamics.quad3d import rotation_zyx


class Quad3D:
    state_dim = 12
    input_dim = 4

    def __init__(self, m: float = 1.0, g: float = 9.81, I: np.ndarray | None = None) -> None:
        self.m = float(m)
        self.g = float(g)
        self.I = np.diag([0.01, 0.01, 0.02]) if I is None else np.asarray(I, dtype=float)
        self._I_inv = np.linalg.inv(self.I)

    def euler_zyx_rates(self, phi: float, theta: float, omega: np.ndarray) -> np.ndarray:
        p, q, r = np.asarray(omega, dtype=float).reshape(3)
        sφ, cφ = np.sin(phi), np.cos(phi)
        tθ = np.tan(theta)
        cθ = np.cos(theta)
        return np.array(
            [
                p + q * sφ * tθ + r * cφ * tθ,
                q * cφ - r * sφ,
                (q * sφ + r * cφ) / cθ,
            ],
            dtype=float,
        )

    def f(self, x: np.ndarray, u: np.ndarray) -> np.ndarray:
        px, py, pz, phi, theta, psi, vx, vy, vz, p, q, r = as_state(x, self.state_dim)
        _ = px, py, pz
        T, tx, ty, tz = as_input(u, self.input_dim)
        R = rotation_zyx(phi, theta, psi)
        acc = (T / self.m) * R[:, 2] - np.array([0.0, 0.0, self.g])
        omega = np.array([p, q, r], dtype=float)
        tau = np.array([tx, ty, tz], dtype=float)
        omega_dot = self._I_inv @ (tau - np.cross(omega, self.I @ omega))
        eul_dot = self.euler_zyx_rates(phi, theta, omega)
        return np.array([vx, vy, vz, *eul_dot, acc[0], acc[1], acc[2], *omega_dot], dtype=float)

    def hover_input(self) -> np.ndarray:
        return np.array([self.m * self.g, 0.0, 0.0, 0.0], dtype=float)

    def altitude_loop(self, x: np.ndarray, z_des: float, kp: float = 8.0, kd: float = 5.0) -> np.ndarray:
        z, vz = float(x[2]), float(x[8])
        T = self.m * self.g + kp * (z_des - z) - kd * vz
        return np.array([T, 0.0, 0.0, 0.0], dtype=float)

    def reset(self, x0: np.ndarray | None = None) -> np.ndarray:
        if x0 is None:
            return np.array([0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        return as_state(x0, self.state_dim)

    def bounds(self) -> dict[str, Any]:
        inf = np.inf
        return {
            "x_min": np.full(12, -inf),
            "x_max": np.full(12, inf),
            "u_min": np.array([0.0, -inf, -inf, -inf]),
            "u_max": np.array([3.0 * self.m * self.g, inf, inf, inf]),
        }
