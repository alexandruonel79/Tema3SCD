import paho.mqtt.client as mqtt
import json
from datetime import datetime
from db_func import save_to_db

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
        json_payload = []
        measurement = msg.topic.split('/')[0]
        tags = msg.topic.split('/')[1]
        data = {
            "measurement": 'UPB.RPi_1.TEMP',
            "tags": {
                "sensor": 'RPi_1',

                },
            "time": datetime.now(),
            "fields": {
                
            }
        }
        json_payload.append(data)
        save_to_db(payload)
    except json.JSONDecodeError:
        print("Mesajul nu este JSON!")
        return
    


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER_HOST, BROKER_PORT)

client.loop_forever()