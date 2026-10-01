.PHONY: setup-venv
setup-venv: ## Set up the Python virtual environment and synchronize dependencies
	uv venv
	source venv/bin/activate
	uv sync
