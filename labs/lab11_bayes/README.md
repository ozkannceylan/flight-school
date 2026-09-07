# Lab 11 — Prior, Likelihood, Posterior

⏱ 40 min · ⇐ Lab 10 · Phase 3

## Why now?

Lab 10's set is "possible / impossible." Weights let you say *how* possible.
That's the discrete Bayes filter — same two arrows, now with numbers.

## What's the idea?

A 1-D corridor. Some cells are doors. You try to step right each tick.

```
predict   bel ← motion kernel (stay 0.2 / forward 0.8)
update    bel ← bel ⊙ p(z|x)   then divide by the sum
```

p(z=door | at a door) = 0.9. p(z=door | empty) = 0.2. Invert those two
numbers and the same data makes a confident, wrong map. Log that — Lab 23
will ask.

## What will you see?

Three stacked histograms: prior, likelihood, posterior. `media/lab11.gif`.

![Lab 11 thumbnail](../../media/lab11_thumb.png)

## Cold Start

- ``corridor_lab11()`` → ``(doors: bool[n], start)``.
- Belief is a length-``n`` vector that must sum to 1 after every step.
- No quadrotor. This is the 1-D cartoon of every filter you will write next.

## Run

```bash
python labs/lab11_bayes/check.py
python labs/lab11_bayes/demo.py
```
