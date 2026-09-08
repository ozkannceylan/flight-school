"""Durable refusal: LK on a blank patch is not a velocity.

Red against the old assumption (always publish a flow). Green against
Lab 23's mitigation (`trusted_flow` returns None).
"""

from __future__ import annotations

import numpy as np

from flightlab.render import (
    IMG_H,
    IMG_W,
    analytic_flow,
    blank,
    default_K,
    render_ground,
    sample_track_points,
    wavy,
)
from flightlab.resolve import get


def _pair(texture, dpy=0.012):
    py, pz, th = 0.0, 1.5, 0.0
    a = render_ground(py, pz, th, texture=texture)
    b = render_ground(py + dpy, pz, th, texture=texture)
    pts = sample_track_points(IMG_W, IMG_H, n=25, margin=16)
    gt = analytic_flow(default_K(), py, pz, th, dpy, 0.0, 0.0, pts)
    return a, b, pts, gt


def test_old_assumption_lk_on_blank_is_wrong():
    lab17 = get("lab17")
    I1, I2, pts, gt = _pair(blank)
    fl = lab17.lucas_kanade(I1, I2, pts, win=6)
    err = float(np.nanmean(np.linalg.norm(fl - gt, axis=1)))
    assert err > 0.6


def test_mitigation_refuses_blank_and_trusts_wavy():
    lab23 = get("lab23")
    b1, b2, pts, _ = _pair(blank)
    assert lab23.trusted_flow(b1, b2, pts) is None
    w1, w2, wpts, gt = _pair(wavy)
    fl = lab23.trusted_flow(w1, w2, wpts)
    assert fl is not None
    err = float(np.nanmean(np.linalg.norm(np.asarray(fl) - gt, axis=1)))
    assert err < 0.45
