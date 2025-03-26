.PHONY: help run run-bash run-bash-no-mount run-root-bash run-root-bash-no-mount run-model run-model-no-mount build

help:
	@echo ""
	@echo "╔══════════════════════════════════════════════════════════════════════════════╗"
	@echo "║                                 MYDER HELP                                    ║"
	@echo "╚══════════════════════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "  GENERAL COMMANDS:"
	@echo "  ────────────────────────────────────────────────────────────────────────────"
	@echo "    help                      Show this help message"
	@echo "    build                     Build and update Docker image locally"
	@echo ""
	@echo "  RUNNING COMMANDS:"
	@echo "  ────────────────────────────────────────────────────────────────────────────"
	@echo "    run                       Run Aider with default Gemini 2.5 Pro model"
	@echo "    run-model MODEL=name      Run Aider with specified model (via OpenRouter)"
	@echo "    run-model-no-mount MODEL=name"
	@echo "                              Run Aider with specified model without mounting"
	@echo "                              current directory"
	@echo ""
	@echo "  SHELL ACCESS COMMANDS:"
	@echo "  ────────────────────────────────────────────────────────────────────────────"
	@echo "    run-bash                  Start bash shell inside Docker container"
	@echo "    run-bash-no-mount         Start bash shell inside Docker container without"
	@echo "                              mounting current directory"
	@echo "    run-root-bash             Start bash shell as root inside Docker container"
	@echo "    run-root-bash-no-mount    Start bash shell as root without mounting"
	@echo "                              current directory"
	@echo ""

run:
	docker run --rm -it \
		--env-file=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))/.env \
		--volume $(PWD):/app \
		--workdir=/app \
		myder \
		--analytics-disable \
		--model openrouter/google/gemini-2.5-pro-exp-03-25:free

run-bash:
	docker run --rm -it \
		--env-file=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))/.env \
		--volume $(PWD):/app \
		--workdir=/app \
		--entrypoint /bin/bash \
		myder

run-bash-no-mount:
	docker run --rm -it \
		--env-file=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))/.env \
		--workdir=/app \
		--entrypoint /bin/bash \
		myder

run-root-bash:
	docker run --rm -it \
		--user 0:0 \
		--env-file=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))/.env \
		--volume $(PWD):/app \
		--workdir=/app \
		--entrypoint /bin/bash \
		myder

run-root-bash-no-mount:
	docker run --rm -it \
		--user 0:0 \
		--env-file=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))/.env \
		--workdir=/app \
		--entrypoint /bin/bash \
		myder
		
run-model:
	@if [ -z "$(MODEL)" ]; then \
		echo "Error: MODEL parameter is required. Usage: make run-model MODEL=your_model_name"; \
		exit 1; \
	fi
	docker run --rm -it \
		--env-file=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))/.env \
		--volume $(PWD):/app \
		--workdir=/app \
		myder \
		--analytics-disable \
		--model openrouter/$(MODEL)

run-model-no-mount:
	@if [ -z "$(MODEL)" ]; then \
		echo "Error: MODEL parameter is required. Usage: make run-model MODEL=your_model_name"; \
		exit 1; \
	fi
	docker run --rm -it \
		--env-file=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))/.env \
		--workdir=/app \
		myder \
		--analytics-disable \
		--model openrouter/$(MODEL)

build:
	cd $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST)))) && \
	Docker build -t myder .

