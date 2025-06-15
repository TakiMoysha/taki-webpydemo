# ============================================================================== SUPPORT
set dotenv-load

export DEV_LAUNCH := "True"

defaul_test_db := "sqlite+asyncio:///tmp/test.sqlite3"
default_alembic_config := "database/migrations/alembic.ini"


# example: just init-alchemy services/messenger
[group: "support"]
init-alchemy project:
  uv --project={{ project }} run alchemy

# make changelog
[group: "support"]
changelog:
  git cliff -o CHANGELOG.md

# run pre-commit check
[group: "support"]
check:
  uv run pre-commit run --all-files   
# ============================================================================== DEMO

demo:
  docker-compose up --build

# ============================================================================== services

# --------------------------------------------------------------------- messenger
# exmaple: just clean-messenger
[group: "demoapp"]
[working-directory: "services/demoapp"]
dev-demoapp *ARGS:
  LITESTAR_DEBUG=True
  UV_PROJECT="services.demoapp" # debug
  uv run server_demoapp run --reload --host 0.0.0.0 --port 8000 --debug {{ ARGS }}

# --------------------------------------------------------------------- messenger
# exmaple: just clean-messenger
[group: "messenger"]
[working-directory: "services/messenger"]
clean-messenger:
  rm tmp/messenger.sqlite3

# example: just dev-messenger
[group: "messenger"]
[working-directory: "services/messenger"]
dev-messenger *ARGS:
  LITESTAR_DEBUG=True
  UV_PROJECT="services.messenger" # debug
  uv run server_messenger run --reload --host 0.0.0.0 --port 8000 --debug {{ ARGS }}

# example: just test-messenger
[group: "messenger"]
[working-directory: "services/messenger"]
test-messenger target="" *ARGS:
  LITESTAR_DEBUG=True
  UV_PROJECT="services.messenger" # debug
  uv run pytest --verbose --capture=no --sqlalchemy-connect-url={{ defaul_test_db }} {{ ARGS }} {{ target }}

# example: just messenger run
[group: "messenger"]
[working-directory: "services/messenger"]
messenger *ARGS:
  LITESTAR_DEBUG=True
  UV_PROJECT="services.messenger" # debug
  uv run server_messenger {{ ARGS }}

# --------------------------------------------------------------------- registry

[group: "registry"]
[working-directory: "services/registry"]
dev-registry *ARGS:
  LITESTAR_DEBUG=True
  UV_PROJECT="services.registry" # debug
  uv run server_registry run --reload --host 0.0.0.0 --port 8000 --debug {{ ARGS }}


# ============================================================================== packages

# example: just test-wsdk tests/test_draft.py::test_specific_test_by_function_name
[group: "wsdk"]
[working-directory: "libs/wsdk"]
test-wsdk target="" *ARGS:
  uv run pytest --verbose --capture=no --log-cli-level=INFO {{ ARGS }} {{target}}



#report-coverage:
#  uv run coverage report --fail-under=100 --show-missing -m

# ============================================================================== WIP
# docker-run:
#   docker run -it --rm --init --name stage-pywebdemo -p 8000:8000 --cpus=4 pywebdemo_app:latest
#
# docker-build:
#   docker build -t pywebdemo_app -f deploy/docker/demoapp.dockerfile .
#
# stage threads='2' workers="2":
#   uv run server --app {{default_app}} run --reload --host 0.0.0.0 --port 8000 --threads {{threads}} --workers {{workers}} 
#
# tunnel_up:
#   ngrok start default:api
#
# # migrate:
# #   uv run {{default_app}} database upgrade
#
# # make-migrations:
# #   uv run {{default_app}} database make-migrations
