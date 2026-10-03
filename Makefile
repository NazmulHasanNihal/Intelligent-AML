# =============================================================================
# Intelligent-AML Master Makefile
# Institutional-grade AML Decision Support & Graph Forensic Engine
# =============================================================================

.PHONY: help dev test seed build lint docker-up docker-down clean

help:
	@echo "Intelligent-AML Build and Orchestration Commands:"
	@echo "  make dev         - Launch both FastAPI backend and Vite frontend concurrently"
	@echo "  make test        - Run rigorous invariant and microservice tests (pytest)"
	@echo "  make seed        - Re-seed relational persistence with mathematically consistent data"
	@echo "  make build       - Build production frontend bundle (Vite + Tailwind)"
	@echo "  make lint        - Run ruff code quality checks"
	@echo "  make docker-up   - Start Postgres, Backend, and Frontend via Docker Compose"
	@echo "  make docker-down - Tear down running Docker Compose containers"

dev:
	@echo "Starting Intelligent-AML in development mode..."
	python -m uvicorn src.engine.api:app --host 0.0.0.0 --port 8000 --reload &
	cd frontend && npm run dev

test:
	@echo "Running backend test suite and mathematical invariant checks..."
	pytest tests/test_invariants.py tests/test_dashboard_and_api.py -v

seed:
	@echo "Seeding data with mathematical single source of truth..."
	python -c "from src.engine.persistence import db, verify_audit_chain; print('Seeded cases:', len(db.cases)); print('Chain status:', db.verify_audit_chain())"

build:
	@echo "Compiling frontend production bundle..."
	cd frontend && npm run build

lint:
	@echo "Running lint and format checks..."
	ruff check src/ tests/

docker-up:
	@echo "Spreading core services (Postgres, Backend, Frontend)..."
	docker compose up -d postgres backend frontend

docker-down:
	@echo "Stopping Docker containers..."
	docker compose down

clean:
	@echo "Cleaning up caches and build artifacts..."
	rm -rf .pytest_cache frontend/dist results/reports/*
