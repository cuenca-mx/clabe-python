SHELL := bash
PATH := ./venv/bin:${PATH}
PYTHON = python3.7
PROJECT = clabe
isort = isort $(PROJECT) tests
black = black -S -l 79 --target-version py38 $(PROJECT) tests
PYDANTIC_V1_VENV := pydantic_v1


all: test

venv:
  	# Trying to run `pdm venv create` raises an error if the virtual env already exist.
  	# `pdm venv create` with --override option will clean all the packages installed in that venv.
	@if pdm venv list | grep -q $(PYDANTIC_V1_VENV); then \
		echo "Virtual environment $(PYDANTIC_V1_VENV) already exists. Skipping creation."; \
	else \
		echo "Creating virtual environment $(PYDANTIC_V1_VENV)."; \
		pdm venv create --with-pip --name $(PYDANTIC_V1_VENV); \
	fi

install: venv
	# Installing packages defined in pyproject.toml as normal
	pdm install -q
	# Install old Pydantic package version in a new environment
	pdm install -q --venv $(PYDANTIC_V1_VENV) --lockfile pdm-legacy.lock --override requirements-legacy.txt

test: venv clean
	# Runs pytest in each virtual environment and combine the coverage reports into one.
	pdm run pytest
	mv .coverage .cov.pydantic_v2
	pdm run --venv $(PYDANTIC_V1_VENV) pytest
	mv .coverage .cov.pydantic_v1
	pdm run coverage combine .cov.pydantic_v1 .cov.pydantic_v2
	pdm run coverage report -m
	pdm run coverage xml -o coverage.xml

format:
	pdm run $(isort)
	pdm run $(black)

lint:
	pdm run flake8 $(PROJECT) tests
	pdm run $(isort) --check-only
	pdm run $(black) --check
	pdm run mypy $(PROJECT) tests

clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -rf .cache
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf htmlcov
	rm -rf *.egg-info
	rm -f .coverage
	rm -f .coverage.*
	rm -rf build
	rm -rf dist

release: test clean
	python setup.py sdist bdist_wheel
	twine upload dist/*


.PHONY: all test format lint clean release
