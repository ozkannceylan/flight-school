"""Planar quadrotor — the spine plant for (almost) every lab.

State ``x = [p_y, p_z, θ, v_y, v_z, ω]`` (LECTURE_LAB_MAP L02 / Lab 01).
Input ``u = [u1, u2]``: right and left rotor thrusts (Newtons).

World frame: +y right, +z up. ``θ`` is the counterclockwise tilt from upright.
Thrust is along the body +z axis, so

    ÿ = −((u1+u2)/m) sin(θ)
    z̈ =  ((u1+u2)/m) cos(θ) − g
    θ̈ =  L (u1 − u2) / I

Hover: ``θ = 0``, ``u1 = u2 = mg/2``.
"""

from __future__ import annotations

from typing import Any

import numpy as np

from flightlab.dynamics.plant import as_input, as_state

# State indices — import these rather than sprinkling magic numbers.
IY, IZ, ITH, IVY, IVZ, IOM = range(6)
STATE_NAMES = ("p_y", "p_z", "theta", "v_y", "v_z", "omega")


class PlanarQuadrotor:
    """Six-state, two-thrust planar quadrotor (implements ``Plant``)."""

    state_dim = 6
    input_dim = 2

    def __init__(
        self,
        m: float = 1.0,
        L: float = 0.25,
        I: float = 0.01,
        g: float = 9.81,
    ) -> None:
        if m <= 0 or L <= 0 or I <= 0:
            raise ValueError("m, L, I must be positive")
        self.m = float(m)
        self.L = float(L)
        self.I = float(I)
        self.g = float(g)

    def f(self, x: np.ndarray, u: np.ndarray) -> np.ndarray:
        py, pz, theta, vy, vz, omega = as_state(x, self.state_dim)
        _ = py, pz
        u1, u2 = as_input(u, self.input_dim)
        thrust = u1 + u2
        m, L, I, g = self.m, self.L, self.I, self.g
        return np.array(
            [
                vy,
                vz,
                omega,
                -(thrust / m) * np.sin(theta),
                (thrust / m) * np.cos(theta) - g,
                (L * (u1 - u2)) / I,
            ],
            dtype=float,
        )

    def hover_input(self) -> np.ndarray:
        """Analytic hover: each rotor carries half the weight."""
        half = self.m * self.g / 2.0
        return np.array([half, half], dtype=float)

    def reset(self, x0: np.ndarray | None = None) -> np.ndarray:
        if x0 is None:
            # One metre up, level, at rest.
            return np.array([0.0, 1.0, 0.0, 0.0, 0.0, 0.0], dtype=float)
        return as_state(x0, self.state_dim)

    def bounds(self) -> dict[str, Any]:
        # Generous boxes; later labs tighten these.
        return {
            "x_min": np.array([-20.0, 0.0, -np.pi, -10.0, -10.0, -20.0]),
            "x_max": np.array([20.0, 20.0, np.pi, 10.0, 10.0, 20.0]),
            "u_min": np.zeros(2),
            "u_max": np.array([3.0, 3.0]) * self.m * self.g,
        }
