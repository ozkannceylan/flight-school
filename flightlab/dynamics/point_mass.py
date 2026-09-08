"""1-D point mass with gravity and optional quadratic drag."""

from __future__ import annotations

from typing import Any

import numpy as np

from flightlab.dynamics.plant import as_state


class PointMass1D:
    """State ``[z, v]``. Input unused (free fall / drag)."""

    state_dim = 2
    input_dim = 0

    def __init__(self, m: float = 1.0, g: float = 9.81, c: float = 0.0) -> None:
        if m <= 0:
            raise ValueError("mass must be positive")
        self.m = float(m)
        self.g = float(g)
        self.c = float(c)

    def f(self, x: np.ndarray, u: np.ndarray | None = None) -> np.ndarray:
        _ = u
        z, v = as_state(x, self.state_dim)
        _ = z
        accel = -self.g - (self.c / self.m) * v * np.abs(v)
        return np.array([v, accel], dtype=float)

    def reset(self, x0: np.ndarray | None = None) -> np.ndarray:
        if x0 is None:
            return np.array([10.0, 0.0], dtype=float)
        return as_state(x0, self.state_dim)

    def bounds(self) -> dict[str, Any]:
        inf = np.inf
        return {
            "x_min": np.array([-inf, -inf]),
            "x_max": np.array([inf, inf]),
            "u_min": np.zeros(0),
            "u_max": np.zeros(0),
        }

    def terminal_velocity(self) -> float:
        """Analytic ``v_∞ = -√(mg/c)`` for quadratic drag. ``-inf`` if ``c==0``."""
        if self.c <= 0:
            return -np.inf
        return -np.sqrt(self.m * self.g / self.c)
