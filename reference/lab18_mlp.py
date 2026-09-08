"""Reference implementation for Lab 18 — An MLP You Can Read."""

from __future__ import annotations

import numpy as np


def relu(z: np.ndarray) -> np.ndarray:
    return np.maximum(z, 0.0)


def forward(x: np.ndarray, W1: np.ndarray, b1: np.ndarray, W2: np.ndarray, b2: np.ndarray):
    x = np.asarray(x, dtype=float)
    z1 = x @ W1 + b1
    h = relu(z1)
    yhat = h @ W2 + b2
    return yhat, {"x": x, "z1": z1, "h": h, "W2": W2}


def backward(yhat: np.ndarray, y: np.ndarray, cache) -> dict[str, np.ndarray]:
    x, z1, h, W2 = cache["x"], cache["z1"], cache["h"], cache["W2"]
    dy = (2.0 / yhat.size) * (yhat - y)
    dW2 = h.T @ dy
    db2 = dy.sum(axis=0)
    dh = dy @ W2.T
    dz1 = dh * (z1 > 0.0)
    dW1 = x.T @ dz1
    db1 = dz1.sum(axis=0)
    return {"W1": dW1, "b1": db1, "W2": dW2, "b2": db2}


def gd_step(params: dict, grads: dict, lr: float) -> dict:
    return {k: params[k] - lr * grads[k] for k in params}


def mse(yhat: np.ndarray, y: np.ndarray) -> float:
    return float(np.mean((yhat - y) ** 2))


def init_params(rng: np.random.Generator, n_in: int = 6, n_h: int = 16, n_out: int = 2) -> dict:
    W1 = rng.normal(0.0, 1.0 / np.sqrt(n_in), size=(n_in, n_h))
    W2 = rng.normal(0.0, 1.0 / np.sqrt(n_h), size=(n_h, n_out))
    return {"W1": W1, "b1": np.zeros(n_h), "W2": W2, "b2": np.zeros(n_out)}
