.PHONY: help run run-bash run-root-bash build

# Default values
DEFAULT_MODEL = google/gemini-2.5-pro-exp-03-25:free

help:
	@echo "MYDER HELP"
	@echo ""
	@echo "GENERAL:"
	@echo "  help                      Show this help message"
	@echo "  build                     Build Docker image locally"
	@echo ""
	@echo "RUNNING:"
	@echo "  run                       Run with default Gemini 2.5 Pro model"
	@echo "  run MODEL=name            Use specified model (via OpenRouter)"
	@echo "  run NOMOUNT=1             Don't mount current directory"
	@echo "  run FORCE_YES=1           Auto-confirm all prompts (dangerous)"
	@echo ""
	@echo "  Examples: make run MODEL=anthropic/claude-3-opus-20240229"
	@echo "            make run MODEL=claude-3-haiku-20240307 FORCE_YES=1 NOMOUNT=1"
	@echo ""
	@echo "SHELL ACCESS:"
	@echo "  run-bash                  Start bash shell in container"
	@echo "  run-bash NOMOUNT=1        Start bash shell without mounting directory"
	@echo "  run-root-bash             Start bash shell as root"
	@echo "  run-root-bash NOMOUNT=1   Start bash shell as root without mounting"
	@echo ""

# Determine model to use
MODEL_ARG = $(if $(MODEL),openrouter/$(MODEL),openrouter/$(DEFAULT_MODEL))

# Determine if --yes-always flag should be included
YES_ARG = $(if $(filter 1,$(FORCE_YES)),--yes-always,)

# Determine if volume mount should be included
VOLUME_ARG = $(if $(filter 1,$(NOMOUNT)),,--volume $(PWD):/app)

run:
	docker run --rm -it \
		--env-file=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))/.env \
		$(VOLUME_ARG) \
		--workdir=/app \
		myder \
		--analytics-disable \
		$(YES_ARG) \
		--model $(MODEL_ARG)

run-bash:
	docker run --rm -it \
		--env-file=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))/.env \
		$(VOLUME_ARG) \
		--workdir=/app \
		--entrypoint /bin/bash \
		myder

run-root-bash:
	docker run --rm -it \
		--user 0:0 \
		--env-file=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))/.env \
		$(VOLUME_ARG) \
		--workdir=/app \
		--entrypoint /bin/bash \
		myder

build:
	cd $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST)))) && \
	docker build -t myder .

