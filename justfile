
[group: "registry"]
[working-directory: "services/registry"]
dev-registry *ARGS:
  uv run server run --reload --host 0.0.0.0 --port 8000 --threads 1 --workers 2 --debug {{ ARGS }}

[group: "wsdk"]
[working-directory: "libs/wsdk"]
test-wsdk target="" *ARGS:
  uv run pytest -v -s --log-cli-level=INFO {{ ARGS }} {{target}}


# ============================================================================== WIP

set dotenv-load

default_env := "stage"
default_app := "demoapp.asgi:create_app"
alembic_config := "src/demoapp/db/migrations/alembic.ini"


demo:
  docker-compose up --build

# ============================================================================== DEVELOPMENT 
install:
    uv run sync
    uv run pre-commit install


docker-run:
  docker run -it --rm --init --name stage-pywebdemo -p 8000:8000 --cpus=4 pywebdemo_app:latest

docker-build:
  docker build -t pywebdemo_app -f deploy/docker/demoapp.dockerfile .


dev app=default_app:
  LITESTAR_DEBUG=True uv run server --app {{default_app}} run --reload --host 0.0.0.0 --port 8000 --threads 1 --workers 2 --debug 

dev-messenger:
  cd messenger; LITESTAR_DEBUG=True uv run dev run --reload

stage threads='2' workers="2":
  uv run server --app {{default_app}} run --reload --host 0.0.0.0 --port 8000 --threads {{threads}} --workers {{workers}} 

tunnel_up:
  ngrok start default:api

# migrate:
#   uv run {{default_app}} database upgrade

# make-migrations:
#   uv run {{default_app}} database make-migrations

# ============================================================================== TESTS
test target="tests":
  uv run pytest -v -s --log-cli-level=INFO {{target}}

debug-test target:
  uv run pytest -v -s -rP {{target}}

check:
  uv run pre-commit run --all-files

# ============================================================================== DOCS 
routes:
  uv run litestar --app {{default_app}} routes

schema:
  uv run litestar --app {{default_app}} schema openapi --output docs/schema.json

make-changelog:
  git cliff -o CHANGELOG.md

make-dependencies:
  uv export --format requirements-txt --output-file requirements.txt

kill-dev:
  ps aux | grep 'granian' | awk '{print $2}' | xargs kill
