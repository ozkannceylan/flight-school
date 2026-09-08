"""3D quadrotor — hover equilibrium, altitude loop, gimbal lock."""

from __future__ import annotations

import numpy as np

from flightlab.dynamics import Quad3D
from flightlab.dynamics.plant import Plant
from flightlab.dynamics.quad3d import euler_zyx_rates
from flightlab.integrate import rollout


def test_plant_protocol():
    q = Quad3D()
    assert isinstance(q, Plant)
    assert q.state_dim == 12
    assert q.input_dim == 4


def test_hover_is_equilibrium():
    q = Quad3D()
    np.testing.assert_allclose(q.f(q.reset(), q.hover_input()), 0.0, atol=1e-12)


def test_euler_rates_match_body_rates_when_level():
    np.testing.assert_allclose(euler_zyx_rates(0.0, 0.0, np.array([0.2, -0.1, 0.3])), [0.2, -0.1, 0.3])


def test_gimbal_lock_blows_up():
    level = np.linalg.norm(euler_zyx_rates(0.0, 0.0, np.array([0.0, 0.0, 1.0])))
    near = np.linalg.norm(euler_zyx_rates(0.0, 1.56, np.array([0.0, 0.0, 1.0])))
    assert near > 10.0 * level


def test_altitude_hold_from_core_plant():
    from reference.lab02_into_3d import Quad3D as StudentShaped

    q = StudentShaped()

    def policy(x, t):
        return q.altitude_loop(x, 2.0)

    _, xs, _ = rollout(q.f, q.reset(), dt=0.02, t_end=4.0, policy=policy)
    assert abs(xs[-1, 2] - 2.0) < 0.15
