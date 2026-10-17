.PHONY: lint test run

lint:
	.venv\Scripts\uv run flake8 competition.py tests/

test:
	.venv\Scripts\uv run pytest tests/

run:
	set FLASK_APP=wsgi.py&& set FLASK_ENV=development&& set FLASK_DEBUG=1&& .venv\Scripts\uv run flask run --no-debugger --no-reload
