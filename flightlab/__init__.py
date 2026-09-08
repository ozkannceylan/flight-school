"""Shared core for flight-school labs.

Stable, boring, well-tested. Student work lives in ``labs/*/lab.py``.
"""

from flightlab.dynamics.plant import Plant
from flightlab.integrate import euler, rk4, rollout

__all__ = ["Plant", "euler", "rk4", "rollout"]
__version__ = "0.1.0"
