"""Lab 23 — Red-Team Your Own Stack.

A one-page failure analysis, plus one assumption you now refuse.

    python labs/lab23_red_team/check.py
    python labs/lab23_red_team/demo.py
"""

from __future__ import annotations

import numpy as np


# Filenames the analysis must cite (the artifacts, not the ideas).
REQUIRED_CITATIONS = (
    "labs/lab11_bayes/check.py",
    "labs/lab17_optical_flow/check.py",
    "labs/lab21_cnn/check.py",
    "labs/lab22_rl/README.md",
)


# ---------------------------------------------------------------------------
# TODO 1 — one-page failure analysis  (written; return a markdown string)
# ---------------------------------------------------------------------------
def failure_analysis() -> str:
    """Cite the four paths in ``REQUIRED_CITATIONS``. Say what each assumption
    was, how it failed, and what you now refuse. Mention safety or liability
    once. This is the only TODO that is prose."""
    # TODO(1)
    raise NotImplementedError("TODO 1: failure_analysis")


# ---------------------------------------------------------------------------
# TODO 2 — texture energy  (≤6 lines)
# ---------------------------------------------------------------------------
def texture_energy(I: np.ndarray) -> float:
    """Mean ``|∇I|``. A blank patch is near zero; a wavy ground is not."""
    # TODO(2): Ix, Iy = np.gradient(I); return mean hypot
    raise NotImplementedError("TODO 2: texture_energy")


# ---------------------------------------------------------------------------
# TODO 3 — refuse to report flow without texture  (≤10 lines)
# ---------------------------------------------------------------------------
def trusted_flow(I1: np.ndarray, I2: np.ndarray, pts: np.ndarray, *, min_energy: float = 0.04):
    """``lucas_kanade`` via ``get("lab17")`` if ``texture_energy(I1) >= min_energy``.

    Otherwise return ``None``. That ``None`` is the mitigation: we no longer
    treat a singular G matrix as a velocity.
    """
    # TODO(3)
    raise NotImplementedError("TODO 3: trusted_flow")
