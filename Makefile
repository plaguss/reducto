
.PHONY: help lint test deps

lint:
	echo "Not defined"

docs:
	echo "Not defined"

deps:  ## Install dependencies
	python -m pip install --upgrade pip
	python -m pip install pytest==6.2.3 pytest-cov==2.11.1

test:  ## Run tests
	pytest --cov=reducto

help:
	echo "Not defined"
