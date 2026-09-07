# The only entry point you need to remember.
PYTHON ?= python3

.PHONY: help test check check-ref demo \
	lab00 lab01 check00 check01 check00-ref check01-ref \
	demo00 demo01 hint00 hint01 \
	random progress

help:
	@echo "flight-school"
	@echo "  make test          pytest (core + reference checks)"
	@echo "  make check         same as test + reference lab tables"
	@echo "  make lab00         demo Lab 00 (gif)"
	@echo "  make lab01         demo Lab 01 (gif)"
	@echo "  make check00       grade YOUR labs/lab00_hello_state/lab.py"
	@echo "  make check01       grade YOUR labs/lab01_planar_dynamics/lab.py"
	@echo "  make demo          both demos"
	@echo "  make random        pick an unchecked lab"
	@echo "  make progress      show PROGRESS.md"

test:
	$(PYTHON) -m pytest -q

check: test check-ref

check-ref:
	$(PYTHON) labs/lab00_hello_state/check.py --reference
	$(PYTHON) labs/lab01_planar_dynamics/check.py --reference

demo: demo00 demo01

lab00 demo00:
	$(PYTHON) labs/lab00_hello_state/demo.py

lab01 demo01:
	$(PYTHON) labs/lab01_planar_dynamics/demo.py

check00:
	$(PYTHON) labs/lab00_hello_state/check.py

check01:
	$(PYTHON) labs/lab01_planar_dynamics/check.py

check00-ref:
	$(PYTHON) labs/lab00_hello_state/check.py --reference

check01-ref:
	$(PYTHON) labs/lab01_planar_dynamics/check.py --reference

hint00:
	$(PYTHON) labs/lab00_hello_state/check.py --hints

hint01:
	$(PYTHON) labs/lab01_planar_dynamics/check.py --hints

progress:
	@sed -n '1,80p' PROGRESS.md

random:
	$(PYTHON) tools/random_lab.py
