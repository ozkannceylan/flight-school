---
title: "Fable session — Princeton IRoM sim lab plan lock"
date: 2026-09-07
tags: [princeton-intro-robotics, fable, architecture, plan]
status: locked
source: "Claude Opus 5 High · https://claude.ai/chat/aecad762-5224-4d27-9dba-9da314d33814"
---

# Fable plan lock (2026-09-07)

**Session:** https://claude.ai/chat/aecad762-5224-4d27-9dba-9da314d33814  
**Model:** Opus 5 High · clean chat-only (no amr-agent, no vault-as-repo)  
**Hermes research:** [[../research/2026-09-07-sim-pedagogy-deep]]

## Locked decisions
1. **Plant spine:** planar quadrotor for (almost) all labs; unicycle secondary for grid/SLAM; 3D quad secondary.
2. **Sim stack:** NumPy + Matplotlib 2D-first. PyBullet/MuJoCo optional Phase 5 parity. Crazyflie stretch only.
3. **Pedagogy:** Explain → Tinker → Check (+ demo gif). One editable `lab.py` per lab.
4. **Repo name (Fable):** `flight-school` — alternate if taken: `princeton-irom-sims`.
5. **NotebookLM + video:** design-only now; per-*phase* studypack → NotebookLM; screencast demos in Phase 5.

## Artifacts in this folder
- [[ARCHITECTURE]]
- [[LECTURE_LAB_MAP]]
- [[PLAN]]
- [[BACKLOG]]
- `2026-09-07-fable-raw.md` — full session dump

## Next
READY_FOR_REPO → CoS creates GitHub → land docs → Cursor labs. Gemini Deep Research after this filing.
