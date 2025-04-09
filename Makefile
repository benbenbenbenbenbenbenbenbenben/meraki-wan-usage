export FLASK_APP=backend/server.py

FLASK_PORT=5002
SVELTE_PORT=5173

.PHONY: install setup-python-packages setup-node-packages backend-dev frontend-dev frontend-build run-prod 

install: setup-python-env setup-python-packages setup-node-packages
	@echo "[install]: All prerequisites installed."

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

