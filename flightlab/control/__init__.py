"""Controller interfaces and helpers. Solutions live in labs/ and reference/."""

from __future__ import annotations

from typing import Protocol

import numpy as np

from flightlab.control.gains import CascadeGains
from flightlab.control.linearize import linearize


class Controller(Protocol):
    """Map ``(x, t) → u``. Gain containers belong here later; not solutions."""

    def __call__(self, x: np.ndarray, t: float) -> np.ndarray: ...


__all__ = ["CascadeGains", "Controller", "linearize"]
