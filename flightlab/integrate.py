"""Fixed-step integrators. Students reimplement Euler/RK4 in Lab 00."""

from __future__ import annotations

from collections.abc import Callable

import numpy as np

VectorField = Callable[[np.ndarray, np.ndarray | None], np.ndarray]
Policy = Callable[[np.ndarray, float], np.ndarray]


def euler(f: VectorField, x: np.ndarray, u: np.ndarray | None, dt: float) -> np.ndarray:
    """One explicit-Euler step: ``x + dt f(x, u)``."""
    x = np.asarray(x, dtype=float).reshape(-1)
    return x + dt * np.asarray(f(x, u), dtype=float).reshape(-1)


def rk4(f: VectorField, x: np.ndarray, u: np.ndarray | None, dt: float) -> np.ndarray:
    """One classical Runge–Kutta 4 step of ``ẋ = f(x, u)``."""
    x = np.asarray(x, dtype=float).reshape(-1)
    k1 = np.asarray(f(x, u), dtype=float).reshape(-1)
    k2 = np.asarray(f(x + 0.5 * dt * k1, u), dtype=float).reshape(-1)
    k3 = np.asarray(f(x + 0.5 * dt * k2, u), dtype=float).reshape(-1)
    k4 = np.asarray(f(x + dt * k3, u), dtype=float).reshape(-1)
    return x + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)


def step(
    f: VectorField,
    x: np.ndarray,
    u: np.ndarray | None,
    dt: float,
    method: str = "rk4",
) -> np.ndarray:
    """Dispatch one integrator step."""
    if method == "euler":
        return euler(f, x, u, dt)
    if method == "rk4":
        return rk4(f, x, u, dt)
    raise ValueError(f"unknown method {method!r}; use 'euler' or 'rk4'")


def rollout(
    f: VectorField,
    x0: np.ndarray,
    dt: float,
    t_end: float,
    u: np.ndarray | None = None,
    policy: Policy | None = None,
    method: str = "rk4",
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Fixed-step loop.

    Parameters
    ----------
    f :
        ``ẋ = f(x, u)``.
    x0 :
        Initial state.
    dt, t_end :
        Step size and horizon. Number of steps is ``round(t_end / dt)``.
    u :
        Constant input (ignored if ``policy`` is given).
    policy :
        ``policy(x, t) -> u`` evaluated at the start of each step.
    method :
        ``"rk4"`` (default) or ``"euler"``.

    Returns
    -------
    t, xs, us :
        Times ``(N+1,)``, states ``(N+1, n)``, inputs ``(N+1, m)``.
        ``us[-1]`` repeats the last applied input.
    """
    if dt <= 0:
        raise ValueError("dt must be positive")
    n_steps = int(round(t_end / dt))
    x = np.asarray(x0, dtype=float).reshape(-1)
    xs = np.zeros((n_steps + 1, x.size), dtype=float)
    t = np.linspace(0.0, n_steps * dt, n_steps + 1)
    us_list: list[np.ndarray] = []
    xs[0] = x
    for i in range(n_steps):
        if policy is not None:
            ui = np.asarray(policy(x, t[i]), dtype=float).reshape(-1)
        elif u is not None:
            ui = np.asarray(u, dtype=float).reshape(-1)
        else:
            ui = np.zeros(0, dtype=float)
        us_list.append(ui)
        x = step(f, x, ui if ui.size else None, dt, method=method)
        xs[i + 1] = x
    if us_list:
        us = np.vstack(us_list + [us_list[-1]])
    else:
        us = np.zeros((1, 0), dtype=float)
    return t, xs, us
