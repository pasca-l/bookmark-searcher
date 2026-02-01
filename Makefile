MAKEFILE_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
BACKEND_DIR := $(MAKEFILE_DIR)/backend
FRONTEND_DIR := $(MAKEFILE_DIR)/frontend

.PHONY: run-local
run-local:
	trap 'kill 0; docker compose down' EXIT; \
	$(MAKE) run-backend-local & \
	$(MAKE) run-frontend-local & \
	wait

.PHONY: run-backend-local
run-backend-local:
	docker compose up -d bookmark-searcher-postgres
	cd $(BACKEND_DIR) && uv run python3 -m app.main

.PHONY: run-frontend-local
run-frontend-local:
	cd $(FRONTEND_DIR) && pnpm run dev
