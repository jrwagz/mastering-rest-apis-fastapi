
.PHONY: .venv
.venv:
	uv venv --python python3.11 .venv
	. .venv/bin/activate && \
		uv pip install -r requirements.txt -r requirements-dev.txt

.PHONY: run
run:
	uvicorn socialapi.main:app --reload

.PHONY: run-gunicorn
run-gunicorn:
	gunicorn socialapi.main:app --workers 4 \
		--worker-class uvicorn.workers.UvicornWorker \
		--bind 0.0.0.0:8000

.PHONY: lint
lint:
	ruff check .
	black --check .
	isort --check .

.PHONY: format
format:
	ruff check --fix .
	black .
	isort .

.PHONY: ready
ready: format lint