FROM python:3.12-slim-bookworm
LABEL maintainer="takimoysha"

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONFOULTHANDLER=1

RUN set -eux; \
  apt-get update; \
  apt-get autoremove -y; \
  rm -rf /var/lib/apt/lists/*; \
  rm -rf /root/.cache;

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app
COPY . /app

RUN chown -R www-data:www-data /app; \
  chmod +x ./scripts/entrypoint.sh;

RUN pip install --no-cache-dir --upgrade pip; \
  pip install --no-deps --no-cache-dir -r /app/requirements.txt

USER www-data

EXPOSE 8000

CMD ["./scripts/entrypoint.sh"]
