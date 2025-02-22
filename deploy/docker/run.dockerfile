ARG PYTHON_BUILDER_IMAGE=3.12.8-bullseye

## ================================== PYHTON ================================== ##
FROM python:${PYTHON_BUILDER_IMAGE} as python-base
ENV PIP_DEFAULT_TIMEOUT=100 \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PIP_NO_CACHE_DIR=1 \
  PIP_ROOT_USER_ACTION=ignore \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONFAULTHANDLER=1 \
  PYTHONHASHSEED=random \
  LANG=C.UTF-8 \
  LC_ALL=C.UTF-8

RUN apt-get update \
  && apt-get upgrade -y \
  && apt-get install -y --no-install-recommends git \
  && apt-get autoremove -y \
  && apt-get clean -y \
  && rm -rf /root/.cache \
  && rm -rf /var/apt/lists/* \
  && rm -rf /var/cache/apt/* \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false\
  && mkdir -p /workspace/app \
  && pip install --quiet -U pip wheel setuptools virtualenv


## -------------------------- PYTHON BUILD BASE ----------------------------- ##
FROM python-base AS build-base
ARG UV_INSTALL_ARGS="--all-groups"
ENV UV_INSTALL_ARGS="${UV_INSTALL_ARGS}" \
  GRPC_PYTHON_BUILD_WITH_CYTHON=1 \
  PATH="/workspace/app/.venv/bin:/usr/local/bin:$PATH"


## -------------------------- ADD BUILD PACKAGES ----------------------------------- ##
RUN apt-get install -y --no-install-recommends build-essential curl \
  && apt-get autoremove -y \
  && apt-get clean -y \
  && rm -rf /root/.cache \
  && rm -rf /var/apt/lists/* \
  && rm -rf /var/cache/apt/* \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false

## -------------------------- INSTALL APPLICATION ----------------------------------- ##
WORKDIR /workspace/app
# INFO: UPDATE
COPY pyproject.toml uv.lock README.md .pre-commit-config.yaml LICENSE Makefile \
  package.json package-lock.json vite.config.ts tsconfig.json tsconfig.node.json \
  ./
COPY scripts ./scripts/
COPY public ./public/
COPY resources ./resources/
RUN python -m venv --copies /workspace/app/.venv \
  && /workspace/app/.venv/bin/pip install cython uv nodeenv  \
  && uv install ${UV_INSTALL_ARGS}
COPY src ./src/


## ================================ DEVELOPMENT BUILD =================================== ##

## ------------------------- USE BUILDER BASE --------------------------------------- ##
FROM build-base as dev-image
ARG ENV_SECRETS="runtime-secrets"
ARG LITESTAR_APP="app.asgi:app"

## --------------------------- STANDARDIZE EXECUTION ENV ----------------------------- ##
ENV PATH="/workspace/app/.venv/bin:$PATH" \
  VIRTUAL_ENV="/workspace/app/.venv" \
  ENV_SECRETS="${ENV_SECRETS}"  \
  PIP_DEFAULT_TIMEOUT=100 \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PIP_NO_CACHE_DIR=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONFAULTHANDLER=1 \
  PYTHONHASHSEED=random \
  LANG=C.UTF-8 \
  LC_ALL=C.UTF-8 \
  LITESTAR_APP="${LITESTAR_APP}"
WORKDIR /workspace/app
COPY docs/ docs/
COPY tests/ tests/
COPY src src/
RUN uv install $UV_INSTALL_ARGS
STOPSIGNAL SIGINT
EXPOSE 8000
CMD [ "litestar","run","--host","0.0.0.0"]
VOLUME /workspace/app
