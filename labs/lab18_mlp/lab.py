"""Lab 18 — An MLP You Can Read.

Forward, MSE, backprop. Then fly the Lab 04 LQR policy you just fitted.

    python labs/lab18_mlp/check.py
    python labs/lab18_mlp/demo.py
"""

from __future__ import annotations

import numpy as np


# ---------------------------------------------------------------------------
# TODO 1 — forward  (≤10 lines)
# ---------------------------------------------------------------------------
def relu(z: np.ndarray) -> np.ndarray:
    return np.maximum(z, 0.0)


def forward(x: np.ndarray, W1: np.ndarray, b1: np.ndarray, W2: np.ndarray, b2: np.ndarray):
    """Return ``(yhat, cache)``. Hidden ReLU, linear output. ``x`` is ``(N, in)``."""
    # TODO(1): h = relu(x W1 + b1); y = h W2 + b2
    raise NotImplementedError("TODO 1: forward")


# ---------------------------------------------------------------------------
# TODO 2 — analytic backward  (≤15 lines)
# ---------------------------------------------------------------------------
def backward(yhat: np.ndarray, y: np.ndarray, cache) -> dict[str, np.ndarray]:
    """Grads of mean MSE (over every entry) wrt W1,b1,W2,b2."""
    # TODO(2)
    raise NotImplementedError("TODO 2: backward")


# ---------------------------------------------------------------------------
# TODO 3 — one GD step + a policy wrapper  (≤10 lines)
# ---------------------------------------------------------------------------
def gd_step(params: dict, grads: dict, lr: float) -> dict:
    """``p ← p − lr ∇p`` for each key."""
    # TODO(3)
    raise NotImplementedError("TODO 3: gd_step")


def mse(yhat: np.ndarray, y: np.ndarray) -> float:
    return float(np.mean((yhat - y) ** 2))


def init_params(rng: np.random.Generator, n_in: int = 6, n_h: int = 16, n_out: int = 2) -> dict:
    """Xavier-ish. Provided."""
    W1 = rng.normal(0.0, 1.0 / np.sqrt(n_in), size=(n_in, n_h))
    W2 = rng.normal(0.0, 1.0 / np.sqrt(n_h), size=(n_h, n_out))
    return {"W1": W1, "b1": np.zeros(n_h), "W2": W2, "b2": np.zeros(n_out)}
