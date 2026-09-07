"""Shipped student lab.py files are unfinished; checks must stay red."""

from __future__ import annotations

from labs_util import run_check


def test_lab00_student_todos_are_red():
    assert run_check("labs/lab00_hello_state/check.py", reference=False) == 1


def test_lab01_student_todos_are_red():
    assert run_check("labs/lab01_planar_dynamics/check.py", reference=False) == 1
