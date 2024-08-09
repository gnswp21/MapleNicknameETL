#!/usr/bin/env bash
sudo docker build -t mykafka -f Dockerfile-kafka .
echo All Docker images have been built successfully.