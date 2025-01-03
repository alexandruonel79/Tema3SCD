import paho.mqtt.client as mqtt
import json
import logging
import os
import sys
from datetime import datetime
from db_func import save_to_db
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

# problema pe windows doar, pe linux merge...
# BROKER_HOST = "host.docker.internal"
logger = logging.getLogger("Info_Logger")

def setup_logging():
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
        print("Conectat la broker!")
        client.subscribe('#')
    else:
        print(f"Eroare la conectare: {rc}")

def is_valid_topic(topic):
    parts = topic.split('/')
    return len(parts) == 2 and all(parts)

def get_timestamp(payload):
    if payload.get('timestamp'):
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

    if not is_valid_topic(msg.topic):
        print("Invalid topic!")
        return

    try:
        payload = json.loads(msg.payload.decode())
        json_payload = []
        location = msg.topic.split('/')[0]
        device = msg.topic.split('/')[1]
        timestamp = get_timestamp(payload)
        payload = clean_payload(payload)

        for metric, data in payload.items():
            logger.info("%s.%s.%s %s", location, device, metric, data)
            data = {
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
            json_payload.append(data)
        save_to_db(json_payload)

    except json.JSONDecodeError:
        print("Mesajul nu este JSON!")
        return


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