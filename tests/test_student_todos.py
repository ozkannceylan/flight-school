"""Shipped student lab.py files are unfinished; checks must stay red."""

from __future__ import annotations

from labs_util import run_check


def test_lab00_student_todos_are_red():
    assert run_check("labs/lab00_hello_state/check.py", reference=False) == 1


def test_lab01_student_todos_are_red():
    assert run_check("labs/lab01_planar_dynamics/check.py", reference=False) == 1


def test_lab02_student_todos_are_red():
    assert run_check("labs/lab02_into_3d/check.py", reference=False) == 1


def test_lab03_student_todos_are_red():
    assert run_check("labs/lab03_cascade_pd/check.py", reference=False) == 1


def test_lab04_student_todos_are_red():
    assert run_check("labs/lab04_lqr/check.py", reference=False) == 1


def test_lab05_student_todos_are_red():
    assert run_check("labs/lab05_search_visualized/check.py", reference=False) == 1


def test_lab06_student_todos_are_red():
    assert run_check("labs/lab06_heuristics/check.py", reference=False) == 1


def test_lab07_student_todos_are_red():
    assert run_check("labs/lab07_rrt/check.py", reference=False) == 1


def test_lab08_student_todos_are_red():
    assert run_check("labs/lab08_flatness/check.py", reference=False) == 1


def test_lab09_student_todos_are_red():
    assert run_check("labs/lab09_time_scaling/check.py", reference=False) == 1


def test_lab10_student_todos_are_red():
    assert run_check("labs/lab10_set_belief/check.py", reference=False) == 1


def test_lab11_student_todos_are_red():
    assert run_check("labs/lab11_bayes/check.py", reference=False) == 1


def test_lab12_student_todos_are_red():
    assert run_check("labs/lab12_kf_pf/check.py", reference=False) == 1


def test_lab13_student_todos_are_red():
    assert run_check("labs/lab13_mcl/check.py", reference=False) == 1


def test_lab14_student_todos_are_red():
    assert run_check("labs/lab14_mapping/check.py", reference=False) == 1


def test_lab15_student_todos_are_red():
    assert run_check("labs/lab15_slam/check.py", reference=False) == 1
