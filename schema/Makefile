MAKEFILE_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
SCHEMA_DIR := $(MAKEFILE_DIR)
BACKEND_DIR := $(MAKEFILE_DIR)../backend
FRONTEND_DIR := $(MAKEFILE_DIR)../frontend

.PHONY: validate
validate:
	docker run --rm -v .:/spec redocly/cli lint /spec/schema.yml

# NOTE: datamode-codegen cannot parse $ref, that refers to external files
.PHONY: oapi-gen
oapi-gen:
	cd $(BACKEND_DIR) && \
	uv run datamodel-codegen \
		--input $(SCHEMA_DIR)schema.yml \
		--input-file-type openapi \
		--output-model-type pydantic_v2.BaseModel \
		--output $(BACKEND_DIR)/app/api/schemas/generated.py \
		--use-schema-description
	cd $(FRONTEND_DIR) && pnpm run oapi-gen
