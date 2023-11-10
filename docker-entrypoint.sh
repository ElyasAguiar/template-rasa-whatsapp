#!/bin/sh

echo "Starting docker-entrypoint.sh"

set -e

echo "Starting SDK..."
rasa run --endpoints endpoints.yml --credentials credentials.yml -m models/prod_model.tar.gz --enable-api -p 5005 --cors "*"