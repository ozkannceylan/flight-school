"""Lab 16 — The Camera Is a Matrix.

Pinhole projection and a linear calibration of K from known correspondences.

    python labs/lab16_camera/check.py
    python labs/lab16_camera/demo.py
"""

from __future__ import annotations

import numpy as np

from flightlab.render import camera_from_planar, to_camera


# ---------------------------------------------------------------------------
# TODO 1 — pinhole project  (≤10 lines)
# ---------------------------------------------------------------------------
def project(K: np.ndarray, R: np.ndarray, C: np.ndarray, X: np.ndarray) -> np.ndarray:
    """``u = fx X/Z + cx``, ``v = fy Y/Z + cy`` in the camera frame. Shape ``(..., 2)``."""
    # TODO(1): Xc = R @ (X-C).T .T ; then divide by depth
    raise NotImplementedError("TODO 1: project")


# ---------------------------------------------------------------------------
# TODO 2 — calibrate fx, fy, cx, cy given known pose  (≤15 lines)
# ---------------------------------------------------------------------------
def calibrate_K(X: np.ndarray, uv: np.ndarray, R: np.ndarray, C: np.ndarray) -> np.ndarray:
    """Least-squares K from world points and pixels. Pose is known.

    For each point: ``u = fx (Xc/Zc) + cx``. Stack and solve two 2-parameter LSQ.
    """
    # TODO(2)
    raise NotImplementedError("TODO 2: calibrate_K")


# ---------------------------------------------------------------------------
# TODO 3 — mean reprojection error in pixels  (≤6 lines)
# ---------------------------------------------------------------------------
def reprojection_error(K: np.ndarray, R: np.ndarray, C: np.ndarray, X: np.ndarray, uv: np.ndarray) -> float:
    """RMSE of ``project(K,...)`` vs ``uv``."""
    # TODO(3)
    raise NotImplementedError("TODO 3: reprojection_error")
