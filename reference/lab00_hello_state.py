"""Reference implementation for Lab 00 — Hello, State.

Same API as ``labs/lab00_hello_state/lab.py``.
"""

from __future__ import annotations

import numpy as np


def euler(f, x, u, dt: float) -> np.ndarray:
    x = np.asarray(x, dtype=float).reshape(-1)
    return x + dt * np.asarray(f(x, u), dtype=float).reshape(-1)


def rk4(f, x, u, dt: float) -> np.ndarray:
    x = np.asarray(x, dtype=float).reshape(-1)
    k1 = np.asarray(f(x, u), dtype=float).reshape(-1)
    k2 = np.asarray(f(x + 0.5 * dt * k1, u), dtype=float).reshape(-1)
    k3 = np.asarray(f(x + 0.5 * dt * k2, u), dtype=float).reshape(-1)
    k4 = np.asarray(f(x + dt * k3, u), dtype=float).reshape(-1)
    return x + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)


def point_mass_f(x, u=None, m: float = 1.0, g: float = 9.81, c: float = 0.15) -> np.ndarray:
    _ = u
    z, v = np.asarray(x, dtype=float).reshape(-1)
    _ = z
    accel = -g - (c / m) * v * np.abs(v)
    return np.array([v, accel], dtype=float)
