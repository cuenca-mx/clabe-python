SHELL := bash
PATH := ./venv/bin:${PATH}
PYTHON = python3.7
PROJECT = clabe
isort = isort $(PROJECT) tests setup.py
black = black -S -l 79 --target-version py38 $(PROJECT) tests setup.py


all: test

venv:
	$(PYTHON) -m venv --prompt $(PROJECT) venv
	pip install -qU pip

venv2:
	pdm venv create --with-pip --name pydanticv1
	pdm venv create --with-pip --name pydanticv2

install:
	pip install -qU -r requirements.txt

install_all:
	eval $(pdm venv activate pydanticv1)
	pip install -qU -r requirements-legacy.txt
	deactivate
	eval $(pdm venv activate pydanticv2)
	pip install -qU -r requirements.txt
	deactivate

install-test: install
	pip install -qU -r requirements-test.txt

test: clean install-test lint
	pytest

format:
	$(isort)
	$(black)

lint:
	flake8 $(PROJECT) tests setup.py
	$(isort) --check-only
	$(black) --check
	mypy $(PROJECT) tests

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


.PHONY: all install-test test format lint clean release
