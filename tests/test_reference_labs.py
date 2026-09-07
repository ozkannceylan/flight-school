"""CI: every shipped reference impl is green against that lab's check.py."""

from __future__ import annotations

from labs_util import run_check


def test_lab00_reference_check():
    assert run_check("labs/lab00_hello_state/check.py", reference=True) == 0


def test_lab01_reference_check():
    assert run_check("labs/lab01_planar_dynamics/check.py", reference=True) == 0
