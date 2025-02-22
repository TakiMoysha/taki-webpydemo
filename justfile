demo:
  docker-compose up --build


test:
  uv run pytest

check:
  pre-commit run --all-files
