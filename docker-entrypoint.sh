#!/bin/sh

echo "Starting docker-entrypoint.sh"

set -e

echo "Starting Core..."

python main.py
