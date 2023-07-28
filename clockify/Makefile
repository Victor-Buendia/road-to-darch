PROJECT_NAME=clockify

.PHONY: help
help:
	@echo "******* COMMANDS AVAILABLE ON THIS MAKEFILE *******"
	@echo
	@echo "setup: Install project's dependencies using Poetry"
	@echo "lint: Lint project's src/ and terraform/ directory files"
	@echo "lint-check: Check src/ and terraform/ directory files linting"
	@echo
	@echo "***************************************************"

.PHONY: setup
setup:
	poetry install

.PHONY: lint
lint:
	black src
	terraform fmt -recursive .

.PHONY: lint-check
lint-check:
	@res=$$(terraform fmt -check -recursive .); \
	if [ $$? -eq 0 ]; then \
		echo "Code is properly formatted"; \
		exit 0; \
	else \
		echo "Terraform linting required for the following files:"; \
		echo "$$res"; \
		exit 1; \
	fi
	black src --check

.PHONY: coverage-test
coverage-test:
	rm -rf htmlcov
	PYTHONPATH=$(PYTHONPATH):src/ coverage run --omit="src/tests/*,*/__init__.py,/usr/*"  -m pytest src/tests
	coverage html
	google-chrome htmlcov/index.html

	