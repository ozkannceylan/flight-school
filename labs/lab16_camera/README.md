# Lab 16 — The Camera Is a Matrix

⏱ 45 min · ⇐ Lab 01 · Phase 4

## Why now?

You can fly and you can estimate. Vision starts with the cheapest model that
is still true: a matrix.

## What's the idea?

A downward camera on the Lab 01 quadrotor. World point ``X``, camera
``(R, C)``, calibration ``K``:

```
Xc = R (X − C)
u  = fx Xc/Zc + cx
v  = fy Yc/Zc + cy
```

Given known pose and correspondences, ``K`` is two linear least-squares
problems. Inverse projection is a *ray* — depth is free. That's the
ambiguity.

## What will you see?

A synthetic camera view of the ground, landmarks over the texture. `media/lab16.gif`.

![Lab 16 thumbnail](../../media/lab16_thumb.png)

## Cold Start

- World: ``+y`` right, ``+z`` up. Camera looks along ``−body z``.
- ``camera_from_planar(py, pz, θ)`` and ``to_camera`` are provided.
- Default ``K`` has ``fx = fy = 200``, principal point ``(80, 60)``.

## STOP HERE — good stopping point

``project`` green is enough to see the picture. Calibration is two ``lstsq`` calls.

## Run

```bash
python labs/lab16_camera/check.py
python labs/lab16_camera/demo.py
```
