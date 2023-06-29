PROJECT_NAME=clockify

.PHONY: setup
setup:
	poetry install

.PHONY: lint
lint:
	black src/

.PHONY: lint-check
lint-check:
	black src/ --check
