"""Numerical linearization of the planar hover."""

from __future__ import annotations

import numpy as np

from flightlab.control import linearize
from flightlab.dynamics import PlanarQuadrotor


def test_hover_jacobians():
    q = PlanarQuadrotor()
    A, B = linearize(q.f, q.reset(), q.hover_input())
    assert A.shape == (6, 6)
    assert B.shape == (6, 2)
    np.testing.assert_allclose(A[3, 2], -q.g, atol=2e-3)
    np.testing.assert_allclose(B[4], [1 / q.m, 1 / q.m], atol=2e-3)
    np.testing.assert_allclose(B[5], [q.L / q.I, -q.L / q.I], atol=2e-3)
