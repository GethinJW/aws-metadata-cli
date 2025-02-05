.ONESHELL:

VENV_PATH:=venv

.PHONY: build
build:
	python3 -m venv $(VENV_PATH) && \
	make deps

.PHONY: deps
deps:
	. ./$(VENV_PATH)/bin/activate && \
	python3 scripts/verify_packages.py || \
	pip install -r requirements.txt

.PHONY: run
run: deps
	. ./$(VENV_PATH)/bin/activate && \
	python src/main.py
