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

test: clean-pyc lint
		python setup.py test

lint:
		pycodestyle setup.py test_clabe.py clabe/

clean-pyc:
		find . -name '*.pyc' -exec rm -f {} +
		find . -name '*.pyo' -exec rm -f {} +
		find . -name '*~' -exec rm -f {} +

release: clean-pyc
		python setup.py sdist bdist_wheel
		twine upload dist/*


.PHONY: all install-dev release test clean-pyc