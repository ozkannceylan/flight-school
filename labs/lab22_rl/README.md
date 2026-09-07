# Lab 22 — Learning to Hover Without Being Told How

⏱ 45 min · ⇐ Labs 04, 19 · Phase 4

## Why now?

You already have an optimal linear controller. RL's job in this course is
one honest comparison: how many samples did it take to *not* beat LQR?

## What's the idea?

A linear policy ``u = u_eq − K(x − x_eq)``. CEM samples the 12 gains,
keeps the elite, repeats.

Reward is ``−(y² + (z−1)² + 0.01‖u−u_eq‖²)``. That's just Lab 04's cost
with a minus sign.

The plot has a flat dashed line labelled **"LQR, zero samples."** That
line is the lesson.

## What will you see?

A learning curve that approaches, and does not cross, the LQR line. `media/lab22.gif`.

![Lab 22 thumbnail](../../media/lab22_thumb.png)

## Cold Start

- ``episode_return`` is a short RK4 rollout at ``dt=0.02``. Lab 04's LQR
  has a fast attitude pole; ``dt=0.05`` makes that baseline look drunk.
  Clip thrust.
- Elite = highest scores (returns are negative; closer to zero is better).
- ``get("lab04")`` for the baseline K.

## STOP HERE — good stopping point

A working ``episode_return`` plus ``cem_update`` is enough to run CEM by hand.

## Run

```bash
python labs/lab22_rl/check.py
python labs/lab22_rl/demo.py
```
