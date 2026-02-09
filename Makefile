# Self-documenting: run "make" or "make help" to list targets.
.PHONY: help install install-dev check lint format typecheck test

help:
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

install: ## Install package in editable mode (for MCP / latest source)
	pip install -e .

install-dev: ## Install in editable mode with dev deps (lint, typecheck, test)
	pip install -e ".[dev]"

check: lint typecheck test ## Run all checks (lint, typecheck, tests)

lint: ## Run ruff check and format check
	ruff check src tests
	ruff format --check src tests

format: ## Format code with ruff
	ruff format src tests

typecheck: ## Run mypy on src
	mypy src/

test: ## Run pytest
	pytest
