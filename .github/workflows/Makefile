# Makefile

.PHONY: install run clean test notebook

# Setup the Python virtual environment
venv:
	python3 -m venv venv

# Install dependencies for a full development environment
install: venv
	. venv/bin/activate && pip install -r requirements.txt

# Run the entire automated analysis pipeline
run:
	. venv/bin/activate && python scripts/run_pipeline.py

# Launch the JupyterLab environment
notebook:
	. venv/bin/activate && jupyter lab

# Run all code quality checks and unit tests locally
test:
	# 1. Format code with Black
	black .
	# 2. Lint with flake8
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=88 --statistics
	# 3. Run unit tests with pytest
	pytest

# Clean up generated files and caches
clean:
	rm -rf reports/*
	rm -f mlflow.db
	mkdir -p reports/figures
	touch reports/.gitkeep reports/figures/.gitkeep
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache
	rm -rf mlruns