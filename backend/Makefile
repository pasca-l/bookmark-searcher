.PHONY: format
format:
	uv run ruff format ./app ./tests

.PHONY: lint
lint:
	uv run ruff check ./app

.PHONY: test
test:
	uv run pytest ./tests

.PHONY: migrate
migrate:
	docker compose run --rm bookmark-searcher-migration
