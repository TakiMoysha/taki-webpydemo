#!/bin/env bash

set -euo pipefail

function postgres_wait() {
  local host=${POSTGRES_HOST:-localhost}
  local port=${POSTGRES_PORT:-5432}
  local timeout=${TIMEOUT:-10}
  local start_time=$(date +%s)

  netcat -z -w $timeout $host $port

  while [ $? -ne 0 ] && [ $(( $(date +%s) - $start_time )) -lt $timeout ]; do
    sleep 1
    netcat -z -w $timeout $host $port
  done

  if [ $(( $(date +%s) - $start_time )) -ge $timeout ]; then
    echo "Postgres is not available after $timeout seconds"
    exit 1
  fi
}
