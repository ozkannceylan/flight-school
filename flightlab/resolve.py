"""Student → reference resolver (ARCHITECTURE §5).

Downstream labs import through ``get(name)``. If the student file is missing,
raises, or fails a smoke test, we fall back to ``reference/`` and print a
banner. Spoilers are one ``open`` away — accepted deliberately.
"""

from __future__ import annotations

import importlib
import importlib.util
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@dataclass(frozen=True)
class LabSpec:
    key: str
    number: str
    student_path: Path
    reference_module: str
    smoke: Callable[[ModuleType], bool]


def _load_file(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def _smoke_lab00(mod: ModuleType) -> bool:
    def f(x, u):
        return np.array([x[1], -1.0], dtype=float)

    x = np.array([0.0, 0.0], dtype=float)
    for step in (mod.euler, mod.rk4):
        out = np.asarray(step(f, x, None, 0.01), dtype=float).reshape(-1)
        if out.size != 2 or not np.isfinite(out).all():
            return False
    xf = np.asarray(mod.point_mass_f(np.array([1.0, 0.0]), None), dtype=float)
    return xf.size == 2 and np.isfinite(xf).all()


def _smoke_lab01(mod: ModuleType) -> bool:
    plant = mod.PlanarQuadrotor()
    x = plant.reset()
    u = np.asarray(plant.hover_input(), dtype=float).reshape(-1)
    if u.size != 2 or not np.isfinite(u).all():
        return False
    xdot = np.asarray(plant.f(x, u), dtype=float).reshape(-1)
    return xdot.size == 6 and np.isfinite(xdot).all()


REGISTRY: dict[str, LabSpec] = {}


def _register(spec: LabSpec, *aliases: str) -> None:
    REGISTRY[spec.key] = spec
    for a in aliases:
        REGISTRY[a] = spec


_register(
    LabSpec(
        key="lab00",
        number="00",
        student_path=ROOT / "labs/lab00_hello_state/lab.py",
        reference_module="reference.lab00_hello_state",
        smoke=_smoke_lab00,
    ),
    "00",
    "lab00_hello_state",
    "hello_state",
)
_register(
    LabSpec(
        key="lab01",
        number="01",
        student_path=ROOT / "labs/lab01_planar_dynamics/lab.py",
        reference_module="reference.lab01_planar_dynamics",
        smoke=_smoke_lab01,
    ),
    "01",
    "lab01_planar_dynamics",
    "planar_quad",
    "planar_dynamics",
)


def _smoke_lab02(mod: ModuleType) -> bool:
    plant = mod.Quad3D()
    rates = np.asarray(plant.euler_zyx_rates(0.0, 0.0, np.array([1.0, 0.0, 0.0])), dtype=float)
    if rates.size != 3 or not np.isfinite(rates).all():
        return False
    xdot = np.asarray(plant.f(plant.reset(), plant.hover_input()), dtype=float).reshape(-1)
    if xdot.size != 12 or not np.isfinite(xdot).all():
        return False
    u = np.asarray(plant.altitude_loop(plant.reset(), 2.0), dtype=float).reshape(-1)
    return u.size == 4 and np.isfinite(u).all()


def _smoke_lab03(mod: ModuleType) -> bool:
    from flightlab.dynamics import PlanarQuadrotor

    plant = PlanarQuadrotor()
    A, B = mod.linearize(plant.f, plant.reset(), plant.hover_input())
    if np.asarray(A).shape != (6, 6) or np.asarray(B).shape != (6, 2):
        return False
    u = np.asarray(mod.cascade_pd(plant, plant.reset(), plant.reset()[:2], mod.DEFAULT_GAINS))
    return u.reshape(-1).size == 2 and np.isfinite(u).all()


def _smoke_lab04(mod: ModuleType) -> bool:
    from flightlab.control import linearize
    from flightlab.dynamics import PlanarQuadrotor

    plant = PlanarQuadrotor()
    Q, R = mod.design_QR()
    if np.asarray(Q).shape != (6, 6) or np.asarray(R).shape != (2, 2):
        return False
    A, B = linearize(plant.f, plant.reset(), plant.hover_input())
    K, _P = mod.lqr(A, B, Q, R)
    if np.asarray(K).shape != (2, 6):
        return False
    u = np.asarray(mod.lqr_control(plant.reset(), plant.reset(), plant.hover_input(), K))
    return u.reshape(-1).size == 2 and np.isfinite(u).all()


_register(
    LabSpec(
        key="lab02",
        number="02",
        student_path=ROOT / "labs/lab02_into_3d/lab.py",
        reference_module="reference.lab02_into_3d",
        smoke=_smoke_lab02,
    ),
    "02",
    "lab02_into_3d",
    "into_3d",
    "quad3d",
)
_register(
    LabSpec(
        key="lab03",
        number="03",
        student_path=ROOT / "labs/lab03_cascade_pd/lab.py",
        reference_module="reference.lab03_cascade_pd",
        smoke=_smoke_lab03,
    ),
    "03",
    "lab03_cascade_pd",
    "cascade_pd",
)
_register(
    LabSpec(
        key="lab04",
        number="04",
        student_path=ROOT / "labs/lab04_lqr/lab.py",
        reference_module="reference.lab04_lqr",
        smoke=_smoke_lab04,
    ),
    "04",
    "lab04_lqr",
    "lqr",
)


def _smoke_lab05(mod: ModuleType) -> bool:
    from flightlab.worlds import maze_lab05

    q = mod.QueueFrontier()
    q.push((0, 0))
    if q.pop() != (0, 0):
        return False
    grid, start, goal = maze_lab05()
    path, exp = mod.bfs(grid, start, goal)
    return bool(path) and path[-1] == goal and len(exp) > 0


def _smoke_lab06(mod: ModuleType) -> bool:
    from flightlab.worlds import manhattan, terrain_lab06

    cmap, start, goal = terrain_lab06()
    path, exp, cost = mod.dijkstra(cmap, start, goal)
    return bool(path) and np.isfinite(cost) and len(exp) > 0


def _smoke_lab07(mod: ModuleType) -> bool:
    from flightlab.worlds import forest_lab07

    field, start, goal = forest_lab07()
    path, nodes, parents = mod.rrt(field, start, goal, seed=0, n_iter=200)
    return len(nodes) >= 2 and len(parents) == len(nodes)


def _smoke_lab08(mod: ModuleType) -> bool:
    from flightlab.dynamics import PlanarQuadrotor

    plant = PlanarQuadrotor()
    x, u = mod.flat_to_xu(0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, plant)
    t, xs, us = mod.sample_flat_traj(plant, dt=0.1, scale=1.0)
    return np.asarray(x).size == 6 and np.asarray(u).size == 2 and len(t) > 3


def _smoke_lab09(mod: ModuleType) -> bool:
    us = np.array([[1.0, -2.0]])
    return abs(mod.peak_rotor(us) - 2.0) < 1e-9


_register(
    LabSpec(
        key="lab05",
        number="05",
        student_path=ROOT / "labs/lab05_search_visualized/lab.py",
        reference_module="reference.lab05_search_visualized",
        smoke=_smoke_lab05,
    ),
    "05",
    "lab05_search_visualized",
    "search",
)
_register(
    LabSpec(
        key="lab06",
        number="06",
        student_path=ROOT / "labs/lab06_heuristics/lab.py",
        reference_module="reference.lab06_heuristics",
        smoke=_smoke_lab06,
    ),
    "06",
    "lab06_heuristics",
    "heuristics",
)
_register(
    LabSpec(
        key="lab07",
        number="07",
        student_path=ROOT / "labs/lab07_rrt/lab.py",
        reference_module="reference.lab07_rrt",
        smoke=_smoke_lab07,
    ),
    "07",
    "lab07_rrt",
    "rrt",
)
_register(
    LabSpec(
        key="lab08",
        number="08",
        student_path=ROOT / "labs/lab08_flatness/lab.py",
        reference_module="reference.lab08_flatness",
        smoke=_smoke_lab08,
    ),
    "08",
    "lab08_flatness",
    "flatness",
)
_register(
    LabSpec(
        key="lab09",
        number="09",
        student_path=ROOT / "labs/lab09_time_scaling/lab.py",
        reference_module="reference.lab09_time_scaling",
        smoke=_smoke_lab09,
    ),
    "09",
    "lab09_time_scaling",
    "time_scaling",
)


def _smoke_lab10(mod: ModuleType) -> bool:
    from flightlab.worlds import rooms_lab10, start_lab10

    grid = rooms_lab10()
    bel = __import__("numpy").zeros((grid.rows, grid.cols), dtype=bool)
    bel[start_lab10()] = True
    out = mod.predict(bel, grid, (0, 1))
    return bool(out.any()) and out.shape == bel.shape


def _smoke_lab11(mod: ModuleType) -> bool:
    import numpy as np

    from flightlab.worlds import corridor_lab11

    doors, _ = corridor_lab11()
    bel = np.full(doors.size, 1.0 / doors.size)
    bel = mod.predict(bel)
    like = mod.likelihood(doors, True)
    post = mod.update(bel, like)
    return abs(float(post.sum()) - 1.0) < 1e-6


def _smoke_lab12(mod: ModuleType) -> bool:
    import numpy as np

    A = np.eye(6)
    mu, P = mod.kf_predict(np.zeros(6), np.eye(6), A, 0.01 * np.eye(6))
    mu, P = mod.kf_update(mu, P, np.eye(6)[:3], np.zeros(3), np.eye(3) * 0.1)
    return mu.size == 6 and np.isfinite(mu).all() and P.shape == (6, 6)


def _smoke_lab13(mod: ModuleType) -> bool:
    import numpy as np

    from flightlab.worlds import office_lab13

    rng = np.random.default_rng(0)
    grid = office_lab13()
    parts = mod.uniform_particles(8, grid, rng)
    out = mod.motion_update(parts, np.array([0.2, 0.0]), rng)
    return out.shape == (8, 3) and np.isfinite(out).all()


def _smoke_lab14(mod: ModuleType) -> bool:
    import numpy as np

    inc = mod.inverse_beam((6, 9), np.array([1.5, 1.5, 0.0]), 2.0, 0.0)
    out = mod.logodds_update(np.zeros((6, 9)), inc)
    return out.shape == (6, 9) and np.isfinite(out).all()


def _smoke_lab15(mod: ModuleType) -> bool:
    import numpy as np

    e = np.asarray(mod.edge_error(np.zeros(3), np.zeros(3), np.zeros(3)), dtype=float)
    poses = mod.compose_odometry(2, [(0, 1, np.array([1.0, 0.0, 0.0]), np.eye(3))])
    return e.size == 3 and np.isfinite(e).all() and poses.shape == (2, 3)


_register(
    LabSpec(
        key="lab10",
        number="10",
        student_path=ROOT / "labs/lab10_set_belief/lab.py",
        reference_module="reference.lab10_set_belief",
        smoke=_smoke_lab10,
    ),
    "10",
    "lab10_set_belief",
    "set_belief",
)
_register(
    LabSpec(
        key="lab11",
        number="11",
        student_path=ROOT / "labs/lab11_bayes/lab.py",
        reference_module="reference.lab11_bayes",
        smoke=_smoke_lab11,
    ),
    "11",
    "lab11_bayes",
    "bayes",
)
_register(
    LabSpec(
        key="lab12",
        number="12",
        student_path=ROOT / "labs/lab12_kf_pf/lab.py",
        reference_module="reference.lab12_kf_pf",
        smoke=_smoke_lab12,
    ),
    "12",
    "lab12_kf_pf",
    "kf_pf",
)
_register(
    LabSpec(
        key="lab13",
        number="13",
        student_path=ROOT / "labs/lab13_mcl/lab.py",
        reference_module="reference.lab13_mcl",
        smoke=_smoke_lab13,
    ),
    "13",
    "lab13_mcl",
    "mcl",
)
_register(
    LabSpec(
        key="lab14",
        number="14",
        student_path=ROOT / "labs/lab14_mapping/lab.py",
        reference_module="reference.lab14_mapping",
        smoke=_smoke_lab14,
    ),
    "14",
    "lab14_mapping",
    "mapping",
)
_register(
    LabSpec(
        key="lab15",
        number="15",
        student_path=ROOT / "labs/lab15_slam/lab.py",
        reference_module="reference.lab15_slam",
        smoke=_smoke_lab15,
    ),
    "15",
    "lab15_slam",
    "slam",
)


def _banner(spec: LabSpec, reason: str) -> None:
    msg = (
        f"using reference {spec.key} — your Lab {spec.number} isn't done or isn't passing"
        f" ({reason})"
    )
    bar = "*" * max(72, len(msg) + 4)
    print(f"\n{bar}\n* {msg}\n{bar}\n", file=sys.stderr)


def _try_student(spec: LabSpec) -> ModuleType | None:
    if not spec.student_path.is_file():
        return None
    try:
        mod = _load_file(spec.student_path, f"flightlab_student_{spec.key}")
    except Exception as exc:  # noqa: BLE001
        _banner(spec, f"import failed: {type(exc).__name__}")
        return None
    try:
        ok = spec.smoke(mod)
    except Exception as exc:  # noqa: BLE001
        _banner(spec, f"smoke test raised {type(exc).__name__}")
        return None
    if not ok:
        _banner(spec, "smoke test failed")
        return None
    return mod


def get(name: str) -> ModuleType:
    """Return the student module if it smokes clean, else the reference."""
    key = name.strip().lower()
    if key not in REGISTRY:
        known = ", ".join(sorted({s.key for s in REGISTRY.values()}))
        raise KeyError(f"unknown lab {name!r}; known: {known}")
    spec = REGISTRY[key]
    student = _try_student(spec)
    if student is not None:
        return student
    if spec.student_path.is_file():
        # banner already printed
        pass
    else:
        _banner(spec, "no student file")
    return importlib.import_module(spec.reference_module)
