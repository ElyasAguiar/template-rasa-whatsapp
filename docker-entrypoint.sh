#!/bin/sh

echo "Starting docker-entrypoint.sh"

set -e

echo "Starting SDK..."
rasa run --enable-api --debug -p 5005 --cors "*"