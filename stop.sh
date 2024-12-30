#!/bin/bash
docker stack rm scd3
# wait 10 seconds for the stack to be removed
echo "Removing stack, waiting 10 seconds for all network connections to be closed..."
sleep 10
echo "Stack removed. Deleting volumes..."
docker volume rm scd3_influxdb_data
docker volume rm scd3_grafana-data
echo "Stack and volumes removed."