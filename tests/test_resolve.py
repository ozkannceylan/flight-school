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


def test_unknown_lab_raises():
    import pytest

    with pytest.raises(KeyError):
        get("lab99")
