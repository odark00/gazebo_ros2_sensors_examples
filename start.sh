#!/bin/bash
# Grants the container access to the host X server, then builds and starts it
# in the background. Work inside it with ./enter.sh.
set -e

xhost +local:docker >/dev/null

docker compose up --build -d "$@"
