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


def test_lab08_falls_back_to_reference_lqr():
    """PLAN Phase 2 exit: unfinished Lab 04 must not block Lab 08."""
    from flightlab.control import linearize
    from flightlab.dynamics import PlanarQuadrotor

    lab04 = get("lab04")
    lab08 = get("lab08")
    plant = PlanarQuadrotor()
    t, xs, _us = lab08.sample_flat_traj(plant, dt=0.1, scale=1.0)
    assert len(t) > 5 and xs.shape[1] == 6
    A, B = linearize(plant.f, plant.reset(), plant.hover_input())
    Q, R = lab04.design_QR()
    K, _ = lab04.lqr(A, B, Q, R)
    assert K.shape == (2, 6)


def test_lab12_falls_back_to_reference_lqr():
    """Unfinished Lab 04 must not block the Lab 12 hover dataset."""
    lab04 = get("lab04")
    lab12 = get("lab12")
    from flightlab.control import linearize
    from flightlab.dynamics import PlanarQuadrotor

    plant = PlanarQuadrotor()
    A, B = linearize(plant.f, plant.reset(), plant.hover_input())
    Q, R = lab04.design_QR()
    K, _ = lab04.lqr(A, B, Q, R)
    mu, P = lab12.kf_predict(np.zeros(6), np.eye(6), np.eye(6), 0.01 * np.eye(6))
    assert mu.shape == (6,) and P.shape == (6, 6)


def test_lab15_loop_closure_cuts_ate():
    """PLAN Phase 3 exit: loop closure drops ATE by ≥60%."""
    from flightlab.worlds import loop_dataset_lab15

    impl = get("lab15")
    gt, odom, loop, _ = loop_dataset_lab15(n_side=4, drift=0.18, seed=0)
    before = impl.compose_odometry(len(gt), odom)
    after = impl.optimize(before, list(odom) + [loop], n_iter=8)
    a0, a1 = impl.ate(before, gt), impl.ate(after, gt)
    assert a0 > 0.3
    assert a1 <= 0.40 * a0


def test_unknown_lab_raises():
    import pytest

    with pytest.raises(KeyError):
        get("lab99")
