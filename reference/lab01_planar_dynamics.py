"""Reference implementation for Lab 01 — Six States and Two Thrusts.

Same API as ``labs/lab01_planar_dynamics/lab.py``.
"""

from __future__ import annotations

from typing import Any

import numpy as np

from flightlab.dynamics.plant import as_input, as_state


class PlanarQuadrotor:
    """Student-shaped plant. Matches ``flightlab.dynamics.PlanarQuadrotor``."""

    state_dim = 6
    input_dim = 2

    def __init__(
        self,
        m: float = 1.0,
        L: float = 0.25,
        I: float = 0.01,
        g: float = 9.81,
    ) -> None:
        self.m = float(m)
        self.L = float(L)
        self.I = float(I)
        self.g = float(g)

    def f(self, x: np.ndarray, u: np.ndarray) -> np.ndarray:
        py, pz, theta, vy, vz, omega = as_state(x, self.state_dim)
        _ = py, pz
        u1, u2 = as_input(u, self.input_dim)
        thrust = u1 + u2
        return np.array(
            [
                vy,
                vz,
                omega,
                -(thrust / self.m) * np.sin(theta),
                (thrust / self.m) * np.cos(theta) - self.g,
                (self.L * (u1 - u2)) / self.I,
            ],
            dtype=float,
        )

    def hover_input(self) -> np.ndarray:
        half = self.m * self.g / 2.0
        return np.array([half, half], dtype=float)

    def reset(self, x0: np.ndarray | None = None) -> np.ndarray:
        if x0 is None:
            return np.array([0.0, 1.0, 0.0, 0.0, 0.0, 0.0], dtype=float)
        return as_state(x0, self.state_dim)

    def bounds(self) -> dict[str, Any]:
        return {
            "x_min": np.array([-20.0, 0.0, -np.pi, -10.0, -10.0, -20.0]),
            "x_max": np.array([20.0, 20.0, np.pi, 10.0, 10.0, 20.0]),
            "u_min": np.zeros(2),
            "u_max": np.array([3.0, 3.0]) * self.m * self.g,
        }
