.PHONY: run pull run-bash run-root-bash run-model

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

