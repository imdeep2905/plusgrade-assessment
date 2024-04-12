.PHONY: test coverage lint typecheck

test:
	poetry run pytest --cov=app

coverage:
	poetry run pytest --cov=app --cov-report=html

lint:
	poetry run ruff check app/* --fix --select I

typecheck:
	poetry run mypy app/ --exclude tests/
