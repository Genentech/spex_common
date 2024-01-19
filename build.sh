#!/usr/bin/env bash

docker build -f ./common/Dockerfile -t spex.common:latest .
docker tag spex.common:latest ghcr.io/genentech/spex.common:latest
docker push ghcr.io/genentech/spex.common:latest