SHELL := bash
PATH := ./venv/bin:${PATH}
PYTHON=python3.7


all: test

install-dev:
		pip install -q -e .[dev]

venv:
		$(PYTHON) -m venv --prompt clabe venv
		source venv/bin/activate
		pip install --quiet --upgrade pip

test: clean-pyc install-dev lint
		pytest

lint:
		pycodestyle setup.py clabe/

clean-pyc:
		find . -name '*.pyc' -exec rm -f {} +
		find . -name '*.pyo' -exec rm -f {} +
		find . -name '*~' -exec rm -f {} +


.PHONY: all install-dev test clean-pyc