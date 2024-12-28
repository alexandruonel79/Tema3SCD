import paho.mqtt.client as mqtt
import json
import logging
import os
import sys
from datetime import datetime
from db_func import save_to_db
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

BROKER_HOST = "host.docker.internal"
BROKER_PORT = 1883

def setup_logging():
    load_dotenv()
    if os.getenv('DEBUG_DATA_FLOW') == 'true':
        # print("Logging is enabled!")
        # Configure the logger to log INFO level and above
        logging.basicConfig(
            level=logging.INFO,  # Log only INFO and above
            format='%(asctime)s - %(message)s',  # Log message format with timestamp and message
            datefmt='%Y-%m-%d %H:%M:%S',
            stream=sys.stdout  # Define timestamp format without milliseconds
        )
        logger.info("Logging is enabled!")
    else:
        logger.disabled = True
        # print("Logging is disabled!")

def on_connect(client: mqtt.Client, userdata, flags, rc: int) -> None:
    if rc == mqtt.CONNACK_ACCEPTED:  # Use the built-in constant for connection success
        print("Conectat la broker!")
        client.subscribe('#')  # Subscribe to all topics
    else:
        print(f"Eroare la conectare: {rc}")

def is_valid_topic(topic):
    parts = topic.split('/')
    return len(parts) == 2 and all(parts)

def get_timestamp(payload):
    if payload.get('timestamp'):
        # return int 
        # return datetime.fromisoformat(payload['timestamp']).isoformat()
        logger.info("Data timestamp is: %s", payload['timestamp'])
        return payload['timestamp']
    else:
        timezone_offset = timedelta(hours=2)
        current_time = datetime.now(timezone(timezone_offset))
        formatted_timestamp = current_time.isoformat()
        logger.info("Data timestamp is: NOW")
        return formatted_timestamp

def clean_payload(old_payload):
    new_payload = {}
    for key, value in old_payload.items():
        if isinstance(value, (int, float)):
            new_payload[key] = value
    
    return new_payload

def on_message(client: mqtt.Client, userdata, msg: mqtt.MQTTMessage) -> None:
    logger.info("Received a message by topic [%s]", msg.topic)
    # print(f"\nMesaj primit pe topicul '{msg.topic}': {msg.payload.decode()}")
    # Check the topic, it should contain only one '/'
    if not is_valid_topic(msg.topic):
        print("Invalid topic!")
        return

    # check if its a json
    try:
        payload = json.loads(msg.payload.decode())
        # print("Payload: ", payload)
        json_payload = []
        location = msg.topic.split('/')[0]
        device = msg.topic.split('/')[1]
        timestamp = get_timestamp(payload)
        payload = clean_payload(payload)

        for key, value in payload.items():
            logger.info("%s.%s.%s %s", location, device, key, value)
            data = {
                "measurement": f"{location}_{device}_{key}",
                "tags": {
                    "location": location,
                    "device": device,
                    "metric": key
                    },
                "time": timestamp,
                "fields": {
                    "data": value
                }
            }
            json_payload.append(data)
        # print("Payload to be saved: ", json_payload)
        save_to_db(json_payload)

    except json.JSONDecodeError:
        print("Mesajul nu este JSON!")
        return

logger = logging.getLogger("Info_Logger")
setup_logging()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER_HOST, BROKER_PORT)

client.loop_forever()