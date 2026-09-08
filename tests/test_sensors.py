"""Synthetic sensors and estimation worlds."""

from __future__ import annotations

import numpy as np

from flightlab.geometry import ominus, oplus, wrap
from flightlab.sensors import IMU, RangeSensor, raycast
from flightlab.worlds import mapping_lab14, office_lab13, rooms_lab10


def test_raycast_hits_nearby_wall():
    grid = rooms_lab10()
    # start hallway facing +x toward the far wall
    z = raycast(grid, np.array([1.5, 5.5, 0.0]), 0.0, max_range=12.0, step=0.2)
    assert 0.5 < z < 10.0


def test_range_sensor_shape():
    grid = office_lab13()
    sensor = RangeSensor(n_beams=5, fov=np.pi, max_range=7.0, sigma=0.0)
    z = sensor.measure(np.array([2.5, 6.5, 0.0]), grid, rng=0)
    assert z.shape == (5,)
    assert np.all((z >= 0.0) & (z <= 7.0))


def test_imu_adds_bias():
    imu = IMU(gyro_sigma=0.0, accel_sigma=0.0, gyro_bias=0.1)
    g, a = imu.measure(0.0, np.zeros(2), rng=0)
    assert abs(g - 0.1) < 1e-12
    np.testing.assert_allclose(a, 0.0)


def test_se2_roundtrip():
    a = np.array([1.0, 2.0, 0.4])
    d = np.array([0.3, -0.1, 0.2])
    b = oplus(a, d)
    np.testing.assert_allclose(ominus(a, b), d, atol=1e-12)
    assert abs(float(wrap(3.5 * np.pi))) <= np.pi


def test_mapping_map_has_interior():
    grid = mapping_lab14()
    assert grid.is_free((1, 1))
    assert grid.occ[0, 0]
