export FLASK_APP=backend/server.py

FLASK_PORT=5002
SVELTE_PORT=5173

.PHONY: install check-dependencies setup-python-packages setup-node-packages backend-dev frontend-dev frontend-build run-prod 

install: check-dependencies setup-python-env setup-python-packages setup-node-packages
	@echo "[install]: All prerequisites installed."

check-dependencies:
	@echo "[check-dependencies]: Verifying required dependencies..."

	@# --- Check Python version ---
	@PYTHON_VERSION=$$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"); \
	REQUIRED_PYTHON="3.12"; \
	if [ "$$(echo $$PYTHON_VERSION | awk -F. '{ printf("%d%02d", $$1, $$2) }')" -lt "$$(echo $$REQUIRED_PYTHON | awk -F. '{ printf("%d%02d", $$1, $$2) }')" ]; then \
		echo "[check-dependencies]: Python 3.12+ required. Found $$PYTHON_VERSION."; \
		exit 1; \
	else \
		echo "[check-dependencies]: Python version $$PYTHON_VERSION OK."; \
	fi

	@# --- Check Node.js ---
	@if ! command -v node >/dev/null 2>&1; then \
		echo "[check-dependencies]: Node.js is not installed. Please install it."; \
		exit 1; \
	else \
		echo "[check-dependencies]: Node.js found."; \
	fi

	@# --- Check npm ---
	@if ! command -v npm >/dev/null 2>&1; then \
		echo "[check-dependencies]: npm is not installed. Please install it."; \
		exit 1; \
	else \
		echo "[check-dependencies]: npm found."; \
	fi

	@echo "[check-dependencies]: All dependencies verified."


setup-python-packages:
	@echo "[setup-python-packages]: Installing python packages..."
	@cd backend && source venv/bin/activate && pip install -r requirements.txt
	@echo "[setup-python-packages]: Done."

setup-node-packages:
	@echo "[setup-node-packages]: Installing node packages..."
	@cd frontend && npm install
	@echo "[setup-node-packages]: Done."

setup-python-env:
	@echo "[setup-python-env]: Setting up python environment..."
	@cd backend && if [ -f venv/bin/activate ]; then \
		echo "[setup-python-env]: Python environment already set up. Skipping..."; \
	else \
		python3 -m venv venv; \
		echo "[setup-python-env]: Done."; \
	fi

backend-dev:
	cd backend && source venv/bin/activate && export FLASK_ENV=development && export FLASK_PORT=$(FLASK_PORT) && python server.py 

frontend-dev:
	cd frontend && BACKEND_PORT=$(FLASK_PORT) && npm run dev -- --host 127.0.0.1 --port $(SVELTE_PORT)

frontend-build:
	cd frontend && npm install && npm run build

run-prod: 
	cd backend && source venv/bin/activate && python server.py 

