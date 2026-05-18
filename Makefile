.PHONY: run-backend run-frontend test ingest clean help

help:
	@echo "🏈 CapCommander Enterprise Make Commands"
	@echo "  run-backend   - Start the FastAPI server"
	@echo "  run-frontend  - Start the Streamlit dashboard"
	@echo "  test          - Run all pytest unit tests"
	@echo "  ingest        - Run the V2 data ingestion pipeline"
	@echo "  docker-up     - Start everything with Docker Compose"
	@echo "  clean         - Remove database and __pycache__ files"

run-backend:
	uvicorn backend.app.main:app --reload

run-frontend:
	streamlit run app.py

test:
	pytest tests/

ingest:
	python scripts/run_v2_ingestion.py

docker-up:
	docker-compose up --build

clean:
	rm -f capcommander_v2.db
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache
