#!/bin/bash
host="localhost"
port=1883

send_messages() {
  local current_timestamp=$1
  local nr_hours=$2
  local timestamp_provided=$3

  topics=()
  for i in {0..9}; do
    topics+=("UPB/DEV$(shuf -i 0-3 -n 1)")
  done

  if [ "$timestamp_provided" == "true" ]; then
    # generate some timestamps
    timestamps=()
    for i in {0..9}; do
      random_hours=$(shuf -i 1-$nr_hours -n 1)
      random_minutes=$(shuf -i 0-59 -n 1)
      timestamps+=($(date -d "$current_timestamp - $random_hours hours - $random_minutes minutes" +"%Y-%m-%dT%H:%M:%S+02:00"))
    done
    # with timestamps
    for i in {0..9}; do

      bat=$(shuf -i 50-100 -n 1)
      humid=$(shuf -i 80-100 -n 1)
      tmp=$(shuf -i 0-40 -n 1)

      message='{"BAT": '$bat', "HUMID": '$humid', "PRJ": "SCD", "TMP": '$tmp', "STATUS": "OK", "timestamp": "'${timestamps[$i]}'"}'
      topic=${topics[$i]}
      echo "Publishing message to topic $topic: $message"
      mosquitto_pub -h "$host" -p "$port" -t "$topic" -m "$message"
      sleep 1
    done

  else
    # without timestamps
    for i in {0..9}; do

      bat=$(shuf -i 50-100 -n 1)
      humid=$(shuf -i 80-100 -n 1)
      tmp=$(shuf -i 0-40 -n 1)

      message='{"BAT": '$bat', "HUMID": '$humid', "PRJ": "SCD", "TMP": '$tmp', "STATUS": "OK"}'
      topic=${topics[$i]}
      echo "Publishing message to topic $topic: $message"
      mosquitto_pub -h "$host" -p "$port" -t "$topic" -m "$message"
      sleep 1
    done
  fi
}

current_timestamp=$(date +"%Y-%m-%dT%H:%M:%S+02:00")
# send for the last 6 hours
send_messages "$current_timestamp" 6 "true"
# send for the last 48 hours
send_messages "$current_timestamp" 48 "true"
# send without timestamp
send_messages "$current_timestamp" -1 "false"
