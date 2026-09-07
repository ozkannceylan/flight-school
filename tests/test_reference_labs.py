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


def test_lab05_reference_check():
    assert run_check("labs/lab05_search_visualized/check.py", reference=True) == 0


def test_lab06_reference_check():
    assert run_check("labs/lab06_heuristics/check.py", reference=True) == 0


def test_lab07_reference_check():
    assert run_check("labs/lab07_rrt/check.py", reference=True) == 0


def test_lab08_reference_check():
    assert run_check("labs/lab08_flatness/check.py", reference=True) == 0


def test_lab09_reference_check():
    assert run_check("labs/lab09_time_scaling/check.py", reference=True) == 0


def test_lab10_reference_check():
    assert run_check("labs/lab10_set_belief/check.py", reference=True) == 0


def test_lab11_reference_check():
    assert run_check("labs/lab11_bayes/check.py", reference=True) == 0


def test_lab12_reference_check():
    assert run_check("labs/lab12_kf_pf/check.py", reference=True) == 0


def test_lab13_reference_check():
    assert run_check("labs/lab13_mcl/check.py", reference=True) == 0


def test_lab14_reference_check():
    assert run_check("labs/lab14_mapping/check.py", reference=True) == 0


def test_lab15_reference_check():
    assert run_check("labs/lab15_slam/check.py", reference=True) == 0


def test_lab16_reference_check():
    assert run_check("labs/lab16_camera/check.py", reference=True) == 0


def test_lab17_reference_check():
    assert run_check("labs/lab17_optical_flow/check.py", reference=True) == 0


def test_lab18_reference_check():
    assert run_check("labs/lab18_mlp/check.py", reference=True) == 0


def test_lab19_reference_check():
    assert run_check("labs/lab19_sgd/check.py", reference=True) == 0


def test_lab20_reference_check():
    assert run_check("labs/lab20_overfit/check.py", reference=True) == 0


def test_lab21_reference_check():
    assert run_check("labs/lab21_cnn/check.py", reference=True) == 0


def test_lab22_reference_check():
    assert run_check("labs/lab22_rl/check.py", reference=True) == 0


def test_lab23_reference_check():
    assert run_check("labs/lab23_red_team/check.py", reference=True) == 0
