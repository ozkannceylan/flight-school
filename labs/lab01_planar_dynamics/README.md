# Lab 01 — Six States and Two Thrusts

⏱ 45 min · ⇐ Lab 00 · Phase 1

## Why now?

Lab 00 gave you a clock. This lab gives you **the** robot. Everything from PD
to SLAM to RL points at these six numbers.

## What's the idea?

A planar quadrotor in the ``y``–``z`` plane:

```
          u1 ↑           ↑ u2          world: +y right, +z up
            ●═══════════●             θ counterclockwise from upright
                 θ ↗                  u1 = right rotor, u2 = left
```

State ``x = [p_y, p_z, θ, v_y, v_z, ω]``. Input ``u = [u1, u2]`` (Newtons).

```
ẏ = v_y          ÿ = −((u1+u2)/m) sin θ
ż = v_z          z̈ =  ((u1+u2)/m) cos θ − g
θ̇ = ω           θ̈ =  L (u1 − u2) / I
```

Hover is algebra, not a search: ``θ = 0`` and ``u1 = u2 = mg/2``.

Fill two TODOs in `lab.py`: ``f(x, u)`` and ``hover_input()``.

**STOP HERE — good stopping point** after hover holds. The tumble is a
five-minute victory lap.

## What will you see?

The vehicle sits still, then a 1% rotor split sends it tumbling.
`media/lab01.gif`. This is the plant for the next 22 labs.

![Lab 01 thumbnail](../../media/lab01_thumb.png)

## Cold Start

- Lab 00: ``rollout`` / RK4 already live in ``flightlab.integrate`` (and via
  ``resolve.get("lab00")`` if you want *your* step).
- ``θ = 0`` means upright; thrust then points at +z.
- ``L`` is COM-to-rotor distance, so the moment arm of ``(u1 − u2)`` is ``L``.

## Run

```bash
python labs/lab01_planar_dynamics/check.py
python labs/lab01_planar_dynamics/demo.py    # or: make lab01
```
