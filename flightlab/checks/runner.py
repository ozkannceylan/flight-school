"""Graded-table runner: partial credit, per-criterion hints (ADR-004)."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass

import numpy as np


class CheckFailure(AssertionError):
    """A criterion failed. Message is shown on the [FAIL] line."""


@dataclass(frozen=True)
class Criterion:
    name: str
    fn: Callable[[], None]
    hint: str = ""


def assert_close(
    got: np.ndarray | float,
    expected: np.ndarray | float,
    *,
    atol: float = 1e-6,
    rtol: float = 1e-6,
    msg: str = "",
) -> None:
    g = np.asarray(got, dtype=float)
    e = np.asarray(expected, dtype=float)
    if g.shape != e.shape:
        raise CheckFailure(msg or f"shape {g.shape} != {e.shape}")
    if not np.allclose(g, e, atol=atol, rtol=rtol):
        raise CheckFailure(msg or f"expected {e}, got {g}")


def assert_true(cond: bool, msg: str) -> None:
    if not cond:
        raise CheckFailure(msg)


@dataclass
class Report:
    title: str
    passed: int
    total: int
    lines: list[str]

    @property
    def ok(self) -> bool:
        return self.passed == self.total


def run_table(title: str, criteria: Sequence[Criterion], *, silent: bool = False) -> Report:
    """Run criteria and print a green/red table. Does not raise."""
    lines: list[str] = [title]
    passed = 0
    for crit in criteria:
        try:
            crit.fn()
        except NotImplementedError:
            detail = "not implemented"
            hint = f"   → hint: {crit.hint}" if crit.hint else ""
            lines.append(f"  [FAIL] {crit.name}{': ' + detail if detail else ''}{hint}")
        except CheckFailure as exc:
            detail = str(exc)
            hint = f"   → hint: {crit.hint}" if crit.hint else ""
            extra = f" {detail}" if detail else ""
            lines.append(f"  [FAIL] {crit.name}{extra}{hint}")
        except Exception as exc:  # noqa: BLE001 — student code can throw anything
            detail = str(exc).split("\n")[0][:100]
            hint = f"   → hint: {crit.hint}" if crit.hint else ""
            lines.append(f"  [FAIL] {crit.name} ({type(exc).__name__}: {detail}){hint}")
        else:
            passed += 1
            lines.append(f"  [PASS] {crit.name}")

    total = len(criteria)
    if passed == total:
        summary = f"  {passed}/{total} — all green."
    elif passed == 0:
        summary = f"  {passed}/{total} — start with the first TODO. You've got this."
    else:
        summary = f"  {passed}/{total} — you're close."
    lines.append(summary)

    if not silent:
        print("\n".join(lines))
    return Report(title=title, passed=passed, total=total, lines=lines)
