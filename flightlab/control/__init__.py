"""Controller interfaces. Solutions live in labs/ and reference/, not here."""

from __future__ import annotations

from typing import Protocol

import numpy as np


class Controller(Protocol):
    """Map ``(x, t) → u``. Gain containers belong here later; not solutions."""

    def __call__(self, x: np.ndarray, t: float) -> np.ndarray: ...
