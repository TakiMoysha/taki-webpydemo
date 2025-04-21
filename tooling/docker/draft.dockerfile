FROM python:3.12.9-alpine3.21

RUN apk add --update \
  curl \
  gcc \
  g++ \
  git \
  libffi-dev \
  openssl-dev \
  python3-dev \
  build-base \
  linux-headers \
  && rm -rf /var/cache/apk/*

RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

ENV PYTHONUNBUFFERED=1 ENVIRONMENT=draft
ENV ROOT_DIR=/workspace
ENV DATABASE_DIR=/database
ENV APP_DIR=${ROOT_DIR}/app
ENV PYMS_CONFIGMAP_FILE=${ROOT_DIR}/config-docker.yaml
RUN mkdir $APP_DIR && adduser -S -D -H python

WORKDIR $APP_DIR
RUN chown -R python $APP_DIR
RUN pip install pipenv
COPY pipfile* /tmp/
RUN cd /tmp && pipenv lock --requirements > requirements.txt
RUN pip install -r /tmp/requirements.txt
COPY . $APP_DIR

RUN mkdir $DATABASE_DIR ; chmod 777 $DATABASE_DIR

EXPOSE 5000
USER python

CMD []

