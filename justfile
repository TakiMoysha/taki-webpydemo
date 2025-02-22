set dotenv-load

default_env := "stage"
default_app := "app.asgi:create_app"
alembic_config := "src/app/db/migrations/alembic.ini"


demo:
  docker-compose up --build

install:
    pre-commit install
    uv run python scripts/pre-build.py --install-packages

# ============================== DEVELOPMENT 
dev:
  uv run server --app {{default_app}} run --reload --debug --host 0.0.0.0 --port 8000


stage threads='2' workers="2":
  uv run server --app {{default_app}} run --reload --host 0.0.0.0 --port 8000 --threads {{threads}} --workers {{workers}} 


make-migrations:
  uv run app database make-migrations

migrate:
  uv run alembic -c {{alembic_config}} upgrade head

routes:
  uv run litestar --app {{default_app}} routes

schema:
  uv run litestar --app {{default_app}} schema openapi --output docs/schema.json --output docs/schema.json --output docs/schema.json --output docs/schema.json


test target="tests":
  uv run pytest -v -s --log-cli-level=INFO {{target}}


check:
  pre-commit run --all-files


# ============================== DOCS 
make-changelog:
  git cliff -o CHANGELOG.md

make-dependencies:
  uv export --format requirements-txt --output-file requirements.txt

kill-dev:
  ps aux | grep 'granian' | awk '{print $2}' | xargs kill
