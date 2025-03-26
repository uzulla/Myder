.PHONY: run pull run-bash run-root-bash run-model

help:
	@echo "Available commands:"
	@echo "  help                   - Show this help message"
	@echo "  run                    - Run Aider with default Gemini 2.5 Pro model"
	@echo "  run-model MODEL=name   - Run Aider with specified model (via OpenRouter)"
	@echo "  run-bash               - Start bash shell inside Docker container"
	@echo "  run-root-bash          - Start bash shell as root inside Docker container"
	@echo "  run-root-bash-no-mount - Start bash shell as root without mounting current directory"
	@echo "  pull                   - Update Docker image to the latest version"

run:
	docker run --rm -it \
		--env-file=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))/.env \
		--volume $(PWD):/app \
		--workdir=/app \
		paulgauthier/aider-full \
		--analytics-disable \
		--model openrouter/google/gemini-2.5-pro-exp-03-25:free

run-bash:
	docker run --rm -it \
		--env-file=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))/.env \
		--volume $(PWD):/app \
		--workdir=/app \
		--entrypoint /bin/bash \
		paulgauthier/aider-full

run-root-bash:
	docker run --rm -it \
		--user 0:0 \
		--env-file=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))/.env \
		--volume $(PWD):/app \
		--workdir=/app \
		--entrypoint /bin/bash \
		paulgauthier/aider-full

run-root-bash-no-mount:
	docker run --rm -it \
		--user 0:0 \
		--env-file=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))/.env \
		--workdir=/app \
		--entrypoint /bin/bash \
		paulgauthier/aider-full
		
run-model:
	@if [ -z "$(MODEL)" ]; then \
		echo "Error: MODEL parameter is required. Usage: make run-model MODEL=your_model_name"; \
		exit 1; \
	fi
	docker run --rm -it \
		--env-file=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))/.env \
		--volume $(PWD):/app \
		--workdir=/app \
		paulgauthier/aider-full --analytics-disable \
		--model openrouter/$(MODEL)

pull:
	docker pull paulgauthier/aider-full

