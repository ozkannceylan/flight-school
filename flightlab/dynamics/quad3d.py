"""12-state 3D quadrotor with ZYX Euler angles (Lab 02 / L03).

Secondary plant — the spine remains the planar quadrotor. ZYX is a
deliberate choice: the singularity at ``θ = ±π/2`` is the lesson.

State ``x = [p_x, p_y, p_z, φ, θ, ψ, v_x, v_y, v_z, p, q, r]``
    world position, ZYX Euler (roll, pitch, yaw), world velocity, body rates.

Input ``u = [T, τx, τy, τz]`` — collective thrust (N) and body torques (N·m).

World frame: +z up. Body +z is the thrust axis. Gravity is ``−g ẑ``.
"""

from __future__ import annotations

from typing import Any

import numpy as np

from flightlab.dynamics.plant import as_input, as_state

IX, IY, IZ, IPHI, ITH, IPSI, IVX, IVY, IVZ, IP, IQ, IR = range(12)
STATE_NAMES = (
    "p_x",
    "p_y",
    "p_z",
    "phi",
    "theta",
    "psi",
    "v_x",
    "v_y",
    "v_z",
    "p",
    "q",
    "r",
)


def rotation_zyx(phi: float, theta: float, psi: float) -> np.ndarray:
    """Body→world rotation. ZYX: yaw ``ψ``, then pitch ``θ``, then roll ``φ``."""
    cφ, sφ = np.cos(phi), np.sin(phi)
    cθ, sθ = np.cos(theta), np.sin(theta)
    cψ, sψ = np.cos(psi), np.sin(psi)
    return np.array(
        [
            [cψ * cθ, cψ * sθ * sφ - sψ * cφ, cψ * sθ * cφ + sψ * sφ],
            [sψ * cθ, sψ * sθ * sφ + cψ * cφ, sψ * sθ * cφ - cψ * sφ],
            [-sθ, cθ * sφ, cθ * cφ],
        ],
        dtype=float,
    )


def euler_zyx_rates(phi: float, theta: float, omega: np.ndarray) -> np.ndarray:
    """Map body rates ``ω = [p, q, r]`` to Euler-angle rates ``[φ̇, θ̇, ψ̇]``.

    ``1/cos(θ)`` and ``tan(θ)`` blow up at ``θ → ±π/2`` — gimbal lock.
    """
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


class Quad3D:
    """12-state, 4-input quadrotor (implements ``Plant``)."""

    state_dim = 12
    input_dim = 4

    def __init__(
        self,
        m: float = 1.0,
        g: float = 9.81,
        I: np.ndarray | None = None,
    ) -> None:
        if m <= 0:
            raise ValueError("mass must be positive")
        self.m = float(m)
        self.g = float(g)
        if I is None:
            I = np.diag([0.01, 0.01, 0.02])
        self.I = np.asarray(I, dtype=float).reshape(3, 3)
        self._I_inv = np.linalg.inv(self.I)

    def f(self, x: np.ndarray, u: np.ndarray) -> np.ndarray:
        px, py, pz, phi, theta, psi, vx, vy, vz, p, q, r = as_state(x, self.state_dim)
        _ = px, py, pz
        T, tx, ty, tz = as_input(u, self.input_dim)
        R = rotation_zyx(phi, theta, psi)
        acc = (T / self.m) * R[:, 2] - np.array([0.0, 0.0, self.g])
        omega = np.array([p, q, r], dtype=float)
        tau = np.array([tx, ty, tz], dtype=float)
        omega_dot = self._I_inv @ (tau - np.cross(omega, self.I @ omega))
        eul_dot = euler_zyx_rates(phi, theta, omega)
        return np.array(
            [vx, vy, vz, *eul_dot, acc[0], acc[1], acc[2], *omega_dot],
            dtype=float,
        )

    def hover_input(self) -> np.ndarray:
        return np.array([self.m * self.g, 0.0, 0.0, 0.0], dtype=float)

    def reset(self, x0: np.ndarray | None = None) -> np.ndarray:
        if x0 is None:
            return np.array([0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        return as_state(x0, self.state_dim)

    def bounds(self) -> dict[str, Any]:
        inf = np.inf
        return {
            "x_min": np.array([-20, -20, 0, -np.pi, -np.pi / 2, -np.pi, -10, -10, -10, -20, -20, -20], dtype=float),
            "x_max": np.array([20, 20, 20, np.pi, np.pi / 2, np.pi, 10, 10, 10, 20, 20, 20], dtype=float),
            "u_min": np.array([0.0, -inf, -inf, -inf]),
            "u_max": np.array([3.0 * self.m * self.g, inf, inf, inf]),
        }
