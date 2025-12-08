.PHONY: format
format:
	uv run isort ./app
	uv run black ./app

.PHONY: lint
lint:
	uv run flake8 ./app --ignore=E501
	uv run mypy ./app

.PHONY: migrate
migrate:
	docker compose run --rm bookmark-searcher-migration
