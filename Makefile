# The only entry point you need to remember.
PYTHON ?= python3

.PHONY: help test check check-ref demo \
	lab00 lab01 lab02 lab03 lab04 \
	check00 check01 check02 check03 check04 \
	check00-ref check01-ref check02-ref check03-ref check04-ref \
	demo00 demo01 demo02 demo03 demo04 \
	hint00 hint01 hint02 hint03 hint04 \
	random progress

help:
	@echo "flight-school"
	@echo "  make test          pytest (core + reference checks)"
	@echo "  make check         same as test + reference lab tables"
	@echo "  make lab00..lab04  demo that lab (gif)"
	@echo "  make check00       grade YOUR labs/lab00_hello_state/lab.py"
	@echo "  make check01..04   grade YOUR lab.py for that number"
	@echo "  make demo          Labs 00–04 demos"
	@echo "  make random        pick an unchecked lab"
	@echo "  make progress      show PROGRESS.md"

test:
	$(PYTHON) -m pytest -q

check: test check-ref

check-ref:
	$(PYTHON) labs/lab00_hello_state/check.py --reference
	$(PYTHON) labs/lab01_planar_dynamics/check.py --reference
	$(PYTHON) labs/lab02_into_3d/check.py --reference
	$(PYTHON) labs/lab03_cascade_pd/check.py --reference
	$(PYTHON) labs/lab04_lqr/check.py --reference

demo: demo00 demo01 demo02 demo03 demo04

lab00 demo00:
	$(PYTHON) labs/lab00_hello_state/demo.py

lab01 demo01:
	$(PYTHON) labs/lab01_planar_dynamics/demo.py

lab02 demo02:
	$(PYTHON) labs/lab02_into_3d/demo.py

lab03 demo03:
	$(PYTHON) labs/lab03_cascade_pd/demo.py

lab04 demo04:
	$(PYTHON) labs/lab04_lqr/demo.py

check00:
	$(PYTHON) labs/lab00_hello_state/check.py

check01:
	$(PYTHON) labs/lab01_planar_dynamics/check.py

check02:
	$(PYTHON) labs/lab02_into_3d/check.py

check03:
	$(PYTHON) labs/lab03_cascade_pd/check.py

check04:
	$(PYTHON) labs/lab04_lqr/check.py

check00-ref:
	$(PYTHON) labs/lab00_hello_state/check.py --reference

check01-ref:
	$(PYTHON) labs/lab01_planar_dynamics/check.py --reference

check02-ref:
	$(PYTHON) labs/lab02_into_3d/check.py --reference

check03-ref:
	$(PYTHON) labs/lab03_cascade_pd/check.py --reference

check04-ref:
	$(PYTHON) labs/lab04_lqr/check.py --reference

hint00:
	$(PYTHON) labs/lab00_hello_state/check.py --hints

hint01:
	$(PYTHON) labs/lab01_planar_dynamics/check.py --hints

hint02:
	$(PYTHON) labs/lab02_into_3d/check.py --hints

hint03:
	$(PYTHON) labs/lab03_cascade_pd/check.py --hints

hint04:
	$(PYTHON) labs/lab04_lqr/check.py --hints

progress:
	@sed -n '1,80p' PROGRESS.md

random:
	$(PYTHON) tools/random_lab.py
