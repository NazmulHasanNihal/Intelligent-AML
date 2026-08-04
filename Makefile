# ──────────────────────────────────────────────────
# Intelligent AML — Makefile
# Single entry-point for common development commands
# ──────────────────────────────────────────────────

.PHONY: install test lint sync-kaggle remote ui clean

## Install local control-plane dependencies
install:
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install -e ".[dev]"

## Run all unit tests
test:
	pytest tests/ -v --tb=short

## Lint and format source code
lint:
	ruff check src/ tests/
	black --check src/ tests/

## Format source code (auto-fix)
format:
	black src/ tests/
	ruff check --fix src/ tests/

## Pull trained artifacts from Kaggle
sync-kaggle:
	python src/utils/kaggle_sync.py

## Run an IDE notebook/script on Kaggle GPU and pull outputs back to this PC.
## Usage: make remote TARGET=notebooks/Layer1_Ingestion/01_Layer1_Data_Ingestion_v4.ipynb
remote:
	python src/utils/run_remote.py run --target $(TARGET)

## Launch the Streamlit dashboard
ui:
	streamlit run src/ui/app.py

## Remove caches and generated files
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	rm -rf .ruff_cache build dist *.egg-info
