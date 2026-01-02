.PHONY: format
format:
	uv run isort ./app ./tests
	uv run black ./app ./tests

.PHONY: lint
lint:
	uv run flake8 ./app --ignore=E203,E501
	uv run mypy ./app

.PHONY: test
test:
	uv run pytest ./tests

.PHONY: migrate
migrate:
	docker compose run --rm bookmark-searcher-migration
