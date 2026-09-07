# The only entry point you need to remember.
PYTHON ?= python3

.PHONY: help test check check-ref demo random progress \
	lab00 lab01 lab02 lab03 lab04 lab05 lab06 lab07 lab08 lab09 \
	check00 check01 check02 check03 check04 check05 check06 check07 check08 check09 \
	demo00 demo01 demo02 demo03 demo04 demo05 demo06 demo07 demo08 demo09 \
	hint00 hint01 hint02 hint03 hint04 hint05 hint06 hint07 hint08 hint09

help:
	@echo "flight-school"
	@echo "  make test          pytest (core + reference checks)"
	@echo "  make check         pytest + reference lab tables"
	@echo "  make labNN         demo that lab (gif)"
	@echo "  make checkNN       grade YOUR lab.py"
	@echo "  make check-ref     all reference tables"
	@echo "  make random        pick an unchecked lab"

test:
	$(PYTHON) -m pytest -q

check: test check-ref

check-ref:
	$(PYTHON) labs/lab00_hello_state/check.py --reference
	$(PYTHON) labs/lab01_planar_dynamics/check.py --reference
	$(PYTHON) labs/lab02_into_3d/check.py --reference
	$(PYTHON) labs/lab03_cascade_pd/check.py --reference
	$(PYTHON) labs/lab04_lqr/check.py --reference
	$(PYTHON) labs/lab05_search_visualized/check.py --reference
	$(PYTHON) labs/lab06_heuristics/check.py --reference
	$(PYTHON) labs/lab07_rrt/check.py --reference
	$(PYTHON) labs/lab08_flatness/check.py --reference
	$(PYTHON) labs/lab09_time_scaling/check.py --reference

demo: demo00 demo01 demo02 demo03 demo04 demo05 demo06 demo07 demo08 demo09

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
lab05 demo05:
	$(PYTHON) labs/lab05_search_visualized/demo.py
lab06 demo06:
	$(PYTHON) labs/lab06_heuristics/demo.py
lab07 demo07:
	$(PYTHON) labs/lab07_rrt/demo.py
lab08 demo08:
	$(PYTHON) labs/lab08_flatness/demo.py
lab09 demo09:
	$(PYTHON) labs/lab09_time_scaling/demo.py

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
check05:
	$(PYTHON) labs/lab05_search_visualized/check.py
check06:
	$(PYTHON) labs/lab06_heuristics/check.py
check07:
	$(PYTHON) labs/lab07_rrt/check.py
check08:
	$(PYTHON) labs/lab08_flatness/check.py
check09:
	$(PYTHON) labs/lab09_time_scaling/check.py

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
hint05:
	$(PYTHON) labs/lab05_search_visualized/check.py --hints
hint06:
	$(PYTHON) labs/lab06_heuristics/check.py --hints
hint07:
	$(PYTHON) labs/lab07_rrt/check.py --hints
hint08:
	$(PYTHON) labs/lab08_flatness/check.py --hints
hint09:
	$(PYTHON) labs/lab09_time_scaling/check.py --hints

progress:
	@sed -n '1,80p' PROGRESS.md

random:
	$(PYTHON) tools/random_lab.py
