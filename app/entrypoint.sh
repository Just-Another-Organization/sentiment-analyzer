#!/bin/sh

INTERNAL_PORT=80
INTERNAL_HOST="0.0.0.0"

if [[ "${ENVIRONMENT}" == "production" ]]; then
  uvicorn main:app --host "${INTERNAL_HOST}" --port "${INTERNAL_PORT}"
else
  uvicorn main:app --host "${INTERNAL_HOST}" --port "${INTERNAL_PORT}" --reload --log-level=debug
fi