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

test: clean install-dev lint
		python setup.py test

lint:
		pycodestyle setup.py test_clabe.py clabe/

clean:
		find . -name '*.pyc' -exec rm -f {} +
		find . -name '*.pyo' -exec rm -f {} +
		find . -name '*~' -exec rm -f {} +
		rm -rf build dist clabe.egg-info

.PHONY: all install-dev release test clean-pyc
