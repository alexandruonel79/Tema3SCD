#!/bin/bash
echo "Building image for python adapter"
docker swarm init
docker build --no-cache -t adapter_image -f "./adapter_impl/Dockerfile" .
echo "Deploying stack, duration: 10s"
docker stack deploy -c stack.yml scd3
for i in {10..1}; do
  echo "$i seconds remaining..."
  sleep 1
done
echo "Stack deployed"