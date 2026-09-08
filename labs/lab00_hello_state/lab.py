"""Lab 00 — Hello, State.

A robot is a state, a vector field, and a clock. Fill the three TODOs.

    python labs/lab00_hello_state/check.py
    python labs/lab00_hello_state/demo.py
"""

from __future__ import annotations

import numpy as np


# ---------------------------------------------------------------------------
# TODO 1 — Euler step  (≤4 lines)
# ---------------------------------------------------------------------------
def euler(f, x, u, dt: float) -> np.ndarray:
    """One explicit-Euler step of ẋ = f(x, u).

    Return the next state: x + dt * f(x, u).
    ``f`` takes (x, u) and returns an array the same shape as x.
    """
    x = np.asarray(x, dtype=float).reshape(-1)
    # TODO(1): one Euler step — return the next state
    raise NotImplementedError("TODO 1: implement Euler")


# ---------------------------------------------------------------------------
# TODO 2 — RK4 step  (≤10 lines)
# ---------------------------------------------------------------------------
def rk4(f, x, u, dt: float) -> np.ndarray:
    """One classical RK4 step of ẋ = f(x, u).

    k1 = f(x, u)
    k2 = f(x + dt/2 k1, u)
    k3 = f(x + dt/2 k2, u)
    k4 = f(x + dt   k3, u)
    x ← x + dt/6 (k1 + 2 k2 + 2 k3 + k4)
    """
    x = np.asarray(x, dtype=float).reshape(-1)
    # TODO(2): k1..k4, then the weighted average
    raise NotImplementedError("TODO 2: implement RK4")


# ---------------------------------------------------------------------------
# TODO 3 — falling point mass with quadratic drag  (≤6 lines)
# ---------------------------------------------------------------------------
def point_mass_f(x, u=None, m: float = 1.0, g: float = 9.81, c: float = 0.15) -> np.ndarray:
    """ẋ for a 1-D point mass. State ``[z, v]`` (height, velocity). ``u`` unused.

    z̈ = −g − (c/m) v |v|
    """
    z, v = np.asarray(x, dtype=float).reshape(-1)
    # TODO(3): return np.array([z_dot, v_dot])
    raise NotImplementedError("TODO 3: implement point-mass dynamics")
