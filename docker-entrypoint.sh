#!/bin/sh

echo "Starting docker-entrypoint.sh"

set -e

echo "Starting Core..."
rasa run --enable-api -p 5005 --cors "*"