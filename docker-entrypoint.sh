#!/bin/sh

echo "Starting docker-entrypoint.sh"

set -e

echo "Starting Core..."

python core/main.py
