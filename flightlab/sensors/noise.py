"""Known-noise helpers. Synthetic sensors, never hardware."""

from __future__ import annotations

import numpy as np


def as_rng(seed: int | np.random.Generator | None) -> np.random.Generator:
    if isinstance(seed, np.random.Generator):
        return seed
    return np.random.default_rng(seed)


def gaussian(rng: np.random.Generator, scale, size=None) -> np.ndarray:
    """Zero-mean Gaussian. ``scale`` is the standard deviation."""
    return rng.normal(0.0, scale, size=size)


def bounded(rng: np.random.Generator, bound: float, size=None) -> np.ndarray:
    """Uniform in ``[-bound, bound]`` — the set-valued cousin of Gaussian noise."""
    return rng.uniform(-bound, bound, size=size)
