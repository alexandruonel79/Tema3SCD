#!/bin/bash
host="localhost"
port=1883

original_timestamp=$(date -u +"%Y-%m-%dT%H:%M:%S+02:00")

# WITH TIMESTAMP, LAST 6 HOURS
echo "Starting to publish messages with timestamps, last 6 hours"
for i in {1..10}; do
  topic="UPB/DEV$(shuf -i 0-5 -n 1)"

  random_hours=$(shuf -i 1-5 -n 1)
  random_minutes=$(shuf -i 0-59 -n 1)

  modified_timestamp=$(date -u -d "$original_timestamp - $random_hours hours - $random_minutes minutes" +"%Y-%m-%dT%H:%M:%S+02:00")

  bat=$(shuf -i 50-100 -n 1)
  humid=$(shuf -i 80-100 -n 1)
  tmp=$(shuf -i 0-40 -n 1)

  message='{"BAT": '$bat', "HUMID": '$humid', "PRJ": "SCD", "TMP": '$tmp', "STATUS": "OK", "timestamp": "'$modified_timestamp'"}'

  echo "Publishing message to topic $topic: $message"
  mosquitto_pub -h "$host" -p "$port" -t "$topic" -m "$message"
  sleep 1
done

# WITHOUT TIMESTAMP
echo "Starting to publish messages without timestamps"
for i in {0..5}; do
  topic="UPB/DEV$i"
  message='{"BAT": 100, "HUMID": 100, "PRJ": "SCD", "TMP": 100, "STATUS": "OK"}'
  echo "Publishing message to topic $topic: $message"
  mosquitto_pub -h "$host" -p "$port" -t "$topic" -m "$message"
  sleep 1
done

# LAST 48 HOURS
echo "Starting to publish messages with timestamps, last 48 hours"
for i in {0..5}; do
  topic="UPB/DEV$i"
  random_hours=$(shuf -i 1-48 -n 1)
  random_minutes=$(shuf -i 0-59 -n 1)
  modified_timestamp=$(date -u -d "$original_timestamp - $random_hours hours - $random_minutes minutes" +"%Y-%m-%dT%H:%M:%S+02:00")
  message='{"BAT": 100, "HUMID": 100, "PRJ": "SCD", "TMP": 100, "STATUS": "OK", "timestamp": "'$modified_timestamp'"}'
  echo "Publishing message to topic $topic: $message"
  mosquitto_pub -h "$host" -p "$port" -t "$topic" -m "$message"
  sleep 1
done

