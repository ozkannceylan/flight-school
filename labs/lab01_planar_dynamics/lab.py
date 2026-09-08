"""Lab 01 — Six States and Two Thrusts.

Derive ẋ = f(x, u) for the planar quadrotor. This plant is the next 22 labs.

    python labs/lab01_planar_dynamics/check.py
    python labs/lab01_planar_dynamics/demo.py
"""

from __future__ import annotations

from typing import Any

import numpy as np

from flightlab.dynamics.plant import as_input, as_state


class PlanarQuadrotor:
    """State ``x = [p_y, p_z, θ, v_y, v_z, ω]``. Input ``u = [u1, u2]``.

    World: +y right, +z up. ``θ`` is counterclockwise tilt from upright.
    ``u1`` is the *right* rotor, ``u2`` the *left*. Thrust along body +z:

        ÿ = −((u1+u2)/m) sin(θ)
        z̈ =  ((u1+u2)/m) cos(θ) − g
        θ̈ =  L (u1 − u2) / I
    """

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

    # -----------------------------------------------------------------------
    # TODO 1 — the vector field  (≤12 lines)
    # -----------------------------------------------------------------------
    def f(self, x: np.ndarray, u: np.ndarray) -> np.ndarray:
        """Return ẋ at (x, u). See the class docstring for the equations."""
        py, pz, theta, vy, vz, omega = as_state(x, self.state_dim)
        u1, u2 = as_input(u, self.input_dim)
        # TODO(1): return the 6-vector [ẏ, ż, θ̇, v̇_y, v̇_z, ω̇]
        raise NotImplementedError("TODO 1: implement PlanarQuadrotor.f")

    # -----------------------------------------------------------------------
    # TODO 2 — hover input  (≤3 lines)
    # -----------------------------------------------------------------------
    def hover_input(self) -> np.ndarray:
        """Analytic hover thrusts. Each rotor carries half the weight."""
        # TODO(2): return np.array([mg/2, mg/2])
        raise NotImplementedError("TODO 2: implement hover_input")

    # -- provided: Plant.reset / Plant.bounds (do not edit) -----------------
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
