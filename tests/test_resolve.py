"""Resolver falls back to reference when the student plant is unfinished."""

from __future__ import annotations

import numpy as np

from flightlab.resolve import get


def test_get_lab00_returns_working_integrators():
    impl = get("lab00")
    x = impl.euler(lambda z, u: np.array([1.0, 0.0]), np.zeros(2), None, 0.1)
    np.testing.assert_allclose(x, [0.1, 0.0])
    xdot = impl.point_mass_f(np.array([1.0, 0.0]), None)
    assert xdot.shape == (2,)
    assert np.isfinite(xdot).all()


def test_get_lab01_hover():
    impl = get("lab01")
    plant = impl.PlanarQuadrotor()
    xdot = plant.f(plant.reset(), plant.hover_input())
    np.testing.assert_allclose(xdot, np.zeros(6), atol=1e-9)


def test_get_lab02_hover():
    impl = get("lab02")
    plant = impl.Quad3D()
    np.testing.assert_allclose(plant.f(plant.reset(), plant.hover_input()), 0.0, atol=1e-9)


def test_get_lab03_cascade_at_hover():
    impl = get("lab03")
    from flightlab.dynamics import PlanarQuadrotor

    plant = PlanarQuadrotor()
    u = impl.cascade_pd(plant, plant.reset(), plant.reset()[:2], impl.DEFAULT_GAINS)
    np.testing.assert_allclose(u, plant.hover_input(), atol=0.05)


def test_get_lab04_lqr_stable():
    impl = get("lab04")
    from flightlab.control import linearize
    from flightlab.dynamics import PlanarQuadrotor

    plant = PlanarQuadrotor()
    A, B = linearize(plant.f, plant.reset(), plant.hover_input())
    Q, R = impl.design_QR()
    K, _ = impl.lqr(A, B, Q, R)
    ev = np.linalg.eigvals(A - B @ K)
    assert np.max(ev.real) < 0


def test_unknown_lab_raises():
    import pytest

    with pytest.raises(KeyError):
        get("lab99")
