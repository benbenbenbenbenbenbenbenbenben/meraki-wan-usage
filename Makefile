export FLASK_APP=backend/server.py
export FLASK_ENV=development

FLASK_PORT=5000
SVELTE_PORT=5173

.PHONY: backend frontend

backend:
	cd backend && source venv/bin/activate && python server.py --port=$(FLASK_PORT)

frontend:
	cd frontend && npm run dev -- --port $(SVELTE_PORT)
