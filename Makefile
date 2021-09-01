
.PHONY: help lint test deps

black:
	black reducto

lint:
	black --check reducto
	mypy --strict reducto

documentation:
	(cd ${PWD}/docs && make html)

deps:  ## Install dependencies
	python -m pip install --upgrade pip
	pip install flit

install: deps  ## Install the package locally
	flit install --deps develop

test:  ## Run tests
	pytest --cov=reducto --cov-report=xml

help:
	@echo "docs: Generate docs."
	@echo "deps: Install dependencies."
	@echo "install: Install the package. Runs flit install."
	@echo "test: Run the unit tests with coverage."
