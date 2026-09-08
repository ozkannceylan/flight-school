"""Lab 02 — Into 3D, and the First Loop.

12 states, ZYX Euler, a proportional altitude loop — and the cliff at 90°.

    python labs/lab02_into_3d/check.py
    python labs/lab02_into_3d/demo.py
"""

from __future__ import annotations

from typing import Any

import numpy as np

from flightlab.dynamics.plant import as_input, as_state
from flightlab.dynamics.quad3d import rotation_zyx


class Quad3D:
    """State ``x = [p_x, p_y, p_z, φ, θ, ψ, v_x, v_y, v_z, p, q, r]``.

    Input ``u = [T, τx, τy, τz]``. World +z up; thrust along body +z.
    """

    state_dim = 12
    input_dim = 4

    def __init__(self, m: float = 1.0, g: float = 9.81, I: np.ndarray | None = None) -> None:
        self.m = float(m)
        self.g = float(g)
        self.I = np.diag([0.01, 0.01, 0.02]) if I is None else np.asarray(I, dtype=float)
        self._I_inv = np.linalg.inv(self.I)

    # -----------------------------------------------------------------------
    # TODO 1 — Euler-angle kinematics  (≤8 lines)
    # -----------------------------------------------------------------------
    def euler_zyx_rates(self, phi: float, theta: float, omega: np.ndarray) -> np.ndarray:
        """Body rates ω=[p,q,r] → [φ̇, θ̇, ψ̇]. Watch ``tan(θ)`` and ``1/cos(θ)``."""
        p, q, r = np.asarray(omega, dtype=float).reshape(3)
        # TODO(1): ZYX Euler-rate map. It diverges at θ → ±π/2.
        raise NotImplementedError("TODO 1: implement euler_zyx_rates")

    # -----------------------------------------------------------------------
    # TODO 2 — Newton–Euler vector field  (≤12 lines)
    # -----------------------------------------------------------------------
    def f(self, x: np.ndarray, u: np.ndarray) -> np.ndarray:
        """ẋ. Acceleration is (T/m) R e3 − g ẑ. ω̇ = I⁻¹ (τ − ω × Iω)."""
        px, py, pz, phi, theta, psi, vx, vy, vz, p, q, r = as_state(x, self.state_dim)
        T, tx, ty, tz = as_input(u, self.input_dim)
        # TODO(2): return the 12-vector. Use rotation_zyx(phi, theta, psi)
        # and self.euler_zyx_rates(phi, theta, [p, q, r]).
        raise NotImplementedError("TODO 2: implement Quad3D.f")

    def hover_input(self) -> np.ndarray:
        return np.array([self.m * self.g, 0.0, 0.0, 0.0], dtype=float)

    # -----------------------------------------------------------------------
    # TODO 3 — the first closed loop  (≤6 lines)
    # -----------------------------------------------------------------------
    def altitude_loop(self, x: np.ndarray, z_des: float, kp: float = 8.0, kd: float = 5.0) -> np.ndarray:
        """P on altitude error, D on vertical velocity. Torques stay zero.

        T = mg + kp (z_des − z) − kd v_z
        """
        z, vz = float(x[2]), float(x[8])
        # TODO(3): return u = [T, 0, 0, 0]
        raise NotImplementedError("TODO 3: implement altitude_loop")

    def reset(self, x0: np.ndarray | None = None) -> np.ndarray:
        if x0 is None:
            return np.zeros(12, dtype=float) + np.array([0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        return as_state(x0, self.state_dim)

    def bounds(self) -> dict[str, Any]:
        inf = np.inf
        return {
            "x_min": np.full(12, -inf),
            "x_max": np.full(12, inf),
            "u_min": np.array([0.0, -inf, -inf, -inf]),
            "u_max": np.array([3.0 * self.m * self.g, inf, inf, inf]),
        }
