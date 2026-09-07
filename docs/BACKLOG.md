---
title: "Fable BACKLOG — Princeton IRoM sim labs"
date: 2026-09-07
tags: [princeton-intro-robotics, fable, backlog]
status: locked
source: "https://claude.ai/chat/aecad762-5224-4d27-9dba-9da314d33814"
---

# BACKLOG

# BACKLOG

## Repo name

**Recommended: `flight-school`**

> **One-liner:** 24 hands-on simulation labs that teach robotics from PD control to SLAM to RL — pure
> NumPy, one quadrotor, no hardware required.

Why: memorable, pronounceable, says "learning" and "flying" without saying "course project." Reads
well as a GitHub URL and as a video series title. Not tied to one university or one semester, so it
survives being a public artifact for years.

**Alternates:**
| Name | Note |
|---|---|
| `quadrotor-from-scratch` | Most searchable, most descriptive, least memorable. Strong second. |
| `irom-labs` | Precise, but opaque to anyone outside Princeton. Poor public choice. |
| `one-quadrotor` | Names the core architectural idea (ADR-002). Cute, but obscure until explained. |

---

## Priority tiers

**P0** — blocks a phase exit. **P1** — real value, schedulable. **P2** — nice, non-blocking. **P3** —
explicitly deferred; recorded so it stops occupying attention.

---

### P0 — must exist

| # | Item | Phase |
|---|---|---|
| 1 | `Plant` protocol design, written down before Lab 00 | 0 |
| 2 | Graded-check runner with partial credit + per-criterion hints | 0 |
| 3 | Student→reference resolver with visible warning banner | 0 |
| 4 | `tools/new_lab.py` scaffolder | 0 |
| 5 | Clean-clone → gif in <2 min, stopwatch-verified | 0 |
| 6 | `flightlab/worlds/` — grids, obstacles, terrain costmaps | 2 |
| 7 | Lab 08 fallback test: delete `lab04/lab.py`, Lab 08 still flies | 2 |
| 8 | `flightlab/sensors/` — beam range model, IMU with bias | 3 |
| 9 | `flightlab/render/` — pinhole, procedural texture, analytic flow GT | 4 |
| 10 | Lab 15 scope fence: 2D pose-graph only, one loop closure | 3 |

### P1 — high value, schedulable

| # | Item | Phase |
|---|---|---|
| 11 | `make random` — picks an unlocked, unfinished lab | 0 |
| 12 | Cold Start block enforced in every lab README (template + lint) | 0 |
| 13 | `STOP HERE` markers placed in every lab >30 min | 1+ |
| 14 | Public README gif grid — 24 thumbnails | 5 |
| 15 | `tools/studypack.py` — per-phase NotebookLM source pack | 5 |
| 16 | `content/L01–L24.md` derivations backfilled | 5 |
| 17 | Cold-start audit: re-enter every lab in ≤60 s | 5 |
| 18 | Lab 21 dual backend — NumPy default, `BACKEND=torch` flag | 4 |
| 19 | CI runs all 24 reference impls on every push | 0 |
| 20 | Deterministic media regeneration at phase boundaries | 5 |

### P2 — nice to have

| # | Item |
|---|---|
| 21 | `tools/screencast.py` — README sections → timed narration beats |
| 22 | PyBullet parity layer + model-mismatch comparison lab |
| 23 | Interactive gain-slider widget for Labs 03/04 (matplotlib widgets, no new deps) |
| 24 | A single `make everything` regression that flies the full Phase-1→2 stack end to end |
| 25 | Per-lab timing telemetry — how long labs *actually* take vs. the 45-min budget |
| 26 | `flightlab/dynamics/unicycle` polish, for cleaner SLAM labs |
| 27 | Solutions diff view: `make compare04` overlays student vs. reference trajectories |

### P3 — deferred, deliberately

| # | Item | Why deferred |
|---|---|---|
| 28 | Crazyflie hardware bridge | Reward, not prerequisite. Only after Phase 5 ships. |
| 29 | MuJoCo backend | PyBullet parity (#22) covers the lesson at lower cost. |
| 30 | FastSLAM / landmark SLAM | Lab 15 is already the largest lab. Separate bonus lab at best. |
| 31 | Full bundle adjustment / visual odometry lab | Beyond course scope; a whole second repo. |
| 32 | PPO or SAC implementation | Lab 22's job is the honest LQR comparison, not an RL library. |
| 23 | Web-based browser demos (Pyodide) | Distribution problem, not a learning problem. |
| 34 | Auto-generated narration audio | Uncanny; you'll rewrite it. Beats only (#21). |
| 35 | Multi-agent / swarm extension | Genuinely interesting, genuinely out of scope. |

---

## Open questions to resolve before Phase 0

1. **Attitude representation in Lab 02** — Euler angles (shows the singularity, which is pedagogically
   useful) or quaternions (correct, but a whole lesson of its own)? *Leaning Euler, with the
   singularity as the deliverable.*
2. **Does `check.py` need a numeric score, or is the pass/fail table plus partial credit enough?* A
   score invites optimizing the score. *Leaning: no score.*
3. **Is `reference/` a separate installable package or an in-repo directory?* Separate package makes
   spoilers marginally harder but adds install friction. *Leaning: in-repo directory, per ADR-003.*
4. **Do lecture derivations live in `content/` or in `labs/*/notes.md`?** Splitting them creates a
   lookup problem. *Leaning: `content/` is canonical, `notes.md` is yours and freeform.*
