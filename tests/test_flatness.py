"""Planar-quad flatness inversion at hover."""

from __future__ import annotations

import numpy as np

from flightlab.dynamics import PlanarQuadrotor
from flightlab.planning.flatness import flat_to_xu, quintic_coeffs, sample_trajectory


def test_hover_inversion():
    q = PlanarQuadrotor()
    x, u = flat_to_xu(0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, q)
    np.testing.assert_allclose(x, [0, 1, 0, 0, 0, 0], atol=1e-9)
    np.testing.assert_allclose(u, q.hover_input(), atol=1e-9)


def test_quintic_endpoints():
    c = quintic_coeffs(1.0, 0.0, 2.0)
    from flightlab.planning.flatness import eval_poly

    p0, v0, a0, _, _ = eval_poly(c, 0.0)
    p1, v1, a1, _, _ = eval_poly(c, 1.0)
    np.testing.assert_allclose([p0, v0, a0], [0, 0, 0], atol=1e-9)
    np.testing.assert_allclose([p1, v1, a1], [2, 0, 0], atol=1e-9)


def test_sample_traj_hits_waypoints():
    q = PlanarQuadrotor()
    wy = np.array([0.0, 1.0, 2.0])
    wz = np.array([1.0, 1.2, 1.0])
    d = np.array([1.0, 1.0])
    t, xs, us = sample_trajectory(wy, wz, d, 0.05, q)
    np.testing.assert_allclose(xs[0, :2], [0.0, 1.0], atol=1e-8)
    np.testing.assert_allclose(xs[-1, :2], [2.0, 1.0], atol=1e-3)
    assert us.shape[1] == 2
