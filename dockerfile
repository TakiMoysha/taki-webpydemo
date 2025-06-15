FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

LABEL org.opencontainers.image.authors="takimoysha"
LABEL org.opencontainers.image.url="https://github.com/takimoysha/taki-pywebdemo"
LABEL org.opencontainers.image.source="https://github.com/takimoysha/taki-pywebdemo"


## =================================================== PYTHON CONFIGURATION
ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONFOULTHANDLER=1

RUN set -eux; \
  apt-get update; \
  apt-get autoremove -y; \
  rm -rf /var/lib/apt/lists/*; \
  rm -rf /root/.cache;

## =================================================== UV CONFIGURATION
ENV UV_COMPILE_BYTECODE=1 \
  UV_CACHE_DIR=/opt/uv-cache \
  UV_LINK_MODE=copy 


# bind uv.lock from host to container
# bind pyproject.toml from host to container
RUN --mount=type=cache,target=/opt/uv-cache \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  uv sync --frozen --no-install-project

## =================================================== APP CONFIGURATION
WORKDIR /workspace
COPY . /workspace

RUN chown -R www-data:www-data /app; \
  chmod +x ./scripts/entrypoint.sh;

USER www-data

EXPOSE 8000

HEALTHCHECK --interval=1m --timeout=5s --start-period=5s --retries=3 \
  CMD [ "/workspace/tooling/scripts/healthcheck.py", "http://localhost:8000/" ]

ENTRYPOINT ["./tooling/scripts/entrypoint.sh"]
