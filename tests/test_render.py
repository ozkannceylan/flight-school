"""Pinhole renderer and gate images."""

from __future__ import annotations

import numpy as np

from flightlab.render import (
    camera_from_planar,
    default_K,
    landmarks_lab16,
    pose_lab16,
    project,
    render_gate,
    render_ground,
)


def test_project_downward_is_finite():
    K = default_K()
    py, pz, th = pose_lab16()
    R, C = camera_from_planar(py, pz, th)
    uv = project(K, R, C, landmarks_lab16(4))
    assert uv.shape[1] == 2
    assert np.isfinite(uv).all()


def test_render_ground_shape():
    img = render_ground(0.0, 1.5, 0.0)
    assert img.ndim == 2
    assert img.min() >= 0.0 and img.max() <= 1.0


def test_gate_has_bright_bar():
    img = render_gate(10.0, size=24, seed=0)
    assert img.shape == (24, 24)
    assert img[:, 10].mean() > img.mean()
