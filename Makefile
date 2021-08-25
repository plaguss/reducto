
.PHONY: help lint test deps

black:
	black reducto

check_black:
	black --check reducto

documentation:
	(cd ${PWD}/docs && make html)

deps:  ## Install dependencies
	python -m pip install --upgrade pip
	python -m pip install pytest==6.2.3 pytest-cov==2.11.1

install:  ## Install the package locally
	flit install

test:  ## Run tests
	pytest --cov=reducto

help:
	@echo "docs: Generate docs."
	@echo "deps: Install dependencies."
	@echo "install: Install the package. Runs flit install."
	@echo "test: Run the unit tests with coverage."
