VENV := .venv
PYTHON := $(VENV)/bin/python
PRE_COMMIT := $(VENV)/bin/pre-commit

.PHONY: setup check

setup:
	python3 -m venv $(VENV)
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt
	$(PRE_COMMIT) install

check:
	$(PRE_COMMIT) run --all-files
