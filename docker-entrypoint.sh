#!/bin/sh

echo "Starting docker-entrypoint.sh"

set -e

echo "Starting Core..."
rasa run --endpoints endpoints.yml --credentials credentials.yml -m app/models/prod_model.tar.gz --enable-api -p 5005 --cors "*"