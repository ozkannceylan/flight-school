"""Engine-agnostic ``Plant`` protocol (ARCHITECTURE ADR-006).

Phase 5 may swap this for a PyBullet-backed plant. Keep the surface narrow:
``state_dim``, ``input_dim``, ``f(x, u)``, ``reset``, ``bounds``.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

import numpy as np


@runtime_checkable
class Plant(Protocol):
    """Continuous-time plant: ``ẋ = f(x, u)``."""

    state_dim: int
    input_dim: int

    def f(self, x: np.ndarray, u: np.ndarray) -> np.ndarray:
        """Return the state derivative at ``(x, u)``."""

    def reset(self, x0: np.ndarray | None = None) -> np.ndarray:
        """Return a valid initial state (``x0`` if given, else a default)."""

    def bounds(self) -> dict[str, Any]:
        """State/input box constraints. Keys: ``x_min``, ``x_max``, ``u_min``, ``u_max``."""


def as_state(x: np.ndarray, dim: int) -> np.ndarray:
    """Copy ``x`` to a 1-D float array and check dimension."""
    arr = np.asarray(x, dtype=float).reshape(-1)
    if arr.size != dim:
        raise ValueError(f"expected state dim {dim}, got {arr.size}")
    return arr


def as_input(u: np.ndarray | None, dim: int) -> np.ndarray:
    """Copy ``u`` to a 1-D float array. ``None`` becomes zeros when ``dim==0``."""
    if u is None:
        if dim == 0:
            return np.zeros(0, dtype=float)
        raise ValueError("input u is required")
    arr = np.asarray(u, dtype=float).reshape(-1)
    if arr.size != dim:
        raise ValueError(f"expected input dim {dim}, got {arr.size}")
    return arr
