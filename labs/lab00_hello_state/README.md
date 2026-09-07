# Lab 00 — Hello, State

⏱ 30 min · ⇐ none · Phase 1

## Why now?

Every later lab is ``ẋ = f(x, u)`` plus a clock. Build the clock once.

## What's the idea?

A robot is three things: a **state** ``x``, a **vector field** ``f``, and a
**step** that advances time.

```
        x_{k+1} = x_k + dt · f(x_k, u)          Euler
        x_{k+1} = x_k + dt/6 (k1+2k2+2k3+k4)    RK4
```

Same ``f``, same ``dt``. Euler looks one step ahead. RK4 looks four times and
averages. On a falling mass with drag they diverge — that's the whole course
in one picture: **the integrator is part of the model.**

Fill three TODOs in `lab.py`: Euler, RK4, and ``point_mass_f``
(``z̈ = −g − (c/m) v|v|``).

## What will you see?

Two dots falling, plus the same clocks on ``ẍ = −x`` — Euler spirals out,
RK4 stays on the circle. `media/lab00.gif`.

![Lab 00 thumbnail](../../media/lab00_thumb.png)

## Cold Start

- State is a NumPy vector. ``f(x, u)`` returns ``ẋ``, same shape.
- Quadratic drag always opposes velocity: ``− v |v|``.
- Mechanical energy of ``ẍ = −x`` is ``½v² + ½x²`` (used by the check, not drag).

## Run

```bash
python labs/lab00_hello_state/check.py
python labs/lab00_hello_state/demo.py    # or: make lab00
```

Checks grade **your** `lab.py`. Demos fall back to `reference/` if TODOs are
open (you'll see a banner).
