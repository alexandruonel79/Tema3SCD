import paho.mqtt.client as mqtt
import json
from datetime import datetime
from db_func import save_to_db
from datetime import datetime, timezone, timedelta

BROKER_HOST = "localhost"
BROKER_PORT = 1883

def on_connect(client: mqtt.Client, userdata, flags, rc: int) -> None:
    if rc == mqtt.CONNACK_ACCEPTED:  # Use the built-in constant for connection success
        print("Conectat la broker!")
        client.subscribe('#')  # Subscribe to all topics
    else:
        print(f"Eroare la conectare: {rc}")

def is_valid_topic(topic):
    parts = topic.split('/')
    return len(parts) == 2 and all(parts)

def get_timestamp(timestamp=None):
    if timestamp:
        return timestamp
    else:
        timezone_offset = timedelta(hours=3)
        current_time = datetime.now(timezone(timezone_offset))
        formatted_timestamp = current_time.isoformat()
        return formatted_timestamp

def clean_payload(old_payload):
    new_payload = {}
    for key, value in old_payload.items():
        if isinstance(value, (int, float)) or key == "timestamp":
            new_payload[key] = value
    
    return new_payload

def on_message(client: mqtt.Client, userdata, msg: mqtt.MQTTMessage) -> None:
    print(f"\nMesaj primit pe topicul '{msg.topic}': {msg.payload.decode()}")
    # Check the topic, it should contain only one '/'
    if not is_valid_topic(msg.topic):
        print("Invalid topic!")
        return

    # check if its a json
    try:
        payload = json.loads(msg.payload.decode())
        print("Payload: ", payload)
        payload = clean_payload(payload)
        json_payload = []
        location = msg.topic.split('/')[0]
        device = msg.topic.split('/')[1]
        timestamp = get_timestamp(payload["timestamp"])

        for key, value in payload.items():
            if key == "timestamp":
                continue

            data = {
                "measurement": f"{location}_{device}_{key}",
                "tags": {
                    "location": location,
                    "device": device
                    },
                "timestamp": timestamp,
                "fields": {
                    "value": value
                }
            }
            json_payload.append(data)
        print("Payload to be saved: ", json_payload)
        save_to_db(json_payload)

    except json.JSONDecodeError:
        print("Mesajul nu este JSON!")
        return
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER_HOST, BROKER_PORT)

client.loop_forever()