.PHONY: install
## Install the dependencies
install:
	poetry install

.PHONY: lint
## Run pre-commit checks
lint:
	poetry run pre-commit run --all-files
