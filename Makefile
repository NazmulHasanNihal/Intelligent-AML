# ─────────────────────────────────────────────────────────────────────────────
# 🏛️ Intelligent-AML (C-STGB) — Developer Makefile
# ─────────────────────────────────────────────────────────────────────────────

PYTHON ?= python
PYTEST ?= pytest

.PHONY: help install install-dev test demo benchmark figures scorecard format lint clean docker-build docker-run audit-latex build-latex watch-latex

help:
	@echo "Available commands:"
	@echo "  make install        Install production dependencies"
	@echo "  make install-dev    Install developer & testing dependencies"
	@echo "  make test           Run full automated test suite (102 tests)"
	@echo "  make demo           Run live enterprise AML streaming simulation"
	@echo "  make benchmark      Run multi-dataset comparative benchmark"
	@echo "  make figures        Generate 300 DPI publication vector figures"
	@echo "  make scorecard      Display 13-dataset literature performance table"
	@echo "  make audit-latex    Run instant semantic & integrity check on LaTeX"
	@echo "  make build-latex    Compile PDF and package Overleaf ZIP archives"
	@echo "  make watch-latex    Continuous live in-IDE LaTeX watcher & auto-compiler"
	@echo "  make lint           Check code quality with ruff & black"
	@echo "  make format         Auto-format code with black & ruff"
	@echo "  make clean          Remove caches and build artifacts"
	@echo "  make docker-build   Build production Docker container"
	@echo "  make docker-run     Run containerized enterprise simulation"

audit-latex:
	$(PYTHON) src/utils/latex_validator.py

build-latex:
	$(PYTHON) scripts/watch_latex.py --once

watch-latex:
	$(PYTHON) scripts/watch_latex.py

install:
	$(PYTHON) -m pip install --upgrade pip setuptools wheel
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m pip install -e .

install-dev: install
	$(PYTHON) -m pip install -e ".[dev,agents,dashboard]"

test:
	$(PYTEST) tests/ -v --tb=short

demo:
	$(PYTHON) scripts/run_enterprise_aml_demo.py

benchmark:
	$(PYTHON) run_before_after_comparison.py

figures:
	$(PYTHON) generate_publication_figures.py

scorecard:
	$(PYTHON) print_all_datasets_report.py

lint:
	ruff check src/ tests/ scripts/
	black --check src/ tests/ scripts/

format:
	black src/ tests/ scripts/
	ruff check --fix src/ tests/ scripts/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "catboost_info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build dist *.egg-info .coverage htmlcov

docker-build:
	docker build -t intelligent-aml:latest .

docker-run:
	docker run --rm -it intelligent-aml:latest demo
