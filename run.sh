#!/bin/bash

docker build --no-cache -t adapter_image -f "./adapter_impl/Dockerfile" .

docker stack deploy -c stack.yml scd3