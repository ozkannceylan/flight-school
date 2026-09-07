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
