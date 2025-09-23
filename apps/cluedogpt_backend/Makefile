# Make all targets depend on the target
run-dev:
	@python -m cluedogpt_backend.api.main

test:
	@pytest

test-unit:
	@pytest tests/unit

test-integration:
	@pytest tests/integration

test-integration-parallel:
	@pytest tests/integration -s -n auto

test-coverage:
	@pytest --cov=cluedogpt_backend

# Add a specific target just for linting
lint:
	@echo "Running ruff linter..."
	@ruff check .

# Format code with ruff
format:
	@echo "Formatting code with ruff..."
	@ruff format .