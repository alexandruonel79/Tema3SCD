import paho.mqtt.client as mqtt
import json
import logging
import os
import sys
from datetime import datetime
from db_func import save_to_db
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

logger = logging.getLogger("Info_Logger")

def setup_logging():
    # if the env variable is set, enable logging
    if os.getenv('DEBUG_DATA_FLOW') == 'true':
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            stream=sys.stdout
        )
        logger.info("Logging is enabled!")
    else:
        logger.disabled = True

def on_connect(client: mqtt.Client, userdata, flags, rc: int) -> None:
    if rc == mqtt.CONNACK_ACCEPTED:
        logger.info("Broker is connected!")
        client.subscribe('#')
    else:
        logger.info(f"Error connecting to broker: {rc}")

def is_valid_topic(topic):
    # it should contain two words, separated only by a '/'
    parts = topic.split('/')
    return len(parts) == 2 and all(parts)

def get_timestamp(payload):
    # check if the payload already contains a timestamp
    if payload.get('timestamp'):
        logger.info("Data timestamp is: %s", payload['timestamp'])
        return payload['timestamp']
    # otherwise create it now
    else:
        timezone_offset = timedelta(hours=2)
        curr_time = datetime.now(timezone(timezone_offset))
        timestamp = curr_time.isoformat()
        logger.info("Data timestamp is: NOW")
        return timestamp

def clean_payload(old_payload):
    new_payload = {}
    for key, value in old_payload.items():
        # if its a number, add it in the new payload
        if isinstance(value, (int, float)):
            new_payload[key] = value
    
    return new_payload

def extract_location_device(message):
    location = message.topic.split('/')[0]
    device = message.topic.split('/')[1]
    return location, device

def create_db_entries(location, device, payload, timestamp):
    json_payload = []
    # use all the data's as metrics for efficiency in influxdb
    for metric, data in payload.items():
        logger.info("%s.%s.%s %s", location, device, metric, data)
        db_entry = {
            "measurement": f"{location}_{device}_{metric}",
            "tags": {
                "location": location,
                "device": device,
                "metric": metric
                },
            "time": timestamp,
            "fields": {
                "data": float(data)
            }
        }
        json_payload.append(db_entry)
        
    return json_payload


def on_message(client: mqtt.Client, userdata, msg: mqtt.MQTTMessage) -> None:
    # check if the topic is valid
    if not is_valid_topic(msg.topic):
        logger.info("Invalid topic format! It needs to be location/device")
        return

    logger.info("Received a message by topic [%s]", msg.topic)
    # the body must be a JSON
    try:
        payload = json.loads(msg.payload.decode())
    except json.JSONDecodeError:
        logger.info("The body is not a JSON!")
        return

    location, device = extract_location_device(msg)
    # get the timestamp
    timestamp = get_timestamp(payload)
    # remove the unnecessary fields, and return a new payload
    payload = clean_payload(payload)
    # create the db entries
    json_payload = create_db_entries(location, device, payload, timestamp)
    # save the entries in the database
    save_to_db(json_payload)

def main():
    load_dotenv()
    BROKER_HOST = 'mqtt_broker'
    BROKER_PORT = 1883

    setup_logging()

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER_HOST, BROKER_PORT)

    client.loop_forever()

if __name__ == "__main__":
    main()