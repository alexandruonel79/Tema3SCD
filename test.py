import paho.mqtt.client as mqtt
import json

# MQTT settings
BROKER_HOST = "localhost"  # Replace with your MQTT broker address
BROKER_PORT = 1883         # Default MQTT port
TOPIC = "UPB/DEV16"       # Topic to publish to

# The message to send
message = {
    "BAT": 16,
    "HUMID": 36,
    "PRJ": "SCD",
    "TMP": 305.3,
    "STATUS": "OK",
    "ERROR": "/bin/sh: 1: sudo: not found\n# apt install mosquitto-clients\nReading package lists... Done\nBuilding dependency tree... Done\nReading state information... Done\nE: Unable to locate package mosquitto-clients\n#"
}

# Function to handle connection
def on_connect(client, userdata, flags, rc):
    if rc == mqtt.CONNACK_ACCEPTED:
        print("Connected to broker!")
        # Publish the message once connected
        client.publish(TOPIC, json.dumps(message), qos=0, retain=False)
        print(f"Message sent to topic {TOPIC}: {message}")
    else:
        print(f"Connection failed with code {rc}")

# Function to handle message receipt (debugging purpose)
def on_message(client, userdata, msg):
    print(f"Message received: {msg.payload.decode()} on topic {msg.topic}")

# Set up the MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(BROKER_HOST, BROKER_PORT, 60)

# Start the loop to handle events
client.loop_forever()  # This will block the script and keep the connection alive
