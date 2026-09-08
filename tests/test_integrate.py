"""Core integrator sanity."""

from __future__ import annotations

import numpy as np
import pytest
from scipy.integrate import solve_ivp

from flightlab.integrate import euler, rk4, rollout, step


def test_euler_constant_derivative():
    def f(x, u):
        return np.array([1.0, 2.0])

    got = euler(f, np.array([0.0, 0.0]), None, 0.25)
    np.testing.assert_allclose(got, [0.25, 0.50])


def test_rk4_linear_decay_one_step():
    def f(x, u):
        return -x

    x0 = np.array([1.0])
    dt = 0.2
    k1 = -x0
    k2 = -(x0 + 0.5 * dt * k1)
    k3 = -(x0 + 0.5 * dt * k2)
    k4 = -(x0 + dt * k3)
    expected = x0 + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
    np.testing.assert_allclose(rk4(f, x0, None, dt), expected)


def test_rk4_beats_euler_on_exponential():
    def f(x, u):
        return -x

    x0 = np.array([1.0])
    dt, t_end = 0.1, 2.0
    _, xs_e, _ = rollout(f, x0, dt, t_end, method="euler")
    _, xs_r, _ = rollout(f, x0, dt, t_end, method="rk4")
    truth = np.exp(-t_end)
    err_e = abs(xs_e[-1, 0] - truth)
    err_r = abs(xs_r[-1, 0] - truth)
    assert err_r < 0.1 * err_e


def test_rollout_shapes_and_policy():
    def f(x, u):
        return np.array([x[1], float(u[0])])

    def policy(x, t):
        return np.array([1.0])

    t, xs, us = rollout(f, np.array([0.0, 0.0]), dt=0.1, t_end=1.0, policy=policy)
    assert t.shape == (11,)
    assert xs.shape == (11, 2)
    assert us.shape == (11, 1)
    np.testing.assert_allclose(us, 1.0)


def test_rollout_matches_scipy_ho():
    def f(x, u):
        return np.array([x[1], -x[0]])

    x0 = np.array([1.0, 0.0])
    dt, t_end = 0.01, 2.0
    t, xs, _ = rollout(f, x0, dt, t_end, method="rk4")
    sol = solve_ivp(lambda tt, y: f(y, None), (0.0, t_end), x0, t_eval=[t_end], rtol=1e-9, atol=1e-9)
    np.testing.assert_allclose(xs[-1], sol.y[:, -1], atol=1e-6)


def test_step_rejects_unknown_method():
    with pytest.raises(ValueError):
        step(lambda x, u: x, np.array([0.0]), None, 0.1, method="rk2")
