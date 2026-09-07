"""CI: every shipped reference impl is green against that lab's check.py."""

from __future__ import annotations

from labs_util import run_check


def test_lab00_reference_check():
    assert run_check("labs/lab00_hello_state/check.py", reference=True) == 0


def test_lab01_reference_check():
    assert run_check("labs/lab01_planar_dynamics/check.py", reference=True) == 0


def test_lab02_reference_check():
    assert run_check("labs/lab02_into_3d/check.py", reference=True) == 0


def test_lab03_reference_check():
    assert run_check("labs/lab03_cascade_pd/check.py", reference=True) == 0


def test_lab04_reference_check():
    assert run_check("labs/lab04_lqr/check.py", reference=True) == 0
