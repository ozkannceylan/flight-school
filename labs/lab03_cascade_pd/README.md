# Lab 03 — Cascade PD

⏱ 45 min · ⇐ Lab 01 · Phase 1

## Why now?

Open-loop hover is an equilibrium, not a controller. A nudge still tumbles
you. Eigenvalues decide whether a loop will pull you back.

## What's the idea?

Linearize ``ẋ = f(x,u)`` about hover — two Jacobians ``A, B``. Then wrap two
PD loops around the same plant:

```
outer (slow)     ay, az  →  θ_des, T
inner (fast)     θ_des   →  differential thrust
```

The inner loop has to be **at least 5× faster** (``√(kp_θ / kp_y) ≥ 5``) or
the outer loop commands a θ the vehicle hasn't reached yet.

**STOP HERE — good stopping point** after TODO 1: if ``A[3,2] ≈ −g`` you
already understand the linearization. The cascade is a second sitting.

## What will you see?

A 3×3 gain sweep. Sluggish, tuned, unstable — side by side. `media/lab03.gif`.

![Lab 03 thumbnail](../../media/lab03_thumb.png)

## Cold Start

- State ``[p_y, p_z, θ, v_y, v_z, ω]``, hover ``u = [mg/2, mg/2]``.
- Small-angle: ``ÿ ≈ −g θ``. That's why ``θ_des = −ay / g``.
- ``flightlab.control.CascadeGains`` is just a container. You fill the policy.

## Run

```bash
python labs/lab03_cascade_pd/check.py
python labs/lab03_cascade_pd/demo.py
```
