"""Planar quadrotor — hover is an equilibrium; a split thrust tumbles."""

from __future__ import annotations

import numpy as np

from flightlab.dynamics import PlanarQuadrotor
from flightlab.dynamics.plant import Plant
from flightlab.integrate import rollout


def test_plant_protocol():
    q = PlanarQuadrotor()
    assert isinstance(q, Plant)
    assert q.state_dim == 6
    assert q.input_dim == 2


def test_hover_is_equilibrium():
    q = PlanarQuadrotor()
    x = q.reset()
    u = q.hover_input()
    np.testing.assert_allclose(u, [q.m * q.g / 2.0, q.m * q.g / 2.0])
    np.testing.assert_allclose(q.f(x, u), np.zeros(6), atol=1e-12)


def test_hover_hold_five_seconds():
    q = PlanarQuadrotor()
    x0 = q.reset()
    _, xs, _ = rollout(q.f, x0, dt=0.02, t_end=5.0, u=q.hover_input())
    assert np.linalg.norm(xs[-1, :2] - x0[:2]) < 0.01


def test_asymmetric_thrust_tumbles():
    q = PlanarQuadrotor()
    u = q.hover_input() * np.array([1.01, 0.99])
    _, xs, _ = rollout(q.f, q.reset(), dt=0.02, t_end=5.0, u=u)
    assert abs(xs[-1, 2]) > 0.5 or abs(xs[-1, 5]) > 1.0


def test_gravity_only_when_unpowered():
    q = PlanarQuadrotor()
    xdot = q.f(np.zeros(6), np.zeros(2))
    np.testing.assert_allclose(xdot, [0, 0, 0, 0, -q.g, 0])


def test_reset_and_bounds_shapes():
    q = PlanarQuadrotor()
    b = q.bounds()
    assert b["x_min"].shape == (6,)
    assert b["u_max"].shape == (2,)
    np.testing.assert_allclose(q.reset(np.arange(6, dtype=float)), np.arange(6))
